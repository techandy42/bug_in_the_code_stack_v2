import pandas as pd
from openai_model import OpenAIModel
from pydantic import BaseModel
from typing import Any

df_python_bugs = pd.read_json('python_bugs.jsonl', lines=True)

openai_model = OpenAIModel(model_name="openai/gpt-4o", context_limit=128000)

class SampleCodeWithBug(BaseModel):
    documentation: str
    code_with_bug: str
    code_without_bug: str
    unit_tests: list[str]

bug_type = df_python_bugs.iloc[0]["name"]
bug_description = df_python_bugs.iloc[0]["description"]
implementation = df_python_bugs.iloc[0]["implementation"]

def tab_s(s: str) -> str:
    return "\n".join(["\t" + line for line in s.splitlines()])

sample_bug_type = "Incorrect Function Implementation"
sample_documentation = """# The function adds two numbers together and returns the sum.
# Example 1: add(1, 2) -> 3
# Example 2: add(-1, 1) -> 0
# Example 3: add(0, 0) -> 0"""
sample_code_with_bug = """def add(a, b):
    return a - b"""
sample_code_without_bug = """def add(a, b):
    return a + b"""
sample_unit_test1 = """try:
    result = add(1, 2)
    assert result == 3
    print("SUCCESS")
except AssertionError:
    print("FAILURE")"""
sample_unit_test2 = """try:
    result = add(-1, 1)
    assert result == 0
    print("SUCCESS")
except AssertionError:
    print("FAILURE")"""
sample_unit_test3 = """try:
    result = add(0, 0)
    assert result == 0
    print("SUCCESS")
except AssertionError:
    print("FAILURE")"""
sample_unit_tests = [sample_unit_test1, sample_unit_test2, sample_unit_test3]
sample_unit_test_with_run_with_timeout = """# Let function be defined as: func(param1: int, param2: str)
# Return value of "run_with_timeout" is either "SUCCESS" or "FAILURE"
try:
    timeout_duration = 1  # Timeout duration in seconds
    result = run_with_timeout(func, timeout_duration, 123, "abc")
    print(result)
except TimeoutException as e:
    pass"""

prompt_bugs_generate = f"""Generate two Python {implementation}s where the first {implementation} has a single bug and the second {implementation} has no bugs. Otherwise, the two {implementation}s should be the same.

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
- "unit_tests" contains a list of three unit tests that calls the {implementation} with different inputs. Each unit test should have the following characteristics:
    - It should be surrounded by a try-except block.
    - All the code for the unit test should be defined within the try-except block.
    - For "code_with_bug", at least one of the unit test should fail.
    - For "code_without_bug", all the unit tests should succeed.
    - If it has an expected value, it should be checked with an assert statement. If the assertion is true, print out "SUCCESS". Otherwise, print out "FAILURE".
    - If it is expected to be terminated (e.g., bug results in non-terminating execution), use pre-defined function "run_with_timeout" to check if the function executes within 1s. If it does, print out "SUCCESS". Otherwise, print out "FAILURE" 

Example Unit Test with "run_with_timeout":
{sample_unit_test_with_run_with_timeout}
    
Example Output (e.g., {sample_bug_type}):
"documentation":
    {tab_s(sample_documentation)}
"code_with_bug":
    {tab_s(sample_code_with_bug)}
"code_without_bug":
    {tab_s(sample_code_without_bug)}
"unit_tests":
    "unit_test item.1":
    {tab_s(tab_s(sample_unit_tests[0]))}
    "unit_test item.2":
    {tab_s(tab_s(sample_unit_tests[1]))}
    "unit_test item.3":
    {tab_s(tab_s(sample_unit_tests[2]))}

Note:
- The names of the {implementation} definitions must not indicate whether the bug exists or not.
- Do not output anything else other than the specificed JSON object.
"""

print(prompt_bugs_generate)

sample_code_dict = openai_model.completion_json(prompt_bugs_generate, SampleCodeWithBug)

print(sample_code_dict)
