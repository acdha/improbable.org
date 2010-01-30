#!/home/acdha/.virtualenvs/imp_chris/bin/python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mingus.settings'

from django.conf import settings

if settings.DEBUG or settings.LOCAL_DEV:
    print >>sys.stderr, "Settings config unrecoverably broken; not starting"
    sys.exit(1)

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
