from django.apps import AppConfig

# --------------------------------------------------------
# Account App Configuration
# --------------------------------------------------------
class AccountConfig(AppConfig):
    """
    Configuration class for the 'account' app.
    Defines default primary key type, app label, and human-readable name.
    """
    # Default field type for auto-generated primary keys
    default_auto_field = "django.db.models.BigAutoField"

    # Python path to the app
    name = "apps.account"

    # Human-readable name for the app (used in admin interface)
    verbose_name = "حساب کاربری"