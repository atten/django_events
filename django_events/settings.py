import os
import socket

from django_docker_helpers.utils import load_yaml_config

from . import __version__


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

# create and populate secret_settings && local_settings
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
        f.write('\n')
        f.close()


from .secret_settings import *  # noqa


# =================== LOAD YAML CONFIG =================== #
CONFIG, configure = load_yaml_config(
    '',
    os.path.join(
        BASE_DIR, 'django_events', 'config',
        os.environ.get('DJANGO_CONFIG_FILE_NAME', 'without-docker.yml')
    )
)
# ======================================================== #

DEBUG = configure('debug', False)
SECRET_KEY = configure('secret_key', SECRET_KEY)

HOSTNAME = socket.gethostname()
ALLOWED_HOSTS = [HOSTNAME] + configure('hosts', [])
INTERNAL_IPS = configure('internal_ips', ['127.0.0.1'])
COMMON_BASE_PORT = configure('port', 43210, coerce_type=int)

if configure('security', False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rest_framework',

    'django_uwsgi',

    'events',
    'notifications',
]

# RAVEN
if configure('raven', False) and configure('raven.dsn', ''):
    import raven  # noqa

    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': configure('raven.dsn', None),
        'release': __version__,
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',

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
        'ENGINE': configure('db.name', 'django.db.backends.postgresql'),
        'HOST': configure('db.host', 'localhost'),
        'PORT': configure('db.port', 5432),

        'NAME': configure('db.database', 'msa_events'),
        'USER': configure('db.user', 'msa_events'),
        'PASSWORD': configure('db.password', 'msa_events'),

        'CONN_MAX_AGE': int(configure('db.conn_max_age', 60)),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': configure('caches.memcached.location', '127.0.0.1:11211'),
        'KEY_PREFIX': configure('caches.memcached.key_prefix', 'msa:events:'),
    },
}

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.abspath(os.path.join(ROOT_PATH, 'locale')),
)

LANGUAGES = (
    ('en', 'en'),
    ('ru', 'ru'),
)

# BATTERIES
# =========

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('events.permissions.ValidApiKeyOrDenied',),
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'URL_FORMAT_OVERRIDE': None,  # don't use 'format' as url argument
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('url_filter.integrations.drf.DjangoFilterBackend',)
}

if DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': ('events.permissions.ValidApiKeyOrSuperuserOrDenied',),
        'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication',),
        'URL_FORMAT_OVERRIDE': None,  # don't use 'format' as url argument
        'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
        'PAGE_SIZE': 10,
        'DEFAULT_FILTER_BACKENDS': ('url_filter.integrations.drf.DjangoFilterBackend',)
    }


# UWSGI
UWSGI_STATIC_SAFE = configure('uwsgi.static_safe', False)


# REDEFINE
from .local_settings import *  # noqa
