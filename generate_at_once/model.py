from abc import ABC, abstractmethod

class Model(ABC):
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
    def completion_json(self, prompt: str) -> dict:
        """
        Abstract method to generate a completion from a prompt.

        Parameters:
        prompt (str): The prompt to generate a completion from.

        Returns:
        dict: The completion as a JSON object.
        """
        pass

    @abstractmethod
    def get_context_limit(self) -> int:
        """
        Abstract method to get the context limit of the model.

        Returns:
        int: The context limit.
        """
        pass
