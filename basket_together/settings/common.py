
import os
from os.path import abspath, dirname

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = abspath(dirname(dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gh67^0opf#&o(tg1^h*u%w*-6=k-89236=h+%_gd0q(xfm0!oz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PROJECT_FOLDER = os.getcwd()

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    # 'rest_auth',
    # 'allauth',
    # 'allauth.account',
    # 'rest_auth.registration',
    # 'custom_user',
    'recruit',
    'accounts',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    )
}

#############################  AUTH  ###################################

# AUTH_USER_MODEL = 'custom_user.CustomUser'

# AUTHENTICATION_BACKENDS = ('custom_user.backends.CustomUserAuth',)

########################################################################


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'recruit.middleware.JSONMiddleware',
]

ROOT_URLCONF = 'basket_together.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'basket_together.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../database/db.sqlite3'),
        # 'NAME': os.path.join(PROJECT_FOLDER, 'development.db'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# prefix of request url
STATIC_URL = '/static/'

# being searched dirs
'''
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'basket_together', 'static'),
]
'''

# collectstatic dir
STATIC_ROOT = os.path.join(BASE_DIR, '../../static')

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')
MEDIA_URL = '/media/'
