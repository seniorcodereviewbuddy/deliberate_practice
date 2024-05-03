import pathlib

import pytest

import deliberate_practice
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


def test_main_practice_one_activity(tmp_path: pathlib.Path) -> None:
    activity_file = pathlib.Path(tmp_path, "activities.txt")
    with open(activity_file, "w", encoding="utf-8") as f:
        f.write("practice_activity")

    results_file = pathlib.Path(tmp_path, "results.txt")

    mock_input = mocks.MockInput(
        [
            "1",  # Start Practice Mode.
            "Y",  # Practice an activity.
            "2",  # Score the activty a 2.
            "N",  # Don't practice another, should exit.
        ]
    )
    deliberate_practice.main(mock_input, activity_file, results_file)
