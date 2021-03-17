from pathlib import Path
from datetime import timedelta
from os import path, getenv

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = getenv('OYUSEC_SECRET', 'CHANGEMEINPRODUCTION')

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party packages
    'rest_framework',
    'corsheaders',

    # Custom apps
    'apps.core.apps.CoreConfig',
    'apps.ctf.apps.CtfConfig',
    'apps.competition',
    'apps.api',
]

MIDDLEWARE = [
    # Cors config
    'corsheaders.middleware.CorsMiddleware',
    # Builtin configs
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': getenv('POSTGRES_DB_NAME', None),
            'USER': getenv('POSTGRES_DB_USERNAME', None),
            'PASSWORD': getenv('POSTGRES_DB_PASSWORD', None),
            'HOST': getenv('POSTGRES_DB_HOST', None),
            'PORT': getenv('POSTGRES_DB_PORT', None),
        }
    }

CORS_ALLOWED_ORIGINS = [
    "http://oyusec.github.io",
    "http://oyusec.ml",
    "http://localhost:3000",
    "http://localhost:5000"
]

# AUTHENTICATION

SIMPLE_JWT = {
    'USER_ID_FIELD': 'uuid',
}


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

AUTH_USER_MODEL = 'core.BaseUser'


# REST FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# MISC

LANGUAGE_CODE = 'mn'

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')
# Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
