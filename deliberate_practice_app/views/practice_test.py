from django import test
from django.urls import reverse
from pytest_django.asserts import assertRedirects


def test_start_practice_session(client: test.Client) -> None:
    response = client.get(reverse("deliberate_practice_app:start-practice-session"))
    assertRedirects(response, "/practice/")


def test_practice_results(client: test.Client) -> None:
    response = client.get(reverse("deliberate_practice_app:practice-results"))
    assert response.status_code == 200
