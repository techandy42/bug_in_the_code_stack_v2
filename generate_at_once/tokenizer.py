from abc import ABC, abstractmethod

class Tokenizer(ABC):
    def __init__(self, *args, **kwargs):
        """
        Initialize the Tokenizer with any number of arguments.

        Parameters:
        *args: A tuple of positional arguments.
        **kwargs: A dictionary of keyword arguments.
        """
        # You can handle or pass these arguments as needed
        super().__init__(*args, **kwargs)  # Optional: useful if extending another class with an __init__

    @abstractmethod
    def count_tokens(self, string: str) -> int:
        """
        Abstract method to count tokens in a string.

        Parameters:
        string (str): The string to count tokens in.

        Returns:
        int: The number of tokens.
        """
        pass
