import pytest

import user_input
from test_utils import mocks


class TestPromptUserForChoice:
    basic_prompt = "basic prompt string"

    @pytest.mark.parametrize("pick", [1, 2, 3])
    def test_valid_choices(self, pick: int) -> None:
        choices = ["a", "b", "c"]
        input_mock = mocks.MockInput([str(pick)])
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == pick - 1

    def test_valid_choice_only_one_option(self) -> None:
        choices = ["a"]
        input_mock = mocks.MockInput(["1"])
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == 0

    def test_valid_choice_after_invalid_str(self) -> None:
        input_mock = mocks.MockInput(["invalid_choice", "1"])
        choices = ["a", "b", "c"]
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == 0

    def test_valid_choice_after_invalid_int(self) -> None:
        input_mock = mocks.MockInput(["7", "1"])
        choices = ["a", "b", "c"]
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == 0

    def test_valid_choice_after_negative_int(self) -> None:
        input_mock = mocks.MockInput(["-7", "2"])
        choices = ["a", "b", "c"]
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == 1

    def test_no_choice_made(self) -> None:
        input_mock = mocks.MockInput([])
        choices = ["a", "b", "c"]
        with pytest.raises(user_input.NoChoiceMadeError):
            user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)

    def test_no_choice_made_after_invalid_choice(self) -> None:
        input_mock = mocks.MockInput(["5"])
        choices = ["a", "b", "c"]
        with pytest.raises(user_input.NoChoiceMadeError):
            user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)


class TestPromptUserForYesOrNo:
    basic_prompt = "basic prompt string"

    @pytest.mark.parametrize(
        ("choice", "expected_value"),
        [("y", True), ("Y", True), ("n", False), ("N", False)],
    )
    def test_valid_choices(self, choice: int, expected_value: bool) -> None:
        mock_input = mocks.MockInput([str(choice)])
        selection = user_input.prompt_yes_or_no(mock_input, self.basic_prompt)
        assert selection == expected_value

    @pytest.mark.parametrize("invalid_inputs", [["1"], ["a"], ["a", "b"]])
    def test_positive_result_after_invalid_inputs(
        self, invalid_inputs: list[str]
    ) -> None:
        mock_input = mocks.MockInput(invalid_inputs + ["y"])
        selection = user_input.prompt_yes_or_no(mock_input, self.basic_prompt)
        assert selection is True

    @pytest.mark.parametrize("invalid_inputs", [["1"], ["a"], ["a", "b"]])
    def test_negative_result_after_invalid_inputs(
        self, invalid_inputs: list[str]
    ) -> None:
        mock_input = mocks.MockInput(invalid_inputs + ["N"])
        selection = user_input.prompt_yes_or_no(mock_input, self.basic_prompt)
        assert selection is False

    def test_no_choice_made(self) -> None:
        mock_input = mocks.MockInput([])
        with pytest.raises(user_input.NoChoiceMadeError):
            user_input.prompt_yes_or_no(mock_input, self.basic_prompt)

    def test_no_choice_made_after_invalid_choice(self) -> None:
        mock_input = mocks.MockInput(["5"])
        with pytest.raises(user_input.NoChoiceMadeError):
            user_input.prompt_yes_or_no(mock_input, self.basic_prompt)
