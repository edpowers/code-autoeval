"""Workbook for interacting with the backend model."""

# %%

import asyncio
import os
import re
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

import nest_asyncio
import pandas as pd
from multiuse.filepaths.find_classes_in_dir import FindClassesInDir
from multiuse.filepaths.find_project_root import FindProjectRoot
from multiuse.filepaths.system_utils import SystemUtils
from multiuse.log_methods.custom_logging_funcs import CustomLoggingFuncs
from multiuse.model import class_data_model

from code_autoeval.llm_model.hierarchy.creation import create_class_hierarchy
from code_autoeval.llm_model.hierarchy.filtration import filter_class_hierarchy

nest_asyncio.apply()

print(CustomLoggingFuncs)

path_cwd = Path(os.getcwd()).parent


if str(path_cwd) not in sys.path:
    sys.path.insert(0, str(path_cwd))

from code_autoeval.llm_model import imports
from code_autoeval.llm_model.llm_model_client import LLMModelClient
from code_autoeval.llm_model.utils import extraction

# %%

llm_model_client = LLMModelClient()

# %%


class AbstractClass(ABC):
    @abstractmethod
    def sum_of_numbers(self, *args: int) -> int:
        """Calculates the sum of the given numbers."""
        ...

    @abstractmethod
    def factorial(self, n: int) -> int:
        """Calculates the factorial of a given number."""
        ...

    @abstractmethod
    def fibonacci(self, n: int) -> int:
        """Finds the nth Fibonacci number."""
        ...

    @abstractmethod
    def gcd(self, a: int, b: int) -> int:
        """Computes the Greatest Common Divisor of two numbers."""
        ...

    @abstractmethod
    def sum_of_primes(self, n: int) -> int:
        """Calculates the sum of prime numbers up to n."""
        ...


# Usage example
async def main() -> None:
    query = "Calculate the sum of 1, 2, and 3"

    code, result, expected_output, context, pytest_tests = (
        await llm_model_client.code_generator(
            query, AbstractClass.sum_of_numbers, verbose=True, debug=True
        )
    )

    print("Final generated code:", code)
    print("Final execution result:", result)
    print("Expected output:", expected_output)
    print("Execution context:", context)

    assert str(result) == (
        expected_output
    ), f"Expected: {expected_output}, Got: {result}"

    # Dictionary of functions to test
    functions_to_test = {
        "Factorial": {
            "query": "Calculate the factorial of 5",
            "function": AbstractClass.factorial,
        },
        "Fibonacci": {
            "query": "Find the 10th Fibonacci number",
            "function": AbstractClass.fibonacci,
        },
        "GCD": {
            "query": "Compute the Greatest Common Divisor of 48 and 18",
            "function": AbstractClass.gcd,
        },
        "Sum of Primes": {
            "query": "Calculate the sum of prime numbers up to 20",
            "function": AbstractClass.sum_of_primes,
        },
    }

    for function_name, function_info in functions_to_test.items():
        query = function_info["query"]
        function = function_info["function"]

        print(f"\n{function_name} Example:")
        code, result, expected_output, context, pytest_tests = (
            await llm_model_client.code_generator(query, function, verbose=True)
        )

        # Clean up the expected output
        expected_output = expected_output.strip()
        expected_output = re.sub(r"^```|```$", "", expected_output).strip()

        print("Query:", query)
        print("Final generated code:", code)
        print("Final execution result:", result)
        print("Expected output:", expected_output)
        print("Execution context:", context)

        try:
            assert (
                str(result) == expected_output
            ), f"Expected: {expected_output}, Got: {result}"
            print("Assertion passed!")
        except AssertionError as e:
            print("Assertion failed:", str(e))


# Run the async main function
# asyncio.run(main())


# %%


