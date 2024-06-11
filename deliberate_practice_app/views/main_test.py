from django import test
from django.urls import reverse


def test_index(client: test.Client) -> None:
    response = client.get(reverse("deliberate_practice_app:index"))
    assert response.status_code == 200

    # Ensure expected URLs are returned on the page.
    assert (
        bytearray(
            reverse("deliberate_practice_app:start_practice_session"), response.charset
        )
        in response.content
    )
    assert (
        bytearray(reverse("deliberate_practice_app:practice_results"), response.charset)
        in response.content
    )
