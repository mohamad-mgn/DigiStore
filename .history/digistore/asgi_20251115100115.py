import os
from django.core.asgi import get_asgi_application

# تنظیمات پیش‌فرض به dev اشاره دارند؛ در production این را تغییر بده
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digistore.settings.dev')
application = get_asgi_application()