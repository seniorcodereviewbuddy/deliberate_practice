import pytest

import user_input
from test_utils import mocks


class TestPromptUserForChoice:
    basic_prompt = "basic prompt string"

    @pytest.mark.parametrize(("pick", "expected_value"), [(1, "a"), (2, "b"), (3, "c")])
    def test_valid_choices(self, pick: int, expected_value: str) -> None:
        choices = ["a", "b", "c"]
        input_mock = mocks.MockInput([str(pick)])
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == expected_value

    def test_valid_choice_only_one_option(self) -> None:
        choices = ["a"]
        input_mock = mocks.MockInput(["1"])
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == "a"

    def test_valid_choice_after_invalid_str(self) -> None:
        input_mock = mocks.MockInput(["invalid_choice", "1"])
        choices = ["a", "b", "c"]
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == "a"

    def test_valid_choice_after_invalid_int(self) -> None:
        input_mock = mocks.MockInput(["7", "1"])
        choices = ["a", "b", "c"]
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == "a"

    def test_valid_choice_after_negative_int(self) -> None:
        input_mock = mocks.MockInput(["-7", "2"])
        choices = ["a", "b", "c"]
        selection = user_input.prompt_for_choice(input_mock, self.basic_prompt, choices)
        assert selection == "b"

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
