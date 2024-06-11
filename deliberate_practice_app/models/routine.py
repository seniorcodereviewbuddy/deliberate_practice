"""Module of the classes related to a practice routine."""

from django.db import models


class Activity(models.Model):
    """Activity is a single practice task.

    An Activity is build block of deliberate practice. Each Activity
    represents a single pratice task that will be executed, graded
    and repeated over time until the user has reached their desired
    level of skill.
    """

    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"Activity({self.description=})"
