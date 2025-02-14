from django.apps import AppConfig


class SwishCoinConfig(AppConfig):  # ✅ Ensure this class name matches settings.py
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'swishcoin'

    def ready(self):
        import swishcoin.signals  # ✅ Ensure signals are loaded
