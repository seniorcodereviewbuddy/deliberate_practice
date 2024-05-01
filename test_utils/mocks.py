"""A module containing mocks for testing."""


class MockInput:  # pylint: disable=too-few-public-methods
    """A MockInput class that can replace input for tests."""

    def __init__(self, inputs: list[str]):
        """Initialize the instance with inputs to return when called."""
        self.inputs = inputs

    def __call__(self, _prompt: str) -> str:
        """Returns the next input string.

        Raises:
            EOFError: if there is no more input, similar to input().
        """
        if not self.inputs:
            raise EOFError

        return self.inputs.pop(0)
