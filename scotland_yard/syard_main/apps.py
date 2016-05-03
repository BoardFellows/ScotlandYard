from django.apps import AppConfig


class SyardMainConfig(AppConfig):
    """Config Syard Main."""

    name = 'syard_main'

    def ready(self):
        """Import signals on ready."""
        from syard_main import signals
