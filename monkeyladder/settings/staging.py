from common import *

DEBUG = True
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
        'NAME': 'monkeyladder-staging',
        'USER': 'monkeyladder',
        'PASSWORD': 'staging',
        'HOST': '',
        'PORT': '',
    }
}

WSGI_APPLICATION = 'monkeyladder.wsgi.application'
