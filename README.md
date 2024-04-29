# Deliberate Practice App
Initial deliberate practice app repo for senior code review buddy.
To learn more about Senior Code Review Buddy, please visit https://seniorcodereviewbuddy.com

You can also visit the YouTube channel at https://www.youtube.com/@SeniorCodeReviewBuddy


## Local Setup

1) Download and install conda
    Probably from https://conda.io/projects/conda/en/latest/user-guide/install/index.html, if you don't already have it.
2) Create the Deliberate Practice conda environment
    Likely with the following command in a CLI "conda env create --file deliberate_practice.yml"
3) If desired, set the environment variable DELIBERATE_PRACTICE_CONDA_DIR to the newly created conda directory
    This can be used by Sublime to find the python executable to run, if desired

## Running Hooks Local

To run the hooks locally, you'll need to first install pre-commit with "pre-commit install", from inside
your Conda environment.

If you want a run just one hook, you can with "pre-commit run {hook_id}"

## Running Tests Locally

To run all the test locally just run pytest in the root directory.

For more details on how to work with pytest, look at https://docs.pytest.org/en/8.2.x/contents.html