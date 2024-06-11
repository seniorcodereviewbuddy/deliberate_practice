from django.utils import timezone

from . import results, routine


def test_practice_session_str() -> None:
    now = timezone.now()
    practice_session = results.PracticeSession(start_time=now, end_time=now)
    expected_str = (
        f"PracticeSession(self.id=None, self.start_time={repr(now)}, "
        f"self.end_time={repr(now)})"
    )
    assert str(practice_session) == expected_str


def test_practice_session_active_state() -> None:
    practice_session = results.PracticeSession()
    assert practice_session.state() == results.PracticeSession.State.ACTIVE


def test_practice_session_finished_state() -> None:
    practice_session = results.PracticeSession(end_time=timezone.now())
    assert practice_session.state() == results.PracticeSession.State.FINISHED


def test_practice_set_str() -> None:
    activity = routine.Activity()
    practice_session = results.PracticeSession()
    score = 1
    practice_time = timezone.now()

    practice_set = results.PracticeSet(
        practice_session=practice_session,
        activity=activity,
        score=score,
        practice_time=practice_time,
    )
    expected_str = (
        f"PracticeSet(self.practice_session={practice_session}, "
        f"self.activity={activity}, self.score={score}, "
        f"self.practice_time={repr(practice_time)})"
    )
    assert str(practice_set) == expected_str
