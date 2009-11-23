# -*- coding: utf-8 -*-

from django.conf import settings
import os

DEBUG           = True
TEMPLATE_DEBUG  = DEBUG
COMPRESS        = False
LOCAL_DEV       = True
THUMBNAIL_DEBUG = DEBUG #sorl-thumbnail

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME   = os.path.join(os.path.dirname(__file__), 'dev.db')

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
STATIC_ROOT= os.path.join(MEDIA_ROOT, "static")

INSTALLED_APPS = settings.INSTALLED_APPS + ["django_wysiwyg"]

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
) + settings.TEMPLATE_DIRS

SECRET_KEY          = '6es\f,@F-2O4}{yY1w&mzTh!NsSm\me'
HONEYPOT_FIELD_NAME = 'Jung24_avers'

#django-contact-form
DEFAULT_FROM_EMAIL = 'contact-form@improbable.org'

ADMINS = (
    ('Chris Adams', 'chris@improbable.org'),
)
MANAGERS = ADMINS

EMAIL_HOST          = '127.0.0.1'
EMAIL_PORT          = 25
EMAIL_HOST_USER     = ''
EMAIL_HOST_PASSWORD = ''

CACHE_BACKEND                   = 'dummy://'
CACHE_MIDDLEWARE_SECONDS        = 60*5
CACHE_MIDDLEWARE_KEY_PREFIX     = 'improbable.org.'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
}

### django-markup
MARKUP_CHOICES = (
    'none',
    #'markdown',
    'restructuredtext'
)


if os.environ['HOSTNAME'].endswith("webfaction.com"):
    from deploy import *
