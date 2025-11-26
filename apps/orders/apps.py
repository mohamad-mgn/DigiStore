from django.apps import AppConfig

# --------------------------------------------------------
# Orders App Configuration
# --------------------------------------------------------
class OrdersConfig(AppConfig):
    """
    Configuration class for the 'orders' app.
    Sets default auto field type and app label.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'

    # Uncomment the ready method if you need to register signals
    # def ready(self):
    #     import apps.orders.signals