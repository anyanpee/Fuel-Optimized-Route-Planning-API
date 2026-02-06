import os
from pathlib import Path
from decouple import Config, RepositoryEnv
from dotenv import load_dotenv

load_dotenv() 

# Load .env from custom 'config/' folder
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, 'config', '.env')
config = Config(repository=RepositoryEnv(env_path))

# Load Environment Variables
try:
    ORS_API_KEY = config('ORS_API_KEY')
    print("[+] ORS_API_KEY loaded:", ORS_API_KEY[:5], "...")
except Exception as e:
    print("[-] Failed to load ORS_API_KEY:", e)
    ORS_API_KEY = ''

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-change-me-now')
DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='*').split(',')

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',         # ✅ Added DRF
    'fuel',
    'datalake',
    'routes',
]

# Middleware Stack
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Config
ROOT_URLCONF = 'config.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# SQLite (Local DB)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# Timezone and Language
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'