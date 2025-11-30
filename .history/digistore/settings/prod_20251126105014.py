from .base import *  # Import all base settings
import os

# --------------------------------------------------------
# DEBUG MODE
# --------------------------------------------------------
# Disable debug mode in production for security
DEBUG = False

# --------------------------------------------------------
# ALLOWED HOSTS
# --------------------------------------------------------
# Define allowed hosts for the production server via environment variable
# Example: 'example.com,www.example.com'
# If not set, defaults to an empty list (no hosts allowed)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# --------------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------------
# PostgreSQL production database settings, all loaded from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL backend
        'NAME': os.getenv('POSTGRES_DB'),           # Production database name
        'USER': os.getenv('POSTGRES_USER'),         # Production database user
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'), # Production database password
        'HOST': os.getenv('POSTGRES_HOST'),         # Database host
        'PORT': os.getenv('POSTGRES_PORT'),         # Database port
    }
}