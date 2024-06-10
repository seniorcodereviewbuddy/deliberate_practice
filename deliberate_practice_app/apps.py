"""Package declaring all the App specific settings."""

from django.apps import AppConfig


class DeliberatePracticeAppConfig(AppConfig):
    """DeliberatePracticeAppConfig is the config object App settings.

    All configuration values specific to this application should be
    located here.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "deliberate_practice_app"
