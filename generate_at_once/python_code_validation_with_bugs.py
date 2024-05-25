import pandas as pd

df_python_code_samples_with_bugs = pd.read_json('python_code_samples_with_bugs.jsonl', lines=True)

run_with_timeout_definition = f"""import concurrent.futures
import time

class TimeoutException(Exception):
    pass

def run_with_timeout(func, timeout, *args, **kwargs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            result = future.result(timeout=timeout)
            return result
        except concurrent.futures.TimeoutError:
            raise TimeoutException("Execution timed out")
"""

n = len(df_python_code_samples_with_bugs)

valid_bugs = []

for i in range(n):
    sample_code_with_bug = df_python_code_samples_with_bugs.iloc[i]
    name = sample_code_with_bug["name"]
    code_with_bug = sample_code_with_bug["code_with_bug"]
    code_without_bug = sample_code_with_bug["code_without_bug"]
    unit_tests = sample_code_with_bug["unit_tests"]

    code_with_bug_and_unit_tests = run_with_timeout_definition + "\n" + code_with_bug + "\n" + "\n\n".join(unit_tests)
    code_without_bug_and_unit_tests = run_with_timeout_definition + "\n" + code_without_bug + "\n" + "\n\n".join(unit_tests)

    print("=" * 11 + f"SAMPLE {i}" + "=" * 11)
    print("CODE WITH BUG:")
    exec(code_with_bug_and_unit_tests)
    print()

    print("CODE WITHOUT BUG:")
    exec(code_without_bug_and_unit_tests)
    print("=" * 30)
    print()
