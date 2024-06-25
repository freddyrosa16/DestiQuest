# destiDocker_back/apps.py

from django.apps import AppConfig


class DestiDockerConfig(AppConfig):
    name = 'destiDocker_back'

    def ready(self):
        import destiDocker_back.signals
