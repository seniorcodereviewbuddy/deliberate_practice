"""Module of everything related to tracking practice results."""

import datetime
import pathlib
import typing

import routine


class InvalidPracticesFileError(Exception):
    """There was an issue with the practices file."""


class Practices:
    """Practices is the holder of all completed practices."""

    def __init__(self, practices_file: pathlib.Path):
        """Creates a Practices instance from the given practices_file.

        If the practices_file doens't exist, create an empty Practices
        instance.
        """
        self.practices_file = practices_file

        self.practice_sets = []

        # If the practices file doesn't exist yet, that is ok.
        # We'll create it later when saving results.
        if not practices_file.is_file():
            print("Note: No Practices file found. Starting from an empty state")
            return

        with open(self.practices_file, encoding="utf-8") as f:
            num_practice_sets_str = f.readline()
            try:
                num_practice_sets = int(num_practice_sets_str)
            except ValueError as e:
                raise InvalidPracticesFileError(
                    "Expected an integer for number of practice sets, instead got "
                    f'"{num_practice_sets_str}"'
                ) from e

            for _ in range(num_practice_sets):
                try:
                    practice_set = PracticeSet.load_from_file_object(f)
                except PracticeSetLoadingError as e:
                    raise InvalidPracticesFileError(
                        "Failed to load practice_set"
                    ) from e
                self.practice_sets.append(practice_set)

            # Verify that there is no other content in the file.
            remaining_data = f.read(None).strip("\n")
            if remaining_data:
                raise InvalidPracticesFileError(
                    "Unexpected data remaining after load completed. Found:\n"
                    f"{remaining_data}"
                )

    def save(self) -> None:
        """Saves this Practices instance to it's practices_file.

        This Practices instance can them be reproduced by opening
        that file.
        """
        with open(self.practices_file, "w", encoding="utf-8") as f:
            f.write(f"{len(self.practice_sets)}\n")
            for practice_set in self.practice_sets:
                practice_set.save(f)

    def get_num_practice_sets(self) -> int:
        """Returns the number of PracticeSets in this instance."""
        return len(self.practice_sets)

    def add_practice_set(
        self, act: routine.Activity, score: int, date_time: datetime.datetime
    ) -> None:
        """Add a PracticeSet to this instance."""
        self.practice_sets.append(PracticeSet(act.get_key(), score, date_time))

    def get_practice_sets(self) -> list["PracticeSet"]:
        """Returns the PracticeSets contained in this instance."""
        return self.practice_sets


class PracticeSetLoadingError(Exception):
    """PracticeSet was given invalid loading data.

    This usually occurs when data is missing, or the wrong type.
    """


class PracticeSet:
    """PracticeSet is an an Activity that was practiced and scored.

    The activity_key allows a PracticeSet to link back to it's root
    activity.
    """

    def __init__(self, activity_key: str, score: int, date_time: datetime.datetime):
        """Creates a PracticeSet with the given values."""
        self.activity_key = activity_key
        self.score = score
        self.date_time = date_time

    @classmethod
    def load_from_file_object(cls, f: typing.TextIO) -> "PracticeSet":
        """Loads a PracticeSet from the given Text I/O stream.

        Raises:
            PracticeSetLoadingError: If the IO buffer has a malformed
                PracticeSet.
        """
        activity_key = f.readline().rstrip("\n")
        if not activity_key:
            raise PracticeSetLoadingError("No value for activity_key")

        score_str = f.readline().rstrip("\n")
        if not score_str:
            raise PracticeSetLoadingError("No value for score")
        try:
            score = int(score_str)
        except ValueError as e:
            raise PracticeSetLoadingError(
                f'score wasn\'t an integer, got "{score_str}"'
            ) from e

        date_time_str = f.readline().rstrip("\n")
        if not date_time_str:
            raise PracticeSetLoadingError("No value for date_time")
        try:
            date_time = datetime.datetime.fromisoformat(date_time_str)
        except ValueError as e:
            raise PracticeSetLoadingError(
                f'datetime wasn\'t in iso format, got "{date_time_str}"'
            ) from e

        return PracticeSet(activity_key, score, date_time)

    def __repr__(self) -> str:
        return f"PracticeSet({self.activity_key=}, {self.score=}, {self.date_time=})"

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, PracticeSet):
            return False

        return (
            self.activity_key == other.activity_key
            and self.score == other.score
            and self.date_time == other.date_time
        )

    def save(self, f: typing.TextIO) -> None:
        """Saves this PracticeSet to the given Text I/O stream.

        This output should be loaded by load_from_file_object.
        """
        f.write(f"{self.activity_key}\n{self.score}\n{self.date_time.isoformat()}\n")
