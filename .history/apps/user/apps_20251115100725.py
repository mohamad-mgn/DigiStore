from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'

    def ready(self):
        # ثبت سیگنال‌ها هنگام آماده شدن اپ
        import apps.user.signals  # noqa