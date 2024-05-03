import datetime
import io
import pathlib

import pytest

import results
import routine


class TestResults:
    def test_missing_practices_file(self, tmp_path: pathlib.Path) -> None:
        practices_file = pathlib.Path(tmp_path, "no_file.txt")
        practices = results.Practices(practices_file)
        assert practices.get_num_practice_sets() == 0

    def test_empty_practices_file(self, tmp_path: pathlib.Path) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")

        # Open the file to create an empty file.
        with open(practices_file, "w", encoding="utf-8"):
            pass

        # An empty file is a invalid file, since if it was saved it
        # would still have some data.
        with pytest.raises(
            results.InvalidPracticesFileError,
            match="Expected an integer for number of practice sets",
        ):
            results.Practices(practices_file)

    def test_save_and_load_empty_results(self, tmp_path: pathlib.Path) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")
        practices = results.Practices(practices_file)
        assert practices.get_num_practice_sets() == 0
        assert not practices.get_practice_sets()

        practices.save()

        new_practice = results.Practices(practices_file)
        assert new_practice.get_num_practice_sets() == 0
        assert not new_practice.get_practice_sets()

    def test_add_results_to_file_and_reload(self, tmp_path: pathlib.Path) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")
        practices = results.Practices(practices_file)
        assert practices.get_num_practice_sets() == 0

        activity = routine.Activity("activity_1")
        time = datetime.datetime.now(datetime.timezone.utc)
        practices.add_practice_set(activity, 2, time)

        assert practices.get_num_practice_sets() == 1

        expected_practice_sets = [results.PracticeSet(activity.get_key(), 2, time)]
        assert practices.get_practice_sets() == expected_practice_sets

        practices.save()

        new_results = results.Practices(practices_file)
        assert new_results.get_num_practice_sets() == 1
        assert new_results.get_practice_sets() == expected_practice_sets

    def test_add_multiple_results_to_file_and_reload(
        self, tmp_path: pathlib.Path
    ) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")
        practices = results.Practices(practices_file)
        assert practices.get_num_practice_sets() == 0

        activity_1 = routine.Activity("activity_1")
        time = datetime.datetime.now(datetime.timezone.utc)
        practices.add_practice_set(activity_1, 2, time)

        activity_2 = routine.Activity("activity_2")
        practices.add_practice_set(activity_2, 3, time)

        assert practices.get_num_practice_sets() == 2

        expected_practice_sets = [
            results.PracticeSet(activity_1.get_key(), 2, time),
            results.PracticeSet(activity_2.get_key(), 3, time),
        ]
        assert practices.get_practice_sets() == expected_practice_sets

        practices.save()

        new_results = results.Practices(practices_file)
        assert new_results.get_num_practice_sets() == 2
        assert new_results.get_practice_sets() == expected_practice_sets

    def test_multiple_load_add_results_loops(self, tmp_path: pathlib.Path) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")
        activity = routine.Activity("activity")

        for count in range(10):
            practices = results.Practices(practices_file)
            assert practices.get_num_practice_sets() == count

            time = datetime.datetime.now(datetime.timezone.utc)
            practices.add_practice_set(activity, count % 5, time)

            assert practices.get_num_practice_sets() == count + 1

            practices.save()

    def test_try_load_from_file_with_missing_sets(self, tmp_path: pathlib.Path) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")

        with open(practices_file, "w", encoding="utf-8") as f:
            f.write("2\n")
            f.write("activity_key\n5\n2024-05-02T14:28:42.439597+00:00\n")

        with pytest.raises(
            results.InvalidPracticesFileError, match="Failed to load practice_set"
        ):
            results.Practices(practices_file)

    def test_try_load_from_file_with_too_much_data(
        self, tmp_path: pathlib.Path
    ) -> None:
        practices_file = pathlib.Path(tmp_path, "practices_file.txt")

        with open(practices_file, "w", encoding="utf-8") as f:
            f.write("1\n")
            f.write("activity_key\n5\n2024-05-02T14:28:42.439597+00:00\n")
            f.write("Unexpected data")

        with pytest.raises(
            results.InvalidPracticesFileError,
            match="Unexpected data remaining after load",
        ):
            results.Practices(practices_file)


