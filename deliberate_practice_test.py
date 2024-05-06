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
        [
            "1",  # Start Practice Mode.
        ]
        + practice_session_inputs
        + [
            "N",  # Don't practice any more activities, should return.
        ]
    )
    activites_done = deliberate_practice.run_practice_mode(
        mock_input, activities, practices
    )
    assert activites_done == number_of_practice_sets


def test_main_practice_one_activity(tmp_path: pathlib.Path) -> None:
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


def test_main_evaluation(tmp_path: pathlib.Path) -> None:
    activity_file = pathlib.Path(tmp_path, "activities.txt")
    with open(activity_file, "w", encoding="utf-8") as f:
        f.write("practice_activity")

    practices_file = pathlib.Path(tmp_path, "practices.txt")

    mock_input = mocks.MockInput(
        [
            "2",  # Start Evaluation Mode.
        ]
    )
    deliberate_practice.main(mock_input, activity_file, practices_file)
