#!/usr/bin/env python

from dateutil.parser import parse as parse_date
from lxml import objectify
from lxml.html import html5parser
from lxml.html import tostring as html_tostring

import codecs
import difflib
import os
import sys
import urllib
import urlparse

from django.core.management import setup_environ
from mingus import settings

setup_environ(settings)

from django.contrib.auth.models import User
from django.core.files.base import File, ContentFile
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.http import QueryDict
from django.template.defaultfilters import slugify

from basic.blog.models import Post
from basic.media.models import Photo, Video
from mingus import settings

DEBUG = False

tree = objectify.parse(codecs.open("impblog.xml", "rb"))

root = tree.getroot()

documents = root.find('//table_data[@name="Documents"]')

owner = User.objects.get_or_create(username="chris")[0]

class PostForm(ModelForm):
    class Meta:
        model = Post

def link_launderer(link):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(link)
    if netloc == "improbable.org":
        if not path.startswith("/chris/"):
            return link

        filename       = urllib.unquote(os.path.basename(path))
        base_name, ext = os.path.splitext(filename)

        if path.startswith('/chris/index.php'):
            q_vals = QueryDict(query)

            if not "ID" in q_vals:
                print >>sys.stderr, "No ID in %s?" % link
            else:
                try:
                    return Post.objects.get(pk=q_vals['ID']).get_absolute_url()
                except Post.DoesNotExist:
                    print >>sys.stderr, "Couldn't load post for %s; returning unmodified %s" % (q_vals['ID'], link)

        if ext.lower() in ('.jpg', '.png', '.gif'):
            photo, created = Photo.objects.get_or_create(source_url=link)
            if created:
                photo.photo.save(filename, ContentFile(urllib.urlopen(link).read()), save=False)
                photo.title      = filename
                photo.slug       = slugify(base_name)
                photo.save()
            return photo.photo.url
        elif ext.lower() in ('.mov', '.mp4', '.m4v'):
            video, created = Video.objects.get_or_create(source_url=link)
            if created:
                file(os.path.join(settings.MEDIA_ROOT, "videos", filename), "wb").write(urllib.urlopen(link).read())
                video.video = os.path.join("videos", filename)
                video.title = filename
                video.slug  = slugify(base_name)
                video.save()
            return os.path.join(settings.MEDIA_URL, "videos", urllib.quote(filename))
        else:
            print >>sys.stderr, "No idea what to do with a %s file: %s" % (ext, link)

    return link.replace("\n", "").strip()

for doc in documents.getchildren():
    # Build a non-wanky data structure from the MySQL dump output:
    attrs = dict(
        (i.attrib['name'], unicode(i) if i else i) for i in doc.getchildren()
    )

    attrs['ID'] = int(attrs['ID'])
    if attrs['ID'] <= 2:
        continue # Skip the containers

    assert attrs['Parent'] == "2"

    post, created      = Post.objects.get_or_create(pk=attrs['ID'])

    full_html          = html5parser.parse("http://improbable.org/chris/?ID=%d" % attrs['ID'])

    post.markup        = "none" # Yes, really
    post.title         = unicode(full_html.xpath("/html/head/title")[0].text_content()).strip().replace(u"Chris Adams: ", u"")
    post.created       = parse_date(attrs['Created'])
    post.modified      = parse_date(attrs['Modified'])
    post.publish       = max(post.created, post.modified)

    post.body          = u""

    blog_entry_el      = full_html.find('//div[@class="BlogEntry"]')

    # TODO: Deal with local media files and page links

    blog_entry_el.make_links_absolute(base_url="http://improbable.org/chris/")
    blog_entry_el.rewrite_links(link_launderer)

    for pre in blog_entry_el.cssselect("pre.code"):
        pre.attrib['class'] += " prettyprint"

    if blog_entry_el.text:
        post.body += unicode(blog_entry_el.text)

    for c in blog_entry_el:
        post.body += html_tostring(c, encoding=unicode)

    if DEBUG and (post.body != attrs['Body']):
        print >>sys.stderr, "Mismatch between imported content and web-delivered:"
        print >>sys.stderr, "\n".join(difflib.unified_diff(attrs['Body'].split(), post.body.split(), "Dump", "HTTP", lineterm=""))

    post.owner    = owner

    if attrs['TextID']:
        post.slug = attrs['TextID']
    else:
        post.slug = slugify(post.title.encode("ascii", "replace"))

    if len(post.slug) > 50:
        slug_parts = post.slug.split("-")
        post.slug  = slug_parts.pop(0)

        for p in slug_parts:
            if len(post.slug) + len(p) >= 49:
                break
            post.slug += "-%s" % p

    post.status = 2 if attrs['Visible'] == "True" else 1

    if attrs['Summary']:
        post.tease  = html_tostring(html5parser.parse(attrs['Summary']), method="text").strip()
    else:
        post.tease = None

    post_form   = PostForm(model_to_dict(post), instance=post)
    if not post_form.is_valid():
        print "ERROR: Can't import #%s: %s" % (post.pk, post_form.errors.as_text())
        continue

    post_form.save()

    print "Imported post #%d: %s" % (post.pk, post.title)
