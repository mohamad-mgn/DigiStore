from django.apps import AppConfig

# ========================================================
# Configuration for the Payments app
# ========================================================
class PaymentsConfig(AppConfig):
    # Default primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Full Python path to the app
    name = 'apps.payments'