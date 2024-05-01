"""Main entry point for the Deliberate Practice CLI."""

import enum

import user_input


class InvalidModeError(Exception):
    """An invalid mode was selected."""


class RunMode(enum.StrEnum):
    """The valid run modes of the deliberate practice app."""

    PRACTICE = "Practice"
    EVALUATION = "Evaluation"


def select_run_mode(fetch_input: user_input.FetchInputWithPrompt) -> RunMode:
    """Prompts the user to determine what RunMode to launch."""
    prompt = (
        "Welcome to the Deliberate Practice CLI" + "\n"
        "Which mode do you wish to run in?"
    )
    all_modes = list(RunMode)

    pick = user_input.prompt_for_choice(fetch_input, prompt, all_modes)
    return RunMode(pick)


def main(fetch_input: user_input.FetchInputWithPrompt) -> None:
    """Starts the Deliberate Practice CLI."""
    selected_run_mode = select_run_mode(fetch_input)
    if selected_run_mode == RunMode.PRACTICE:
        print("Practice Mode Selected")
    elif selected_run_mode == RunMode.EVALUATION:
        print("Evaluation Mode Selected")
    else:
        raise InvalidModeError(f"Unexpected mode given, {selected_run_mode}")


if __name__ == "__main__":
    main(input)
