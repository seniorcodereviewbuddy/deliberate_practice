"""Module containing various settings constants."""

import pathlib

USER_FILES_ROOT = pathlib.Path(__file__, "..", "user_files").resolve()

ACTIVITIES_FILE = pathlib.Path(USER_FILES_ROOT, "my_deliberate_practice_activities.txt")

PRACTICES_FILE = pathlib.Path(USER_FILES_ROOT, "my_deliberate_practice_practices.txt")
