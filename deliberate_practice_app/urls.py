"""URL configuration for deliberate_practice_app app.

The `urlpatterns` list routes URLs to views. For more information please
see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.urls import path

from .views import main, practice

app_name = "deliberate_practice_app"  # pylint: disable=invalid-name
urlpatterns = [
    path("", main.index, name="index"),
    path("practice-results", practice.practice_results, name="practice-results"),
    path(
        "start-practice-session",
        practice.start_practice_session,
        name="start-practice-session",
    ),
]
