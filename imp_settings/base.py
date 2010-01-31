from urlparse import urljoin
import logging
import os

execfile("/Users/ctadams/Projects/django-mingus/mingus/settings.py")
# mingus = __import__("mingus")
# execfile(os.path.join(os.path.dirname(mingus.__file__), "settings.py"))

try:
    import subprocess
    git_rev = subprocess.Popen(
        ("git", "rev-parse", "HEAD"),
        stdout=subprocess.PIPE,
        cwd=os.path.dirname(__file__),
    ).communicate()[0]
    MEDIA_KEY = git_rev.strip()
except (OSError, IOError), e:
    logging.warning("Unable to set MEDIA_KEY from Git (will fall back to %s mtime): %s", __file__, e)
    MEDIA_KEY = os.stat(__file__).st_mtime

LOCAL_DEV       = True
DEBUG           = False
TEMPLATE_DEBUG  = DEBUG

#sorl-thumbnail
THUMBNAIL_DEBUG = DEBUG

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', 'media')
STATIC_ROOT= os.path.join(MEDIA_ROOT, "static")
STATIC_URL = urljoin(MEDIA_URL, "static/")

TEMPLATE_DIRS += (
    os.path.join(os.path.dirname(__file__), '..', 'templates'),
)

# SECURITY NOTE: Change these in your production config!
SECRET_KEY          = '6es\f,@F-2O4}{yY1w&mzTh!NsSm\me'
HONEYPOT_FIELD_NAME = 'Jung24_avers'

#django-contact-form
DEFAULT_FROM_EMAIL = 'contact-form@improbable.org'

ADMINS = (
    ('Chris Adams', 'chris@improbable.org'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME   = os.path.join(os.path.dirname(__file__), 'dev.db')

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

# I dislike the django-request performance anti-pattern, so we'll disable it:
INSTALLED_APPS = tuple(
    app for app in INSTALLED_APPS if app not in ('request', 'compressor')
)
MIDDLEWARE_CLASSES = tuple(
        i for i in MIDDLEWARE_CLASSES if not i.startswith("request.")
)

# NOTE: Your IP must be in this file to use django-debug-toolbar:
INTERNAL_IPS = ('127.0.0.1',)

# django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

# django-markup
MARKUP_CHOICES = (
    'none',
    'markdown',
    'textile',
    'restructuredtext'
)