# -*- coding: utf-8 -*-

import time

from imp_settings.global_settings import *

MEDIA_KEY = time.time()

LOCAL_DEV       = True
DEBUG           = True
TEMPLATE_DEBUG  = DEBUG

#sorl-thumbnail
THUMBNAIL_DEBUG = DEBUG

# Completely disable caching to avoid masking performance problems:
if DEBUG and False:
    CACHE_BACKEND = "dummy://"

DATABASES = {
    'default': {
        'NAME': os.path.join(PROJECT_ROOT, 'dev.db'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS += ('debug_toolbar', 'django_extensions', 'test_utils')

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