class AbstractDataFrameClass(ABC):

    @abstractmethod
    def remove_outliers(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Removes outliers from the given DataFrame column.

        If the column does not contain numerical data, then log the column name - data type,
        and return the original dataframe.

        Numerical column data types can be defined as:
            np.number, np.int64, np.float64, np.float32, np.int32, np.int16, np.float16

        Please use a library that preserves the temporal nature of the data, without
        introducing leakage or bias.
        """
        ...

    @abstractmethod
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Removes duplicate rows from the given DataFrame.

        If the DataFrame is empty, return an empty DataFrame.
        Make sure the dataframe has an index in the test cases.
        """
        ...


async def main2() -> None:
    query = "Remove outliers from a numerical column in a pandas dataframe with temporal ordering."
    goal = "Refactor code to handle edge cases."

    function_to_implement = AbstractDataFrameClass.remove_outliers
    skip_generate_fake_data = False

    code, serialized_result, expected_output, context, pytest_tests = (
        await llm_model_client.code_generator(
            query,
            function_to_implement,
            goal=goal,
            verbose=True,
            debug=True,
            skip_generate_fake_data=skip_generate_fake_data,
        )
    )


# %%

# Run the async main function
# asyncio.run(main2())

# %%
# %%

llm_model_client = LLMModelClient()

unique_imports = (
    imports.find_imports_from_dir.FindImportsFromDir.find_unique_imports_from_dir()
)


# Example usage
module_path = SystemUtils.get_class_file_path(main2)

# Find the project root
project_root = FindProjectRoot.find_project_root(module_path)

directory = project_root.joinpath("code_autoeval")
generated_code_dir = project_root.joinpath("generated_code/tests")
generated_code_logs = project_root.joinpath("generated_code_logs")

SystemUtils.clean_directory(generated_code_logs, python_file_patterns=["*.log"])

class_info_list = FindClassesInDir.find_classes_in_dir(str(directory))

class_data_factory = class_data_model.ClassDataModelFactory(project_root)
class_data_models = class_data_factory.create_from_class_info(class_info_list)

# Instantiate the fixer parser class to find all registered fixtures.
fixture_parser = extraction.fixture_parser.FixtureParser()
fixture_parser.parse_directory(
    project_root.joinpath("generated_code/fixtures/fixtures")
)


filter_hierarchy_classes = filter_class_hierarchy.FilterClassHierarchy()
filter_hierarchy_classes.build_hierarchy_levels(
    create_class_hierarchy.CreateClassHierarchy.construct_class_hierarchy().filtered_hierarchy
)
filter_hierarchy_classes.get_hierarchy_levels()
flattened_hierachy = filter_hierarchy_classes.flatten_hierarchy()
class_data_models = class_data_factory.sort_by_hierarchy(flattened_hierachy)


display(class_data_models)

# %%


# %%


async def generate_code_for_classes(
    class_data_models: List[class_data_model.ClassDataModel],
    llm_model_client: LLMModelClient,
    generated_code_dir: Path,
    clean_directory_before_start: bool = True,
    goal: str = "Refactor code to handle edge cases and improve efficiency.",
    fixture_parser: Optional[extraction.fixture_parser.FixtureParser] = None,
) -> None:

    if clean_directory_before_start:
        SystemUtils.clean_directory(
            generated_code_dir, python_file_patterns=["*.py", "*.pyc"]
        )

    for class_model in class_data_models:

        print(f"Generating code for class: {class_model.class_name}")

        if not class_model.class_methods:
            print(f"Skipping: No functions to implement for {class_model.class_name}")
            continue

        for method in class_model.class_methods:

            try:
                function_to_implement = getattr(class_model.class_object, method)
            except AttributeError:
                print(
                    f"Error getting method {method} for class {class_model.class_name}"
                )
                continue

            query = (
                f"Implement the {method} method for the {class_model.class_name} class."
            )

            # display(class_model)

            try:
                code, serialized_result, context, pytest_tests = (
                    await llm_model_client.code_generator(
                        query,
                        function_to_implement,
                        goal=goal,
                        verbose=True,
                        debug=True,
                        skip_generate_fake_data=True,
                        class_model=class_model,
                        fixture_parser=fixture_parser,
                    )
                )

                print(f"Generated code for {class_model.class_name}.{method}:")
                print(code)
                print("\nGenerated pytest tests:")
                print(pytest_tests)
                print("\n" + "=" * 50 + "\n")

            except Exception as e:
                print(CustomLoggingFuncs.show_code_lines(e))


# %%


async def main3(clean_directory_before_start: bool = False) -> None:
    # Assuming llm_model_client is already initialized
    await generate_code_for_classes(
        class_data_models,
        llm_model_client,
        generated_code_dir=generated_code_dir,
        clean_directory_before_start=clean_directory_before_start,
        fixture_parser=fixture_parser,
    )


# Run the async main function
value = asyncio.run(main3(clean_directory_before_start=False))


# %%
# %%


# %%


class_data_models[0]

# %%


# %%


# file_path = "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/llm_model/utils/model_response/test_SerializeDataframes_deserialize_dataframe.py"
# from code_autoeval.llm_model.utils.code_cleaning.remove_invalid_imports import RemoveInvalidImports
# RemoveInvalidImports.remove_invalid_imports(file_path)

# %%

import subprocess
from pprint import pprint

result = subprocess.run(
    ["mypy", file_path],
    capture_output=True,
    text=True,
)

pprint(result)

# %%


pprint(result)

# %%

file_path = "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/llm_model/utils/model_response/test_SerializeDataframes_serialize_dataframe.py"

flake8_result = subprocess.run(
    ["flake8", "--select=E999", file_path],
    capture_output=True,
    text=True,
)

pprint(str(flake8_result))

# %%


from code_autoeval.llm_model.imports.run_flake8_fix_imports import RunFlake8FixImports

RunFlake8FixImports.comment_out_syntax_errors(file_path)

# %%
