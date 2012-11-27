from common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Garbutt', 'iamgarjust@gmail.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

TIME_ZONE = 'America/Toronto'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/db/monkeyladder.db' % PROJECT_ROOT,
    }
}

WSGI_APPLICATION = 'monkeyladder.wsgi.application'
