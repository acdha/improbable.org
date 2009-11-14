#!/usr/bin/env python

from django.core.management import setup_environ
from mingus import settings

setup_environ(settings)

from basic.blog.models import Post
from dateutil.parser import parse as parse_date
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.forms import ModelForm
from django.forms.models import model_to_dict
from lxml import objectify
from lxml.html import html5parser
from lxml.html import tostring as html_tostring
import codecs

import difflib
import sys

tree = objectify.parse(codecs.open("impblog.xml", "rb"))

root = tree.getroot()

documents = root.find('//table_data[@name="Documents"]')

owner = User.objects.get_or_create(username="chris")[0]

class PostForm(ModelForm):
    class Meta:
        model = Post

for doc in documents.getchildren():
    # Build a non-wanky data structure from the MySQL dump output:
    attrs = dict(
        (i.attrib['name'], unicode(i) if i else i) for i in doc.getchildren()
    )

    attrs['ID'] = int(attrs['ID'])
    if attrs['ID'] <= 2:
        continue # Skip the containers

    assert attrs['Parent'] == "2"

    post, created = Post.objects.get_or_create(pk=attrs['ID'])

    full_html     = html5parser.parse("http://improbable.org/chris/?ID=%d" % attrs['ID'])

    post.markup   = "none" # Yes, really
    post.title    = unicode(full_html.xpath("/html/head/title")[0].text_content()).strip().replace(u"Chris Adams: ", u"")
    post.created  = parse_date(attrs['Created'])
    post.modified = parse_date(attrs['Modified'])
    post.publish  = max(post.created, post.modified)

    post.body     = u""

    blog_entry_el = full_html.find('//div[@class="BlogEntry"]')

    blog_entry_el.rewrite_links(lambda i: i.replace("\n", "").strip())

    for pre in blog_entry_el.cssselect("pre.code"):
        pre.attrib['class'] += " prettyprint"

    if blog_entry_el.text:
        post.body += unicode(blog_entry_el.text)

    for c in blog_entry_el:
        post.body += html_tostring(c, encoding=unicode)

    if post.body != attrs['Body']:
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
    post.tease  = launder_html(attrs['Summary'], as_text=True)

    post_form   = PostForm(model_to_dict(post), instance=post)
    if not post_form.is_valid():
        print "ERROR: Can't import #%s: %s" % (post.pk, post_form.errors.as_text())
        continue

    post_form.save()

    print "Imported post #%d: %s" % (post.pk, post.title)
