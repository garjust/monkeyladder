import os

VERSION_NUMBER = "0.5.0"

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", "..")).replace("\\", "/")

ROOT_URLCONF = 'monkeyladder.urls'
LOGIN_REDIRECT_URL = '/home'
LOGIN_URL = '/accounts/login/'

AUTH_PROFILE_MODULE = 'core.UserProfile'

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    '{}/static'.format(PROJECT_ROOT),
)

TEMPLATE_DIRS = (
    '{}/templates'.format(PROJECT_ROOT),
)

SECRET_KEY = 'y&amp;n8ww2nrpv9yemnvd9-y+v=5(n_t2q+m3+*19b#+qnfge*ygc'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.humanize',
    'accounts',
    'core',
    'datedmodels',
    'leaderboard',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'monkeyladder.context_processors.version_number',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(module)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'monkeyladder': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        }
    }
}
