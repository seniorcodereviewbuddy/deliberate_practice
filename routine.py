"""Module of the classes related to a practice routine."""

import pathlib
import random


class InvalidActivitiesFileError(Exception):
    """There was an issue with the activities file."""


class Activities:
    """Activities is the root of all practice routine information.

    Activities is responsible for managing all the practice activities,
    including deciding what activity should be done next.
    """

    def __init__(self, activity_file: pathlib.Path):
        """Creates an Activities instance from the specified file."""
        self.activities = []
        try:
            with open(activity_file, encoding="utf-8") as f:
                for line in f.readlines():
                    self.activities.append(Activity(line.strip()))
        except FileNotFoundError as e:
            raise InvalidActivitiesFileError(
                "No Activity file found, please create an activity file. "
            ) from e

        if not self.activities:
            raise InvalidActivitiesFileError(
                "No activities found in activity file. Please add activities."
            )

    def get_activity_descriptions(self) -> list[str]:
        """Returns all the Activity descriptions, in key order."""
        sorted_activities = sorted(self.activities, key=lambda x: x.get_key())
        return [x.get_description() for x in sorted_activities]

    def get_num_activities(self) -> int:
        """Returns the number of Activities in this instance."""
        return len(self.activities)

    def get_random_activity(self) -> "Activity":
        """Returns a random Activity."""
        return random.choice(self.activities)


class Activity:
    """Activity is a single practice task.

    An Activity is build block of deliberate practice. Each Activity
    represents a single pratice task that will be executed, graded
    and repeated over time until the user has reached their desired
    level of skill.
    """

    def __init__(self, description: str):
        """Creates an Activity with the given description.

        At this time, an activity is fully represented by a single
        string.
        """
        self.description = description

    def get_description(self) -> str:
        """Returns the description of this Activity.

        This should be enough information for the user to know how to
        practice it.
        """
        return self.description

    def get_key(self) -> str:
        """Returns the key for this Activity.

        Currently the key is just the description, but in the future it
        should be a unique identifier that maps to this activity and
        this activity only.
        """
        return self.get_description()
