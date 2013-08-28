"""Common settings and globals."""

import sys
import os
from os.path import abspath, basename, dirname, join, normpath


########## PATH CONFIGURATION

# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name.
SITE_NAME = basename(DJANGO_ROOT)

# Absolute filesystem path to the top-level project folder.
SITE_ROOT = dirname(DJANGO_ROOT)

# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.

SECRET_DIR = normpath(join(SITE_ROOT, 'deploy'))

if not os.path.isdir(SECRET_DIR):
    os.makedirs(SECRET_DIR)

SECRET_FILE = normpath(join(SECRET_DIR, 'SECRET_FILE'))


# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(SITE_ROOT)
sys.path.append(normpath(join(SITE_ROOT, 'apps')))
sys.path.append(normpath(join(SITE_ROOT, 'libs')))


########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION

# Disable debugging by default.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION

# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ("Matthew Tiger", "matthew@jetpackjoust.com"),
)

MANAGERS = ADMINS

########## END MANAGER CONFIGURATION


########## GENERAL CONFIGURATION

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html.
LANGUAGE_CODE = 'en-us'

# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and a
# single database can manage content for multiple sites.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# Sets the date format to ISO standards.
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:m:s'

########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = 'media/'

########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION

# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = normpath(join(SITE_ROOT, 'static'))

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files.
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

########## END STATIC FILE CONFIGURATION


########## TEMPLATE CONFIGURATION

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

# Directories to search when loading templates.
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
    normpath(join(SITE_ROOT, 'apps', 'articles', 'templates')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages")

########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin panel and documentation.
    'django.contrib.admin',
    'django.contrib.admindocs',

    # django-taggit for tagging of articles.
    'taggit',

    # apps used by website.
    'home',
    'articles'
    )

########## END APP CONFIGURATION


########## URL CONFIGURATION

ROOT_URLCONF = '{}.urls'.format(SITE_NAME)

########## END URL CONFIGURATION


########## KEY CONFIGURATION

# Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        import random
        SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
        secret = file(SECRET_FILE, 'w')
        secret.write(SECRET_KEY)
        secret.close()
    except IOError:
        raise Exception('Cannot open file `{}` for writing.'.format(SECRET_FILE))

########## END KEY CONFIGURATION
