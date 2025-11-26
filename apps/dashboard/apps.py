from django.apps import AppConfig

# --------------------------------------------------------
# Dashboard App Configuration
# --------------------------------------------------------
class DashboardConfig(AppConfig):
    """
    Configuration class for the 'dashboard' app.
    Sets default auto field type and app label.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"