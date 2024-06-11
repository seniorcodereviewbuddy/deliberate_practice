from django import test
from django.urls import reverse
from pytest_django.asserts import assertRedirects


def test_start_practice_session(client: test.Client) -> None:
    response = client.post(reverse("deliberate_practice_app:start_practice_session"))
    assertRedirects(response, "/practice/")


def test_end_practice_session(client: test.Client) -> None:
    response = client.post(
        reverse(
            "deliberate_practice_app:end_practice_session",
            kwargs={"practice_session_id": 0},
        )
    )
    assertRedirects(response, "/practice/")


def test_practice_session(client: test.Client) -> None:
    response = client.get(
        reverse(
            "deliberate_practice_app:practice_session",
            kwargs={"practice_session_id": 0},
        )
    )
    assertRedirects(response, "/practice/")


def test_add_practice_set(client: test.Client) -> None:
    response = client.post(
        reverse(
            "deliberate_practice_app:add_practice_set",
            kwargs={"practice_session_id": 0},
        )
    )
    assertRedirects(response, "/practice/")


def test_practice_results(client: test.Client) -> None:
    response = client.get(reverse("deliberate_practice_app:practice_results"))
    assert response.status_code == 200
