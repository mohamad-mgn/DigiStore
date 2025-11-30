import os
from django.core.asgi import get_asgi_application

# --------------------------------------------------------
# DJANGO SETTINGS MODULE
# --------------------------------------------------------
# Set the default Django settings module for the ASGI application.
# Here it points to the development settings.
# In production, this would typically be 'digistore.settings.prod'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digistore.settings.dev')

# --------------------------------------------------------
# ASGI APPLICATION
# --------------------------------------------------------
# Get the ASGI application used by Django's ASGI servers.
# ASGI supports asynchronous protocols like WebSockets in addition to HTTP.
application = get_asgi_application()