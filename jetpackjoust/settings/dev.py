"""Development settings and globals."""
import os
import sys
from os.path import dirname, realpath

from jetpackjoust.settings.common import *

########## DEBUG CONFIGURATION

DEBUG = True
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION


########## ALLOWED HOSTS CONFIGURATION

ALLOWED_HOSTS = ['localhost']

########## END ALLOWED HOSTS


######### SITE CONFIGURATION

# primary key from django_site table is 1 for localhost:8000

SITE_ID = 1

######## END SITE CONFIGURATION


########## MEDIA CONFIGURATION

MEDIA_URL = '/media/'

########## END MEDIA CONFIGURATION


########## EMAIL CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION


def get_db_credentials():
    """Helper function to grab username and password from relative path
    ../../../deploy/db_credentials and returns dictionary containing keys
    "user" and "password", which are the first entries of the lines in file.
    """
    location = os.path.join(dirname(dirname(dirname(realpath(__file__)))),
                            'deploy', 'db_credentials')
    try:
        with open(location) as f:
            lines = [line.strip('\n').split('\t') for line in f.readlines()]
            credentials = {line[0]: line[1] for line in lines}
    except(IOError):
        sys.exit(1)
    return credentials


credentials = get_db_credentials()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jpj_content',
        'USER': credentials['user'],
        'PASSWORD': credentials['password'],
        'HOST': '',
        'PORT': '',
    }
}

########## END DATABASE CONFIGURATION
