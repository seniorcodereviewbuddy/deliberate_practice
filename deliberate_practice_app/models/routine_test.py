from . import routine


def test_activity_str() -> None:
    description = "short description"
    activity = routine.Activity(description=description)

    assert str(activity) == f"Activity(self.description='{description}')"
