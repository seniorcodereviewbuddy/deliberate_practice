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
    path("practice-results", practice.practice_results, name="practice_results"),
    path(
        "start-practice-session",
        practice.start_practice_session,
        name="start_practice_session",
    ),
    path(
        "end-practice-session/<int:practice_session_id>",
        practice.end_practice_session,
        name="end_practice_session",
    ),
    path(
        "practice-session/<int:practice_session_id>",
        practice.practice_session,
        name="practice_session",
    ),
    path(
        "practice-session/<int:practice_session_id>/practice-set",
        practice.add_practice_set,
        name="add_practice_set",
    ),
]
