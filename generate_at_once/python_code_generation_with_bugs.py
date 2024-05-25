import pandas as pd
from openai_model import OpenAIModel
from openai_tokenizer import OpenAITokenizer
from pydantic import BaseModel
import uuid
import datetime
import json

def append_dict_to_jsonl(file_path, data):
    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write('\n')

def generate_unique_id():
    # Get the current time
    current_time = datetime.datetime.now()
    
    # Format the time as a string
    time_str = current_time.strftime("%Y%m%d%H%M%S%f")
    
    # Generate a UUID
    unique_suffix = uuid.uuid4().hex
    
    # Combine the time string with the UUID to ensure uniqueness
    unique_id = f"{time_str}_{unique_suffix}"
    
    return unique_id

def tab_s(s: str) -> str:
    return "\n".join(["\t" + line for line in s.splitlines()])

df_python_bugs = pd.read_json('python_bugs.jsonl', lines=True)

openai_model = OpenAIModel(model_name="openai/gpt-4o", context_limit=128000)
openai_tokenizer = OpenAITokenizer(encoding_name="cl100k_base")

class SampleCodeWithBug(BaseModel):
    documentation: str
    code_with_bug: str
    code_without_bug: str
    unit_tests: list[str]

n = len(df_python_bugs)
i = 0
tries = 0

while i < n:
    try:
        bug_type = df_python_bugs.iloc[i]["name"]
        bug_description = df_python_bugs.iloc[i]["description"]
        implementation = df_python_bugs.iloc[i]["implementation"]
        sample_unit_test_with_run_with_timeout = """# Let function be defined as: func(param1: int, param2: str)
# Return value of "run_with_timeout" is either "SUCCESS" or "FAILURE"
try:
    timeout_duration = 1  # Timeout duration in seconds
    _ = run_with_timeout(func, timeout_duration, 123, "abc")
    print("SUCCESS")
except:
    print("FAILURE")"""

        prompt = f"""Generate two Python {implementation}s where the first {implementation} has a single bug and the second {implementation} has no bugs. Otherwise, the two {implementation}s should be the same.

Bug Type:
{bug_type}

Bug Description:
{bug_description}

JSON Output Format:
{{
    "documentation": str
    "code_with_bug": str
    "code_without_bug": str
    "unit_tests": list[str]
}}

Output Explained:
- "documentation" is a valid comment for the {implementation} definition. The documentation should have the following characteristics:
    - Each line should start with a "#".
    - First line should describe the purpose of the {implementation} definition.
    - Afterwards, every line should describe the sample inputs and expected outputs from the "unit_tests".
    - It must not mention about the bug.
- "code_with_bug" contains the {implementation} definition with a single bug. 
- "code_without_bug" contains the {implementation} definition with no bugs.
- "unit_tests" contains a list of five unit tests that calls the {implementation} with different inputs. Each unit test should have the following characteristics:
    - It should be surrounded by a try-except block.
    - Do not include exception type in the except block.
    - All the code for the unit test should be defined within the try-except block.
    - For "code_with_bug", at least one of the unit test should fail.
    - For "code_without_bug", all the unit tests should succeed.
    - If it has an expected value, it should be checked with an assert statement. If the assertion is true, print out "SUCCESS". Otherwise, print out "FAILURE".
    - If it is expected to be terminated (e.g., bug results in non-terminating execution), use pre-defined function "run_with_timeout" to check if the function executes within 1s. If it does, print out "SUCCESS". Otherwise, print out "FAILURE"
    - All unit tests should either be assert statements or calls to "run_with_timeout". Do not mix these two.

Example Unit Test with "run_with_timeout":
{sample_unit_test_with_run_with_timeout}

Note:
- The names of the {implementation} definitions must not indicate whether the bug exists or not.
- Do not output anything else other than the specified JSON object."""

        code_sample_dict = {
            'id': generate_unique_id(),
            'name': bug_type,
        }
        result_dict = openai_model.completion_json(prompt, SampleCodeWithBug)
        for key in result_dict.keys():
            code_sample_dict[key] = result_dict[key]

        append_dict_to_jsonl('python_code_samples_with_bugs.jsonl', code_sample_dict)

        print(f"Generated code sample with bug no.{i}...")

        i += 1

    except Exception as e:
        print(f"Error at generating code sample with bug no.{i}...")

        tries += 1
        if tries == 5:
            tries = 0
            i += 1
