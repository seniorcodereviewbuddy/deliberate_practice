import typing
import urllib

import pytest
from django import test
from django.urls import reverse
from django.utils import timezone
from pytest_django.asserts import assertContains, assertRedirects

from deliberate_practice_app.models import results, routine

if typing.TYPE_CHECKING:
    # This type doesn't exist at runtime, so only import when doing
    # type checking.
    # For more details, see:
    # https://stackoverflow.com/questions/76858314/how-to-properly-type-client-post-response-in-django-test
    from django.test.client import (
        _MonkeyPatchedWSGIResponse as TestHttpResponse,  # pylint: disable=import-outside-toplevel
    )


LOW_SCORE = 0
MIDPOINT_SCORE = 3


def asset_status(response: "TestHttpResponse", expected_status: int) -> None:
    assert response.status_code == expected_status, (
        f"Unexpected status code returned. "
        f"Request content:\n\t{response.content.decode()}"
    )


@pytest.fixture(name="activity")
def fixture_activity() -> routine.Activity:
    return routine.Activity.objects.create(description="practice_activity")


def create_multiple_activities(num_to_create: int) -> list[routine.Activity]:
    return [
        routine.Activity.objects.create(description=f"practice_activity_{x}")
        for x in range(num_to_create)
    ]


@pytest.mark.django_db
def test_practice_session_invalid_session_given(client: test.Client) -> None:
    response = client.get(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": 1},
        )
    )
    asset_status(response, 404)


@pytest.mark.django_db
def test_practice_session_valid_session_given_session_active(
    client: test.Client,
) -> None:
    practice_session = results.PracticeSession.objects.create()
    assert practice_session.state() == results.PracticeSession.State.ACTIVE

    response = client.get(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session.id},
        )
    )
    asset_status(response, 200)
    assertContains(
        response, "<input type='submit' value='End Practice Session' />", html=True
    )


@pytest.mark.django_db
def test_practice_session_valid_session_given_session_finished(
    client: test.Client,
) -> None:
    practice_session = results.PracticeSession.objects.create(end_time=timezone.now())
    assert practice_session.state() == results.PracticeSession.State.FINISHED

    response = client.get(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session.id},
        )
    )
    asset_status(response, 200)
    assertContains(
        response, "<input type='submit' value='Start Practice Session' />", html=True
    )


@pytest.mark.django_db
@pytest.mark.usefixtures("activity")
def test_practice_session_try_pick_activity_wrong_type(client: test.Client) -> None:
    practice_session = results.PracticeSession.objects.create()

    response = client.get(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session.id},
        ),
        data={"activity_id": "activity_id"},
    )
    asset_status(response, 400)


@pytest.mark.django_db
def test_practice_session_try_pick_activity_that_does_not_exist(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session = results.PracticeSession.objects.create()

    response = client.get(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session.id},
        ),
        data={"activity_id": activity.id + 1},
    )
    asset_status(response, 404)


@pytest.mark.django_db
def test_practice_session_pick_activity(client: test.Client) -> None:
    practice_session = results.PracticeSession.objects.create()
    activities = create_multiple_activities(100)
    selected_activity_id = activities[0].id

    response = client.get(
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session.id},
        ),
        data={"activity_id": selected_activity_id},
    )
    asset_status(response, 200)
    print(response.content.decode())
    assertContains(
        response,
        f'<input type="hidden" name="activity_id" value="{selected_activity_id}">',
        html=True,
    )


def start_new_practice_session(
    client: test.Client, expected_result_substr: typing.Optional[str] = None
) -> int:
    response = client.post(
        reverse("deliberate_practice_app:start_practice_session"), follow=True
    )
    practice_session_id = int(response.context["practice_session_id"])
    assertRedirects(
        response,
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        ),
    )

    if expected_result_substr:
        assertContains(response, expected_result_substr)

    return practice_session_id


