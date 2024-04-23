from django.apps import AppConfig

class DynamicgeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DynamicGenerator'
    def ready(self):
        import DynamicGenerator.signals