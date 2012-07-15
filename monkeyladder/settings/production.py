from common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Garbutt', 'jagarbut@gmail.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

TIME_ZONE = 'America/Toronto'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jagarbut',
        'USER': 'jagarbut',
        'PASSWORD': 'monkeyladderadmin',
        'HOST': '',
        'PORT': '',
    }
}

WSGI_APPLICATION = 'monkeyladder.wsgi.application'
