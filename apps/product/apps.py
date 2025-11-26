from django.apps import AppConfig

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.product'

    def ready(self):
        # Import signals to connect signal handlers when app is ready
        import apps.product.signals