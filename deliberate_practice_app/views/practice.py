"""Module of all the views relating to practices."""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def start_practice_session(_request: HttpRequest) -> HttpResponse:
    """Django view for starting a practice session.

    Currently this just redirects to the main index.
    """
    return HttpResponseRedirect(reverse("deliberate_practice_app:index"))


def practice_results(request: HttpRequest) -> HttpResponse:
    """Django view for showing the practice results."""
    return render(request, "deliberate_practice_app/practice_results.html", {})
