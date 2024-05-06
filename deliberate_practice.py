"""Main entry point for the Deliberate Practice CLI."""

import datetime
import enum
import pathlib

import results
import routine
import settings
import user_input


class InvalidModeError(Exception):
    """An invalid mode was selected."""


class RunMode(enum.StrEnum):
    """The valid run modes of the deliberate practice app."""

    PRACTICE = "Practice"
    EVALUATION = "Evaluation"


def select_run_mode(fetch_input: user_input.FetchInput) -> RunMode:
    """Prompts the user to determine what RunMode to launch."""
    prompt = (
        "Welcome to the Deliberate Practice CLI" + "\n"
        "Which mode do you wish to run in?"
    )
    all_modes = list(RunMode)

    picked_index = user_input.prompt_for_choice(fetch_input, prompt, all_modes)
    picked_mode = all_modes[picked_index]
    return RunMode(picked_mode)


def run_practice_mode(
    fetch_input: user_input.FetchInput,
    activities: routine.Activities,
    practices: results.Practices,
) -> int:
    """Runs Practice mode with the given activites.

    Results are saved to the given practices instance.

    Returns the number of practice sets completed.
    """
    if not activities.get_num_activities():
        print("No activities found, nothing to practice.")
        return 0

    print(
        f"You currently have {activities.get_num_activities()} "
        "activities you can practice."
    )

    activities_done = 0
    while user_input.prompt_yes_or_no(
        fetch_input, "Do you wish to practice an activity?"
    ):
        chosen_activity = activities.get_random_activity()
        print(f"\nThe chosen activity is:\n\t{chosen_activity.get_description()}\n")

        user_prompt = "How did you do on this activity?"
        user_score = user_input.prompt_for_choice(
            fetch_input, user_prompt, results.POSSIBLE_SCORES
        )
        print("Keep up the good work\n")

        activities_done += 1

        current_time = datetime.datetime.now(datetime.timezone.utc)
        practices.add_practice_set(chosen_activity, user_score, current_time)
        practices.save()

    return activities_done


def main(
    fetch_input: user_input.FetchInput,
    activities_file: pathlib.Path,
    practices_file: pathlib.Path,
) -> None:
    """Starts the Deliberate Practice CLI.

    Raises:
        InvalidModeError: An unsupported mode was selected.
    """
    selected_run_mode = select_run_mode(fetch_input)
    if selected_run_mode == RunMode.PRACTICE:
        print("\nStaring Practice Mode")
        activities = routine.Activities(activities_file)
        practices = results.Practices(practices_file)

        run_practice_mode(fetch_input, activities, practices)
    elif selected_run_mode == RunMode.EVALUATION:
        print("\nStarting Evaluation Mode")
        practices = results.Practices(practices_file)
        evaluation = results.Evaluation(practices)
        print(evaluation)
    else:
        raise InvalidModeError(f"Unexpected mode given, {selected_run_mode}")


if __name__ == "__main__":
    main(
        input,
        settings.ACTIVITIES_FILE,
        settings.PRACTICES_FILE,
    )
