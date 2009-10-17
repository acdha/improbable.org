# -*- coding: utf-8 -*-
import logging
import os, sys
from os.path import join, dirname, normpath
import re

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG           = True
TEMPLATE_DEBUG  = DEBUG
LOCAL_DEV       = DEBUG

#sorl-thumbnail
THUMBNAIL_DEBUG = DEBUG

MEDIA_ROOT         = join(PROJECT_ROOT, 'media')
MEDIA_URL          = '/media/'
STATIC_ROOT        = join(MEDIA_ROOT, 'static')
STATIC_URL         = '/media/static/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

SITE_ID      = 1
ROOT_URLCONF = 'mingus.urls'

SECRET_KEY          = '6es\f,@F-2O4}{yY1w&mzTh!NsSm\me'
HONEYPOT_FIELD_NAME = 'Jung24_avers'

ADMINS       = ()
MANAGERS     = ()
INTERNAL_IPS = ('127.0.0.1',)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME   = os.path.join(PROJECT_ROOT, "dev.db")

# Localization settings:
USE_I18N      = False
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
  os.path.join(PROJECT_ROOT, "templates"),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'sugar.middleware.debugging.UserBasedExceptionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'djangodblog.DBLogMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "basic.blog.context_processors.blog_settings",
    "mingus.core.context_processors.site_info",
    "navbar.context_processors.navbars",
)

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.admin',
  'django.contrib.sitemaps',
  'django.contrib.flatpages',
  'django.contrib.redirects',

  'django_extensions',
  'tagging',
  'djangodblog',
  'disqus',
  'basic.inlines',
  'basic.blog',
  'basic.bookmarks',
  'basic.media',
  'oembed',
  'flatblocks',
  'south',
  'navbar',
  'sorl.thumbnail',
  'template_utils',
  'django_proxy',

  'django_markup',
  'google_analytics',
  'robots',
  'basic.elsewhere',
  'compressor',
  'contact_form',
  'honeypot',
  'sugar',
  'quoteme',
  'mingus',
)

try:
    from local_settings import *
except ImportError, e:
    print >> sys.stderr, "Unable to import local_settings: continuing using development settings. Error: %s" % e

# n.b. This will have no effective if logging has already been configured in
# this process. If you want to change what logging does, set it in a place like
# local_settings.py or your WSGI app:

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(levelname)s: %(message)s'
)

if DEBUG:
    try:
        import debug_toolbar

        INSTALLED_APPS += ('debug_toolbar',)
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    except ImportError:
        logging.info("Running debug mode without debug_toolbar: install it if you need it")

