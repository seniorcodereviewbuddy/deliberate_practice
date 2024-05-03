"""Module containing various settings used by the Deliberate Practice App."""

import pathlib

USER_FILES_ROOT = pathlib.Path(
    __file__, "..", "user_files"
).resolve()

ACTIVITIES_FILE = pathlib.Path(
    USER_FILES_ROOT, "my_deliberate_practice_activites.txt"
)

PRACTICES_FILE = pathlib.Path(
    USER_FILES_ROOT, "my_deliberate_practice_results.txt"
)
