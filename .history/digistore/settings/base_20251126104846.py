import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# --------------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------------
# Define the base directory for the project (three levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --------------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------------
# Load environment variables from a .env file for sensitive data like SECRET_KEY
load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-for-dev')  # Default value for development

# --------------------------------------------------------
# INTERNATIONALIZATION & TIMEZONE
# --------------------------------------------------------
LANGUAGE_CODE = 'fa'                 # Set Persian (Farsi) as the default language
TIME_ZONE = 'Asia/Tehran'            # Set Tehran timezone
USE_I18N = True                       # Enable Django’s translation system
USE_L10N = True                       # Format dates, numbers, and calendars according to locale
USE_TZ = True                         # Enable timezone-aware datetimes

# --------------------------------------------------------
# INSTALLED APPS
# --------------------------------------------------------
# List of all Django and custom apps used in the project
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Provides human-friendly formatting for numbers/dates

    # Third-party apps
    'crispy_forms',  # For better form rendering with Bootstrap

    # Custom project apps
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

# --------------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------------
# Middleware are hooks that process requests/responses globally
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # Security improvements like HTTPS redirects
    'django.contrib.sessions.middleware.SessionMiddleware',  # Handles user sessions
    'django.middleware.common.CommonMiddleware',             # Common HTTP features (e.g., 404 handling)
    'django.middleware.csrf.CsrfViewMiddleware',             # Protect against Cross-Site Request Forgery
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Handles user authentication
    'django.contrib.messages.middleware.MessageMiddleware',   # Enables flash messaging
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Prevents clickjacking attacks
]

# --------------------------------------------------------
# URL CONFIGURATION
# --------------------------------------------------------
ROOT_URLCONF = 'digistore.urls'  # Entry point for URL routing

# --------------------------------------------------------
# TEMPLATES
# --------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,                  # Look for templates in each app's 'templates' folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Adds debug info to templates
                'django.template.context_processors.request', # Adds 'request' object to templates
                'django.contrib.auth.context_processors.auth', # Adds 'user' object to templates
                'django.contrib.messages.context_processors.messages', # Adds flash messages
                'apps.account.context_processors.global_context', # Custom global context
            ],
        },
    },
]

# --------------------------------------------------------
# WSGI & ASGI APPLICATIONS
# --------------------------------------------------------
# Entry points for WSGI/ASGI servers
WSGI_APPLICATION = 'digistore.wsgi.application'
ASGI_APPLICATION = 'digistore.asgi.application'

# --------------------------------------------------------
# STATIC & MEDIA FILES
# --------------------------------------------------------
STATIC_URL = '/static/'                       # URL prefix for static files
STATICFILES_DIRS = [BASE_DIR / 'static']      # Directories to look for static files
MEDIA_URL = '/media/'                         # URL prefix for uploaded media files
MEDIA_ROOT = BASE_DIR / 'media'               # Filesystem location for media files

# --------------------------------------------------------
# CUSTOM USER MODEL
# --------------------------------------------------------
AUTH_USER_MODEL = 'user.User'  # Use a custom User model instead of default Django user

# --------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# --------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default auto-increment field for models

# --------------------------------------------------------
# CRISPY FORMS
# --------------------------------------------------------
CRISPY_TEMPLATE_PACK = 'bootstrap4'  # Use Bootstrap 4 styling for forms

# --------------------------------------------------------
# LOGIN/LOGOUT REDIRECTION
# --------------------------------------------------------
LOGIN_URL = '/account/signin/'          # URL to redirect users for login
LOGIN_REDIRECT_URL = '/'                # Redirect after successful login
LOGOUT_REDIRECT_URL = '/'               # Redirect after logout

# --------------------------------------------------------
# LOGGING
# --------------------------------------------------------
# Simple console logging for development/debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class':'logging.StreamHandler',  # Output logs to console
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Log messages of INFO level and above
    },
}