class TestPracticeSet:
    def test_equal_practice_sets(self) -> None:
        time = datetime.datetime.now(datetime.timezone.utc)
        set_1 = results.PracticeSet("key1", 2, time)
        set_2 = results.PracticeSet("key1", 2, time)
        assert set_1 == set_2

    def test_equality_unequal_activity_keys(self) -> None:
        time = datetime.datetime.now(datetime.timezone.utc)
        set_1 = results.PracticeSet("key1", 2, time)
        set_2 = results.PracticeSet("key2", 2, time)
        assert set_1 != set_2

    def test_equality_unequal_scores(self) -> None:
        time = datetime.datetime.now(datetime.timezone.utc)
        set_1 = results.PracticeSet("key1", 1, time)
        set_2 = results.PracticeSet("key1", 2, time)
        assert set_1 != set_2

    def test_equality_unequal_date_times(self) -> None:
        time = datetime.datetime.now(datetime.timezone.utc)
        set_1 = results.PracticeSet("key1", 1, time)
        set_2 = results.PracticeSet("key1", 2, time + datetime.timedelta(hours=1))
        assert set_1 != set_2

    def test_load_practice_set(self) -> None:
        time = datetime.datetime.now(datetime.timezone.utc)
        practice_set = results.PracticeSet("key1", 2, time)

        f = io.StringIO()
        practice_set.save(f)

        # Reset f to the beginning so the data can be read.
        f.seek(0)

        reload_practice_set = results.PracticeSet.load_from_file_object(f)

        assert practice_set == reload_practice_set

    def test_load_practice_set_missing_score_and_time(self) -> None:
        f = io.StringIO("activity_key\n\n\n")
        with pytest.raises(results.PracticeSetLoadingError, match="No value for score"):
            results.PracticeSet.load_from_file_object(f)

    def test_load_practice_set_missing_key_and_time(self) -> None:
        f = io.StringIO("\n2\n\n")
        with pytest.raises(
            results.PracticeSetLoadingError, match="No value for activity_key"
        ):
            results.PracticeSet.load_from_file_object(f)

    def test_load_practice_set_missing_key_and_score(self) -> None:
        f = io.StringIO("\n\n2024-05-02T14:28:42.439597+00:00\n")
        with pytest.raises(
            results.PracticeSetLoadingError, match="No value for activity_key"
        ):
            results.PracticeSet.load_from_file_object(f)

    def test_load_practice_set_missing_score(self) -> None:
        f = io.StringIO("activity_key\n\n2024-05-02T14:28:42.439597+00:00\n")
        with pytest.raises(results.PracticeSetLoadingError, match="No value for score"):
            results.PracticeSet.load_from_file_object(f)

    def test_load_practice_set_missing_date_time(self) -> None:
        f = io.StringIO("activity_key\n5\n\n")
        with pytest.raises(
            results.PracticeSetLoadingError, match="No value for date_time"
        ):
            results.PracticeSet.load_from_file_object(f)

    def test_load_pratice_set_missing_activity_key(self) -> None:
        f = io.StringIO("\n5\n2024-05-02T14:28:42.439597+00:00\n")
        with pytest.raises(
            results.PracticeSetLoadingError, match="No value for activity_key"
        ):
            results.PracticeSet.load_from_file_object(f)

    def test_load_pratice_set_score_wrong_type(self) -> None:
        f = io.StringIO("activity_key\nscore is a 5\nwrong_date_format\n")

        with pytest.raises(
            results.PracticeSetLoadingError, match="score wasn't an integer"
        ):
            results.PracticeSet.load_from_file_object(f)

    def test_load_pratice_set_datetime_wrong_format(self) -> None:
        f = io.StringIO("activity_key\n5\nwrong_date_format\n")

        with pytest.raises(
            results.PracticeSetLoadingError, match="datetime wasn't in iso format"
        ):
            results.PracticeSet.load_from_file_object(f)
