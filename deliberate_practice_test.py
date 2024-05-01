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
