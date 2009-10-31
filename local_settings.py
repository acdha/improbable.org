# -*- coding: utf-8 -*-

#django-contact-form
DEFAULT_FROM_EMAIL = 'contact-form@improbable.org'

ADMINS = (
    ('Chris Adams', 'chris@improbable.org'),
)
MANAGERS = ADMINS

# TODO: Configure email sensibly:
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'ABC'
EMAIL_HOST_PASSWORD = 'ABC'
EMAIL_USE_TLS       = True

# TODO: Enable memcache
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
    'markdown',
    'restructuredtext'
)

