"""Module of all the views relating to practices."""

import random
import typing
import urllib

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from deliberate_practice_app.models import results, routine


@require_POST
def start_practice_session(request: HttpRequest) -> HttpResponse:
    """Django view for starting a practice session.

    After creating the new session, redirect to that practice sessions
    page.
    """
    practice_session = results.PracticeSession()
    practice_session.save()
    return HttpResponseRedirect(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session.id},
        )
    )


class HttpResponseConflict(HttpResponse):
    """HTTPResponse when returning status_code==409."""

    status_code = 409


@require_POST
def end_practice_session(
    request: HttpRequest, practice_session_id: int
) -> HttpResponse:
    """Django view for ending an active practice session."""
    practice_session = get_object_or_404(
        results.PracticeSession, pk=practice_session_id
    )
    if practice_session.end_time is not None:
        return HttpResponseConflict(
            content="Trying to end a practice session that is already over."
        )

    practice_session.end_time = timezone.now()
    practice_session.save()

    return HttpResponseRedirect(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        )
    )


class InvalidActivityIdError(Exception):
    """The given activity_id doesn't map to a known activity."""


class ActivityIdTypeError(InvalidActivityIdError):
    """An activity_id of the wrong type was given."""


def pick_activity(request: HttpRequest) -> typing.Optional[routine.Activity]:
    """Determine which activity the user should practice.

    If the request has specified an activity, use that one.
    Otherwise, randomly pick and activity.

    If there are no Activities in the database, return None.

    Raises:
        ActivityIdTypeError: activity_id parameter was the wrong type.
        InvalidActivityIdError: activity_id doesn't map to a known
            activity.

    """
    if "activity_id" in request.GET:
        try:
            activity_id = int(request.GET["activity_id"])
        except ValueError as e:
            raise ActivityIdTypeError(
                f"activity_id must be an integer, got "
                f'{type(request.GET["activity_id"])}'
            ) from e

        try:
            return routine.Activity.objects.get(pk=activity_id)
        except routine.Activity.DoesNotExist as e:
            raise InvalidActivityIdError(
                f"given activity_id, {activity_id}, doesn't exist"
            ) from e

    if routine.Activity.objects.count():
        return random.choice(routine.Activity.objects.all())

    return None


@require_GET
def show_practice_session(
    request: HttpRequest, practice_session_id: int
) -> HttpResponse:
    """Django view for showing a practice session.

    If the session is active, the user will have the option of adding
    new practice sets to it.
    """
    practice_session = get_object_or_404(
        results.PracticeSession, pk=practice_session_id
    )

    args = {
        "practice_session_id": practice_session_id,
        "num_practice_sets": practice_session.practice_sets.count(),
        "session_state": str(practice_session.state()),
        "scores": results.POSSIBLE_SCORES,
    }

    if "error_message" in request.GET:
        args["error_message"] = request.GET["error_message"]

    if practice_session.state() == results.PracticeSession.State.ACTIVE:
        try:
            activity = pick_activity(request)
        except ActivityIdTypeError:
            return HttpResponseBadRequest(
                "activity_id was the wrong type, should be an integer"
            )
        except InvalidActivityIdError:
            return HttpResponseNotFound(
                "activity_id pointed to an non-existent activity"
            )

        if activity:
            args["activity_id"] = activity.id
            args["activity_description"] = activity.description

    return render(request, "deliberate_practice_app/practice_session.html", args)


@require_POST
def add_practice_set(request: HttpRequest, practice_session_id: int) -> HttpResponse:
    """Django view for adding a practice set.

    If the score value is missing, we'll redirect to the practice
    session page with the same question.
    """
    practice_session = get_object_or_404(
        results.PracticeSession, pk=practice_session_id
    )

    if practice_session.end_time is not None:
        return HttpResponseConflict(
            "Unable to add a practice set to a practice session that has finished."
        )

    try:
        activity_id_raw = request.POST["activity_id"]
    except KeyError:
        return HttpResponseBadRequest("mandatory field activity_id missing")

    try:
        activity_id = int(activity_id_raw)
    except ValueError:
        return HttpResponseBadRequest(
            "activity_id was the wrong type, should be an integer"
        )

    activity = get_object_or_404(routine.Activity, pk=activity_id)

    try:
        score_raw = request.POST["score"]
    except KeyError:
        url_base = reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        )
        data = {
            "error_message": "You didn't select a score",
            "activity_id": activity_id,
        }
        encoded_data = urllib.parse.urlencode(data)
        full_url = f"{url_base}?{encoded_data}"
        return HttpResponseRedirect(full_url)

    try:
        score = int(score_raw)
    except ValueError:
        return HttpResponseBadRequest("score was the wrong type, should be an integer")

    practice_session.practice_sets.create(activity=activity, score=score)

    # Redirect to practice session page
    return HttpResponseRedirect(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        )
    )


def practice_results(request: HttpRequest) -> HttpResponse:
    """Django view for showing the practice results."""
    return render(request, "deliberate_practice_app/practice_results.html", {})
