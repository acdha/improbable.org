#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import HTMLParser
import sys

import simplejson

import requests

from django.db import IntegrityError
from django.template.defaultfilters import slugify

from basic.bookmarks.models import Bookmark

HTML_PARSER = HTMLParser.HTMLParser()

def import_item(item):
    time_updated = datetime.fromtimestamp(item['updated'])
    time_published = datetime.fromtimestamp(item['published'])

    assert len(item['alternate']) == 1

    url = item['alternate'][0]['href']

    if 'feedproxy' in url:
        url = requests.get(url).url
        item['alternate'][0]['href'] = url  # In place update for error reporting below

    title = item.get('title', 'Untitled')
    title = HTML_PARSER.unescape(title)

    slug = slugify(item['id'])

    b, created = Bookmark.objects.get_or_create(slug=slug,
                                                defaults={"modified": time_updated,
                                                          "created": time_published,
                                                          "url": url,
                                                          'title': title})

    b.description = u'<div class="googlereader description" data-google-id="%s">' % item['id']

    for annotation in item['annotations']:
        b.description += u'<p class="annotation">%s</p>' % annotation['content']

    if 'content' in item:
        b.description += u'<blockquote>%s</blockquote>' % item['content']['content']

    if 'summary' in item:
        b.description += u'<blockquote>%s</blockquote>' % item['summary']['content']

    b.description += u'</div>'

    b.tags = "googlereader"

    try:
        b.full_clean()
    except IntegrityError:
        b.slug = u"%s-%s%s%s" % (b.slug, time_published.year,
                                 time_published.month, time_published.day)
        b.full_clean()

    b.save()

    # Defeat auto_now / auto_now_add logic:
    Bookmark.objects.filter(pk=b.pk).update(modified=time_updated,
                                            created=time_published)


for filename in sys.argv[1:]:
    with open(filename, "rb") as f:
        data = simplejson.load(f)

    for item in data['items']:
        try:
            import_item(item)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print >>sys.stderr, "Unable to import %s: %s" % (item['id'], e)

            try:
                print >>sys.stderr, "\t", item['title']
                print >>sys.stderr, "\t", item['alternate'][0]['href']
            except (KeyError, IndexError):
                pass

            continue
