"""Module of all the main views, like indices."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Django View to for the Deliberate Practice Index.

    This is the main landing page is where users can select what they'd
    like to do.
    """
    return render(request, "deliberate_practice_app/index.html", {})
