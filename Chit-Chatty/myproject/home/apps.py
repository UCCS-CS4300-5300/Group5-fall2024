from django.apps import AppConfig
import os


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        # Checks if the current process is the main one. 
        # If so, run the scheduler
        if os.environ.get('RUN_MAIN', None) == 'true':
            from .scheduler import startScheduler
            startScheduler()
