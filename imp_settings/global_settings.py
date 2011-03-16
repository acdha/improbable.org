# -*- coding: utf-8 -*-

from urlparse import urljoin
import logging
import os
import subprocess
import time

from mingus.settings import *

try:
    git_rev = subprocess.Popen(
        ("git", "rev-parse", "HEAD"),
        stdout=subprocess.PIPE,
        cwd=os.path.dirname(__file__),
    ).communicate()[0]
    MEDIA_KEY = git_rev.strip()
except (OSError, IOError), e:
    logging.warning("Unable to set MEDIA_KEY from Git (will fall back to timestamp): %s", e)
    MEDIA_KEY = time.time()

LOCAL_DEV       = False
DEBUG           = False
TEMPLATE_DEBUG  = DEBUG

#sorl-thumbnail
THUMBNAIL_DEBUG = DEBUG

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(MEDIA_ROOT, "static")
STATIC_URL = urljoin(MEDIA_URL, "static/")

TEMPLATE_DIRS += (os.path.realpath(os.path.join(PROJECT_ROOT, 'templates')), )

# SECURITY NOTE: Change these in your production config!
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

CACHE_BACKEND                   = 'locmem://'
CACHE_MIDDLEWARE_SECONDS        = 60 * 5
CACHE_MIDDLEWARE_KEY_PREFIX     = 'improbable.org.'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Turn on some helpful template variables:
TEMPLATE_CONTEXT_PROCESSORS += ('sugar.context_processors.site_settings',)

# NOTE: Your IP must be in this file to use django-debug-toolbar:
INTERNAL_IPS = ('127.0.0.1',)

# django-markup
MARKUP_CHOICES = (
    'none',
    'markdown',
    'textile',
    'restructuredtext'
)
