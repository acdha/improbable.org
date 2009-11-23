#!/home/acdha/.virtualenvs/imp_chris/bin/python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mingus.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
