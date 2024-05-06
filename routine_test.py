import pathlib

import pytest

import routine


class TestActivities:
    def test_no_activity_file(self, tmp_path: pathlib.Path) -> None:
        activity_file = pathlib.Path(tmp_path, "no_file.txt")

        with pytest.raises(routine.InvalidActivitiesFileError):
            routine.Activities(activity_file)

    def test_empty_activity_file(self, tmp_path: pathlib.Path) -> None:
        activity_file = pathlib.Path(tmp_path, "activities.txt")

        # Open the file to create an empty file.
        with open(activity_file, "w", encoding="utf-8"):
            pass

        with pytest.raises(routine.InvalidActivitiesFileError):
            routine.Activities(activity_file)

    def test_activity_file_blank_lines(self, tmp_path: pathlib.Path) -> None:
        activity_file = pathlib.Path(tmp_path, "activities.txt")

        with open(activity_file, "w", encoding="utf-8") as f:
            f.write("\n\n")

        # The blank lines aren't the error, it's that there are no
        # non-blank lines.
        with pytest.raises(routine.InvalidActivitiesFileError):
            routine.Activities(activity_file)

    def test_activity_file_one_activity(self, tmp_path: pathlib.Path) -> None:
        activity_file = pathlib.Path(tmp_path, "activities.txt")
        with open(activity_file, "w", encoding="utf-8") as f:
            f.write("activity")

        activities = routine.Activities(activity_file)
        assert activities.get_num_activities() == 1

        assert activities.get_activity_descriptions() == ["activity"]

    def test_activity_file_one_activity_with_blank_lines(
        self, tmp_path: pathlib.Path
    ) -> None:
        activity_file = pathlib.Path(tmp_path, "activities.txt")
        with open(activity_file, "w", encoding="utf-8") as f:
            f.write("\nactivity\n")

        activities = routine.Activities(activity_file)
        assert activities.get_num_activities() == 1

        assert activities.get_activity_descriptions() == ["activity"]

    def test_activity_file_many_activity(self, tmp_path: pathlib.Path) -> None:
        activity_file = pathlib.Path(tmp_path, "activities.txt")
        with open(activity_file, "w", encoding="utf-8") as f:
            f.write("activity with Whitespace\n")
            f.write("activity_1\n")
            f.write("activity_2\n")
            f.write("activity_3\n")
            f.write("activity_4\n")

        activities = routine.Activities(activity_file)
        assert activities.get_num_activities() == 5
        assert activities.get_activity_descriptions() == [
            "activity with Whitespace",
            "activity_1",
            "activity_2",
            "activity_3",
            "activity_4",
        ]

    def test_activity_file_getting_many_random_activities(
        self, tmp_path: pathlib.Path
    ) -> None:
        activity_file = pathlib.Path(tmp_path, "activities.txt")
        with open(activity_file, "w", encoding="utf-8") as f:
            f.write("activity_1\n")
            f.write("activity_2\n")
            f.write("activity_3\n")

        activities = routine.Activities(activity_file)
        assert activities.get_num_activities() == 3
        assert activities.get_activity_descriptions() == [
            "activity_1",
            "activity_2",
            "activity_3",
        ]

        # Ensure we can call random activity many more time then the
        # number of activities we have.
        for _ in range(20):
            assert activities.get_random_activity()


def test_activity_get_description() -> None:
    act = routine.Activity("content")
    assert act.get_description() == "content"


def test_activity_get_key() -> None:
    act = routine.Activity("content")
    assert act.get_key() == "content"
