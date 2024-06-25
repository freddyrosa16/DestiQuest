from django.apps import AppConfig


class DestiDockerConfig(AppConfig):
    name = 'destidocker'

    def ready(self):
        import destidocker.signals
