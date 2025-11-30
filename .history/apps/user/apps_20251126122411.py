from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # Default primary key type for models
    name = "apps.user"  # App name
    verbose_name = "مدیریت کاربران"  # Display name for admin

    def ready(self):
        # Import signals when app is ready
        import apps.user.signals