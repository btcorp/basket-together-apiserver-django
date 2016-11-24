import os
from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'basket_together',
        'USER': 'postgres',
        'PASSWORD': '1234qwer',
        'HOST': 'localhost',
    }
}
