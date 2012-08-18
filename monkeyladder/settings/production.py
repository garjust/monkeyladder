from common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Garbutt', 'jagarbut@gmail.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

MEDIA_ROOT = ''
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/jagarbut/webapps/django_static'
STATIC_URL = 'http://monkeyladder.ca/static/'

STATICFILES_DIRS = (
    '/home/jagarbut/webapps/django/monkeyladder/static',
)

TEMPLATE_DIRS = (
    '/home/jagarbut/webapps/django/monkeyladder/templates',
)

TIME_ZONE = 'America/Toronto'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jagarbut_ml_1_1_0',
        'USER': 'jagarbut_ml_1_1_0',
        'PASSWORD': 'monkeyladderadmin',
        'HOST': '',
        'PORT': '',
    }
}
