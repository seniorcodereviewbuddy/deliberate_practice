"""Module of all the views relating to practices."""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST


@require_POST
def start_practice_session(_request: HttpRequest) -> HttpResponse:
    """Django view for starting a practice session.

    Currently this just redirects to the main index.
    """
    return HttpResponseRedirect(reverse("deliberate_practice_app:index"))


@require_POST
def end_practice_session(
    request: HttpRequest, practice_session_id: int
) -> HttpResponse:
    """Django view for starting a ending session.

    Currently this just redirects to the main index.
    """
    del practice_session_id
    return HttpResponseRedirect(reverse("deliberate_practice_app:index"))


@require_GET
def practice_session(request: HttpRequest, practice_session_id: int) -> HttpResponse:
    """Django view for showing a practice session.

    If the session is active, the user will have the option of adding
    new practice sets to it.

    Currently this just redirects to the main index.
    """
    del practice_session_id
    return HttpResponseRedirect(reverse("deliberate_practice_app:index"))


@require_POST
def add_practice_set(request: HttpRequest, practice_session_id: int) -> HttpResponse:
    """Django view for adding a practice set.

    Currently this just redirects to the main index.
    """
    del practice_session_id
    return HttpResponseRedirect(reverse("deliberate_practice_app:index"))


def practice_results(request: HttpRequest) -> HttpResponse:
    """Django view for showing the practice results."""
    return render(request, "deliberate_practice_app/practice_results.html", {})
