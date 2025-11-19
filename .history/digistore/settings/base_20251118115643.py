"""
تنظیمات پایه — مشترک بین dev و prod.
تمام مقادیر حساس باید در .env قرار بگیرند.
"""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# BASE_DIR ==> ریشه پروژه (جایی که manage.py هست)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# بارگذاری اتوماتیک فایل .env (اگر وجود داشته باشد)
load_dotenv(find_dotenv())

# مقدار کلید مخفی (از .env خوانده می‌شود)
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-for-dev')

# زبان و timezone - تنظیم به فارسی و ساعت تهران
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# اپ‌ها
INSTALLED_APPS = [
    # اپ‌های جنگو
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.hmanize',
    
    # third-party
    'crispy_forms',

    # اپ‌های محلی (همه داخل پوشه apps/)
    'apps.account',
    'apps.user',
    'apps.home',
    'apps.store',
    'apps.product',
    'apps.cart',
    'apps.orders',
    'apps.payments',
    'apps.dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'digistore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # فولدر templates در ریشه پروژه
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.account.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'digistore.wsgi.application'
ASGI_APPLICATION = 'digistore.asgi.application'

# فایل‌های استاتیک و رسانه
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# مدل کاربر سفارشی
AUTH_USER_MODEL = 'user.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# کریسپی فرم پک
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# بررسی ارسال SMS (local)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'class':'logging.StreamHandler',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}