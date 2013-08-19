"""Development settings and globals."""

from common import *
from os.path import join, normpath

########## DEBUG CONFIGURATION

DEBUG = True
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION


########## MEDIA CONFIGURATION

MEDIA_URL = 'http://127.0.0.1:8000/media/'

########## END MEDIA CONFIGURATION


########## EMAIL CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(SITE_ROOT, 'dev_database', 'content.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

########## END DATABASE CONFIGURATION
