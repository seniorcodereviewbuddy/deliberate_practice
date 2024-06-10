"""Module of the classes related to practice results."""

from django.db import models

from . import routine

POSSIBLE_SCORES = [
    (0, "I wasn’t successful"),
    (1, "I was ~25% successful"),
    (2, "I was ~50% successful"),
    (3, "I was ~75% successful"),
    (4, "I executed the task flawlessly"),
]


class PracticeSet(models.Model):
    """PracticeSet is an an Activity that was practiced and scored."""

    activity_id = models.ForeignKey(routine.Activity, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=POSSIBLE_SCORES)
    practice_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"PracticeSet({self.activity_id=}, {self.score=}, {self.practice_time=})"
