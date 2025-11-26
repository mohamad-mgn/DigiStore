from django.apps import AppConfig

# --------------------------------------------------------
# Cart App Configuration
# --------------------------------------------------------
class CartConfig(AppConfig):
    """
    Configuration class for the 'cart' app.
    Sets default auto field type and app label.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'