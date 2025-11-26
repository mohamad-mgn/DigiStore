from django.apps import AppConfig

# --------------------------------------------------------
# Home App Configuration
# --------------------------------------------------------
class HomeConfig(AppConfig):
    """
    Configuration class for the 'home' app.
    Sets default auto field type and app label.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"