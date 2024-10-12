from django.apps import AppConfig


class MediaPlatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_platform'

    def ready(self) -> None:
        from . import signals
