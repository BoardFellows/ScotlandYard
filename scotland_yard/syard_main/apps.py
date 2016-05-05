from django.apps import AppConfig


class SyardMainConfig(AppConfig):
    """Config Syard Main."""

    name = 'syard_main'

    def ready(self):

        """code to run when app is ready."""
        from syard_main import handlers
