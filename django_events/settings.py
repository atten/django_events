import socket
import os

from django.core.urlresolvers import reverse_lazy

gettext = lambda s: s

DEBUG = True

# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = BASE_DIR
PROJECT_PATH = ROOT_PATH
PROJECT_NAME = os.path.basename(ROOT_PATH)
PROJECT_DATA_DIR = os.path.join(BASE_DIR, PROJECT_NAME, 'data')
__TEMPLATE_DIR = os.path.join(BASE_DIR, PROJECT_NAME, 'templates')

VIRTUAL_ENV_DIR = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir))
LOGGING_DIR = os.path.join(VIRTUAL_ENV_DIR, 'log')

STATIC_ROOT = os.path.join(ROOT_PATH, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/media/'

LOCAL_SETTINGS_FILE = os.path.join(BASE_DIR, PROJECT_NAME, 'local_settings.py')
SECRET_SETTINGS_FILE = os.path.join(BASE_DIR, PROJECT_NAME, 'secret_settings.py')


# ------
for path in [LOGGING_DIR, STATIC_ROOT, MEDIA_ROOT, PROJECT_DATA_DIR, __TEMPLATE_DIR]:
    if not os.path.exists(path):
        os.makedirs(path, mode=0o755, exist_ok=True)

if not os.path.exists(SECRET_SETTINGS_FILE):
    with open(SECRET_SETTINGS_FILE, 'w') as f:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        f.write("SECRET_KEY = '%s'\n" % get_random_string(50, chars))
        f.close()

if not os.path.exists(LOCAL_SETTINGS_FILE):
    with open(LOCAL_SETTINGS_FILE, 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.close()

from .secret_settings import *

# HOSTS
HOSTNAME = socket.gethostname()
RELEASE_HOSTS = [
    'hatebase',
    'burble',
]

ALLOWED_HOSTS = [
    HOSTNAME,
    '127.0.0.1',
    'events.etc-marfa.ru',
]

if HOSTNAME in RELEASE_HOSTS:
    DEBUG = False


INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    # 'django.contrib.admin',
    # 'django.contrib.sites',
    'rest_framework',
    'events',
]

if not DEBUG:
    import raven
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)


MIDDLEWARE_CLASSES = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'django_events.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [__TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_events.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'msa_events',
        'USER': '',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': 60
    }
}


LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('en', gettext('en')),
    ('ru', gettext('ru')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# BATTERIES
# =========
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('events.permissions.HasValidApiKey',),
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('url_filter.integrations.drf.DjangoFilterBackend',)
}


# REDEFINE
from .local_settings import *
