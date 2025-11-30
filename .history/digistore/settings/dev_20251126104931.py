from .base import *  # Import all base settings
import os

# --------------------------------------------------------
# DEBUG MODE
# --------------------------------------------------------
# Enable debug mode based on environment variable (default: True for development)
DEBUG = os.getenv('DEBUG', 'True') in ['True', 'true', '1']

# --------------------------------------------------------
# ALLOWED HOSTS
# --------------------------------------------------------
# In development, allow all hosts (not recommended for production)
ALLOWED_HOSTS = ['*']

# --------------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------------
# PostgreSQL database settings, configurable via environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',           # PostgreSQL backend
        'NAME': os.getenv('POSTGRES_DB', 'digistore_db'),   # Database name
        'USER': os.getenv('POSTGRES_USER', 'digistore_user'), # Database user
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),     # Database password
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),    # Database host
        'PORT': os.getenv('POSTGRES_PORT', '5432'),         # Database port
    }
}