import datetime
import pathlib

import pytest

import deliberate_practice
import results
import routine
import user_input
from test_utils import mocks


@pytest.mark.parametrize(
    ("user_selection", "expected_mode"),
    [
        (1, deliberate_practice.RunMode.PRACTICE),
        (2, deliberate_practice.RunMode.EVALUATION),
    ],
)
def test_select_run_mode_choice_made(
    user_selection: str, expected_mode: deliberate_practice.RunMode
) -> None:
    input_mock = mocks.MockInput([str(user_selection)])
    selected_mode = deliberate_practice.select_run_mode(input_mock)
    assert selected_mode == expected_mode


def test_select_run_mode_no_choice() -> None:
    input_mock = mocks.MockInput([])
    with pytest.raises(user_input.NoChoiceMadeError):
        deliberate_practice.select_run_mode(input_mock)


@pytest.mark.parametrize("number_of_practice_sets", [0, 1, 10, 100])
def test_run_practice_mode(
    tmp_path: pathlib.Path, number_of_practice_sets: int
) -> None:
    activity_file = pathlib.Path(tmp_path, "activities.txt")
    with open(activity_file, "w", encoding="utf-8") as f:
        f.write("practice_activity")

    activities = routine.Activities(activity_file)

    practices_file = pathlib.Path(tmp_path, "practices.txt")
    practices = results.Practices(practices_file)

    practice_session_inputs = [
        "Y",  # Start an activity.
        "2",  # Score the activity a 2.
    ] * number_of_practice_sets

    mock_input = mocks.MockInput(
        practice_session_inputs
        + [
            "N",  # Don't practice any more activities, should return.
        ]
    )
    activites_done = deliberate_practice.run_practice_mode(
        mock_input, activities, practices
    )
    assert activites_done == number_of_practice_sets


def test_main_practice_one_activity(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    activity_file = pathlib.Path(tmp_path, "activities.txt")
    with open(activity_file, "w", encoding="utf-8") as f:
        f.write("practice_activity")

    practices_file = pathlib.Path(tmp_path, "practices.txt")

    mock_input = mocks.MockInput(
        [
            "1",  # Start Practice Mode.
            "Y",  # Practice an activity.
            "2",  # Score the activty a 2.
            "N",  # Don't practice another, should exit.
        ]
    )
    deliberate_practice.main(mock_input, activity_file, practices_file)

    expected_output = (
        "Welcome to the Deliberate Practice CLI\n"
        "Which mode do you wish to run in?\n"
        "1) Practice\n"
        "2) Evaluation\n\n"
        "Staring Practice Mode\n"
        "Note: No Practices file found. Starting from an empty state\n"
        "You currently have 1 activities you can practice.\n"
        "Do you wish to practice an activity?\n(Y/N)? \n"
        "The chosen activity is:\n"
        "\tpractice_activity\n\n"
        "How did you do on this activity?\n"
        "1) I wasn’t successful\n"
        "2) I was ~25% successful\n"
        "3) I was ~50% successful\n"
        "4) I was ~75% successful\n"
        "5) I executed the task flawlessly"
        "\nKeep up the good work\n\n"
        "Do you wish to practice an activity?\n(Y/N)? "
    )

    captured_output = capsys.readouterr().out
    assert expected_output in captured_output


def test_main_evaluation(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    activity_key = "practice_activity"
    activity = routine.Activity(activity_key)

    activity_file = pathlib.Path(tmp_path, "activities.txt")
    with open(activity_file, "w", encoding="utf-8") as f:
        f.write(activity_key)

    practices_file = pathlib.Path(tmp_path, "practices.txt")
    practices = results.Practices(practices_file)
    time = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)
    num_practice_sets = 5
    for _ in range(num_practice_sets):
        practices.add_practice_set(activity, 1, time)
    practices.save()

    mock_input = mocks.MockInput(
        [
            "2",  # Start Evaluation Mode.
        ]
    )
    deliberate_practice.main(mock_input, activity_file, practices_file)

    expected_output = (
        "Starting Evaluation Mode\n"
        f"1 activity has been completed {num_practice_sets} times.\n\n"
        "practice_activity\n"
        f"\tPracticed {num_practice_sets} times.\n"
        "\tOldest practice 2024-01-01T00:00:00+00:00\n"
        "\tNewest practice 2024-01-01T00:00:00+00:00\n"
        "\tScores: [1, 1, 1, 1, 1]"
    )
    captured = capsys.readouterr()
    assert expected_output in captured.out
