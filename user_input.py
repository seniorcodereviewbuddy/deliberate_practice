"""Functions handling collecting input from users.

This allows the code relating to automatically retrying when an input
isn't valid to be grouped in this single location.
"""

import typing

# Note, ideally this should be a type, but that isn't currently
# supported by mypy.
# See https://github.com/python/mypy/issues/15238 for details.
FetchInputWithPrompt = typing.Callable[[str], str]


class NoChoiceMadeError(Exception):
    """No choice was made by the User."""


def _is_valid_pick(user_choice: str, max_choice: int) -> bool:
    try:
        pick = int(user_choice)
    except ValueError:
        return False

    if pick < 1 or pick > max_choice:
        return False

    return True


def prompt_for_choice(
    fetch_input: FetchInputWithPrompt, prompt: str, choices: list[str]
) -> int:
    """Prompts the user to pick an option from the list of choices.

    Note, since python lists are 0-based, but we want to show the
    choices to users as 1-based, we have to 1 when moving to user land
    and remove 1 when moving back to code interactions.

    Returns the index of the selected item.

    Raises:
        NoChoiceMadeError: If the user fails to make a decision due to
            lack of input.
    """
    # Start enumerate at 1 and add 1 to max_choice as we shift from
    # 0-based to 1-based.
    choices_with_index = "\n".join(
        f"{str(index)}) {value}" for index, value in enumerate(choices, 1)
    )
    max_choice = len(choices) + 1
    complete_user_prompt = prompt + "\n" + choices_with_index + "\n"
    while True:
        try:
            user_choice = fetch_input(complete_user_prompt)
        except EOFError as e:
            raise NoChoiceMadeError from e

        if _is_valid_pick(user_choice, max_choice):
            # Subtract 1 here since the user_choice was 1-based before
            # and now is 0-based.
            return int(user_choice) - 1

        print(
            "\n\nUnclear input, was expecting a value between 1 and "
            f"{max_choice}, got {user_choice}. Please try again"
        )
        continue
