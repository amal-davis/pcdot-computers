from django.apps import AppConfig


class PcdotappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pcdotapp'


class PcdotappConfig(AppConfig):
    name = 'pcdotapp'

    def ready(self):
        import pcdotapp.signals  # Ensure the signals are registered