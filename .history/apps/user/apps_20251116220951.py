from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user"
    verbose_name = "مدیریت کاربران"

    def ready(self):
        # در اینجا سیگنال‌ها را importe می‌کنیم تا در زمان راه‌اندازی پروژه فعال شوند
        import apps.user.signals  # noqa: F401