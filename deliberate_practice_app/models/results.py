"""Module of the classes related to practice results."""

import enum

from django.db import models

from . import routine

POSSIBLE_SCORES = [
    (0, "I wasn’t successful"),
    (1, "I was ~25% successful"),
    (2, "I was ~50% successful"),
    (3, "I was ~75% successful"),
    (4, "I executed the task flawlessly"),
]


class PracticeSession(models.Model):
    """PracticeSession is a collection of PracticeSet."""

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

    class State(enum.Enum):
        """State of the Practice Session.

        Active session can have new PracticeSets added.
        """

        ACTIVE = 0
        FINISHED = 1

    def __str__(self) -> str:
        return f"PracticeSession({self.id=}, {self.start_time=}, {self.end_time=})"

    def state(self) -> State:
        """Returns the state of this PracticeSession.

        Mainly used to determine if more PracticeSets can
        be added or not.
        """
        if self.end_time is None:
            return PracticeSession.State.ACTIVE
        return PracticeSession.State.FINISHED


class PracticeSet(models.Model):
    """PracticeSet is an an Activity that was practiced and scored."""

    # on_delete is set to CADCASE for practice session since practice
    # set should have the same lifetime as the session they live in.
    practice_session = models.ForeignKey(
        PracticeSession, on_delete=models.CASCADE, related_name="practice_sets"
    )
    # on_delete is set to PROTECT for acitivity because once we've
    # practice an activity, we need to keep that activity around or
    # practice session would look weird with missing data.
    activity = models.ForeignKey(routine.Activity, on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(choices=POSSIBLE_SCORES)
    practice_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"PracticeSet({self.practice_session=!s}, "
            f"{self.activity=!s}, {self.score=}, {self.practice_time=})"
        )
