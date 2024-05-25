from model import Model
from pydantic import BaseModel, ValidationError
from typing import Type
import json
import re
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class OpenAIModel(Model):
    def __init__(self, model_name, context_limit):
        self.model_name = model_name
        self.context_limit = context_limit

    def completion_json(self, prompt: str, pydantic_model: Type[BaseModel]) -> dict:
        # Define the messages to send to the model
        messages = [
            {
                "role": "system",
                "content": "Return output in JSON format.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        # Generate the JSON output using the completion method
        response = completion(model=self.model_name, messages=messages)

        # Extract the content from the response
        content = response.choices[0].message.content.strip()

        # Remove ```json <content> ``` tags using regex
        content = re.sub(r'```json\s*(.*?)\s*```', r'\1', content, flags=re.DOTALL)

        # Parse the JSON into a dictionary
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("The content returned is not valid JSON")

        # Validate the dictionary against the Pydantic model
        try:
            _ = pydantic_model(**data)
        except ValidationError as e:
            raise ValueError(f"The JSON does not contain all necessary fields: {e}")

        return data

    def get_context_limit(self) -> int:
        return self.context_limit
    
# Test Case
if __name__ == "__main__":
    openai_model = OpenAIModel(model_name="openai/gpt-4o", context_limit=128000)
    class Person(BaseModel):
        name: str
        age: int
    prompt = f"""Create a fictional person with a name and an age.

JSON Output Format:
{{
    "name": str,
    "age": int, 
}}
"""
    data = openai_model.completion_json(prompt, Person)
    print(data)