def close_practice_session(client: test.Client, practice_session_id: int) -> None:
    response = client.post(
        reverse(
            "deliberate_practice_app:end_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        )
    )
    assertRedirects(
        response,
        reverse(
            "deliberate_practice_app:show_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        ),
    )


@pytest.mark.django_db
def test_start_practice_session_with_no_activities(client: test.Client) -> None:
    assert results.PracticeSession.objects.count() == 0

    practice_session_id = start_new_practice_session(
        client, expected_result_substr="No Activities to Practice."
    )

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.all()[0]
    assert practice_session.id == practice_session_id


@pytest.mark.django_db
def test_start_practice_session(
    client: test.Client, activity: routine.Activity
) -> None:
    assert results.PracticeSession.objects.count() == 0

    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.all()[0]
    assert practice_session.id == practice_session_id


@pytest.mark.django_db
def test_start_practice_session_and_end_right_away(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.get(pk=practice_session_id)
    assert practice_session
    assert practice_session.state() == results.PracticeSession.State.ACTIVE

    close_practice_session(client, practice_session_id)

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.get(pk=practice_session_id)
    assert practice_session
    assert practice_session.state() == results.PracticeSession.State.FINISHED


@pytest.mark.django_db
def test_try_to_end_an_ended_practice_session(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    close_practice_session(client, practice_session_id)

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.get(pk=practice_session_id)
    assert practice_session
    assert practice_session.state() == results.PracticeSession.State.FINISHED

    response = client.post(
        reverse(
            "deliberate_practice_app:end_practice_session",
            kwargs={"practice_session_id": practice_session_id},
        )
    )
    assert response.status_code == 409


@pytest.mark.django_db
def test_try_to_end_non_existent_practice_session(client: test.Client) -> None:
    response = client.post(
        reverse(
            "deliberate_practice_app:end_practice_session",
            kwargs={"practice_session_id": 1},
        )
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_try_to_add_practice_set_to_non_existent_practice_session(
    client: test.Client, activity: routine.Activity
) -> None:
    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": 1},
        ),
        {"activity_id": activity.id, "score": MIDPOINT_SCORE},
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_try_to_add_practice_set_to_finished_practice_session(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    close_practice_session(client, practice_session_id)

    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": practice_session_id},
        ),
        {"activity_id": activity.id, "score": MIDPOINT_SCORE},
    )
    asset_status(response, 409)


@pytest.mark.django_db
def test_try_to_add_practice_set_without_activity_id(client: test.Client) -> None:
    practice_session_id = start_new_practice_session(client)

    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": practice_session_id},
        ),
        {"score": 5},
    )
    asset_status(response, 400)


@pytest.mark.django_db
def test_try_to_add_practice_set_without_score(client: test.Client) -> None:
    practice_session_id = start_new_practice_session(client)
    # Create a lot of activities to ensure we persist the selected
    # activity when going back to the page after missing the score.
    activities = create_multiple_activities(100)
    selected_activity_id = activities[0].id

    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": practice_session_id},
        ),
        data={"activity_id": selected_activity_id},
        follow=True,
    )

    expected_url_base = reverse(
        "deliberate_practice_app:show_practice_session",
        kwargs={"practice_session_id": practice_session_id},
    )
    error_msg = "You didn't select a score"
    data = {
        "error_message": error_msg,
        "activity_id": selected_activity_id,
    }
    encoded_data = urllib.parse.urlencode(data)
    expected_url = f"{expected_url_base}?{encoded_data}"

    assertRedirects(response, expected_url)

    # Ensure the error mesage was added to the page.
    assertContains(response, error_msg, html=True)

    # Make sure the Activity to practice didn't change.
    assertContains(
        response,
        f'<input type="hidden" name="activity_id" value="{selected_activity_id}">',
        html=True,
    )


@pytest.mark.django_db
def test_try_to_add_practice_set_with_invalid_activity_id(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": practice_session_id},
        ),
        {"activity_id": activity.id + 1, "score": MIDPOINT_SCORE},
    )
    asset_status(response, 404)


@pytest.mark.django_db
def test_try_to_add_practice_set_with_invalid_activity_id_type(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": practice_session_id},
        ),
        {"activity_id": "activity_id", "score": MIDPOINT_SCORE},
    )
    asset_status(response, 400)


@pytest.mark.django_db
def test_try_to_add_practice_set_with_invalid_score_type(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": practice_session_id},
        ),
        {"activity_id": activity.id, "score": "fake_score"},
    )

    asset_status(response, 400)


@pytest.mark.django_db
def test_start_practice_and_practice_several_times_same_score(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    practice_count = 5
    for _ in range(practice_count):
        response = client.post(
            reverse(
                "deliberate_practice_app:add_practice_set",
                kwargs={"practice_session_id": practice_session_id},
            ),
            {"activity_id": activity.id, "score": MIDPOINT_SCORE},
        )
        asset_status(response, 302)

    close_practice_session(client, practice_session_id)

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.get(id=practice_session_id)
    assert practice_session
    assert practice_session.practice_sets.count() == practice_count
    for practice_set in practice_session.practice_sets.all():
        assert practice_set.score == MIDPOINT_SCORE


@pytest.mark.django_db
def test_start_practice_and_practice_several_times_different_scores(
    client: test.Client, activity: routine.Activity
) -> None:
    practice_session_id = start_new_practice_session(
        client, expected_result_substr=f"Please practice: {activity.description}"
    )

    scores = [LOW_SCORE] * 3 + [MIDPOINT_SCORE] * 3
    for score in scores:
        response = client.post(
            reverse(
                "deliberate_practice_app:add_practice_set",
                kwargs={"practice_session_id": practice_session_id},
            ),
            {"activity_id": activity.id, "score": score},
        )
        asset_status(response, 302)

    close_practice_session(client, practice_session_id)

    assert results.PracticeSession.objects.count() == 1
    practice_session = results.PracticeSession.objects.get(id=practice_session_id)
    assert practice_session
    assert practice_session.practice_sets.count() == len(scores)
    for index, practice_set in enumerate(
        practice_session.practice_sets.all().order_by("practice_time")
    ):
        assert practice_set.score == scores[index]


def test_practice_results(client: test.Client) -> None:
    response = client.get(reverse("deliberate_practice_app:practice_results"))
    assert response.status_code == 200
