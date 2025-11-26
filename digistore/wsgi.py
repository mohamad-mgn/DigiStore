import os
from django.core.wsgi import get_wsgi_application

# --------------------------------------------------------
# DJANGO SETTINGS MODULE
# --------------------------------------------------------
# Set the default Django settings module for the WSGI application.
# Here it points to the development settings.
# In production, this would typically be 'digistore.settings.prod'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digistore.settings.dev')

# --------------------------------------------------------
# WSGI APPLICATION
# --------------------------------------------------------
# Get the WSGI application used by Django's development server
# and by any WSGI-compatible web servers (e.g., Gunicorn, uWSGI).
application = get_wsgi_application()