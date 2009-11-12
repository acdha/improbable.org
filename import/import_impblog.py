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

tree = objectify.parse(file("impblog.xml"))

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
    
    post.markup   = "none" # Yes, really
    post.title    = attrs['Title']
    post.created  = parse_date(attrs['Created'])
    post.modified = parse_date(attrs['Modified'])
    post.publish  = max(post.created, post.modified)
    post.body     = attrs['Body']
    post.owner    = owner
    post.slug     = attrs['TextID'] or slugify(attrs['Title'])
    # TODO: Handle len>50
    post.status   = 2 if attrs['Visible'] == "True" else 1
    post.tease    = attrs['Summary']
    
    post_form = PostForm(model_to_dict(post), instance=post)
    if not post_form.is_valid():
        print "ERROR: Can't import #%s: %s" % (post.pk, post_form.errors.as_text())
        continue
        
    post_form.save()
    
    print "Imported post #%d: %s" % (post.pk, post.title)
