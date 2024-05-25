from tokenizer import Tokenizer
import tiktoken

class OpenAITokenizer(Tokenizer):
    def __init__(self, encoding_name):
        self.encoding_name = encoding_name

    def count_tokens(self, string: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(self.encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
