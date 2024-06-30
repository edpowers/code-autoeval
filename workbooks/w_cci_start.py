"""Workbook for interacting with the backend model."""

# %%
import asyncio
import inspect
import logging
import os
import re
import sys
from inspect import Parameter
from pathlib import Path

import pandas as pd
from multiuse.filepaths.find_classes_in_dir import FindClassesInDir
from multiuse.filepaths.find_project_root import FindProjectRoot
from multiuse.filepaths.system_utils import SystemUtils
from multiuse.log_methods.custom_logging_funcs import CustomLoggingFuncs

path_cwd = Path(os.getcwd()).parent


if str(path_cwd) not in sys.path:
    sys.path.insert(0, str(path_cwd))

import importlib
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

import nest_asyncio
from dotenv import load_dotenv
from pydantic import create_model

from code_autoeval.clients.llm_model.llm_model import LLMModel

nest_asyncio.apply()

print(logging, inspect, Parameter, create_model, load_dotenv, os)


# %%


# %%

llm_model_client = LLMModel()

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

# Example usage
module_path = Path(SystemUtils.get_class_file_path(main2))

# Find the project root
project_root = FindProjectRoot.find_project_root(module_path)

directory = project_root.joinpath("code_autoeval")

class_info = FindClassesInDir.find_classes_in_dir(directory)


display(class_info)

llm_model_client = LLMModel()

# %%

from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel

print(ClassDataModel)


# %%


async def generate_code_for_classes(
    class_info: Dict[str, List[Tuple[str, str, List[str]]]], llm_model_client: LLMModel
) -> None:
    for file_path, classes in class_info.items():
        for (
            class_name,
            import_path,
            function_names,
        ) in classes:

            if not function_names:
                print(f"Skipping: No functions to implement for {classes=}")
                continue

            print(f"Generating code for class: {class_name} from {file_path}")

            # Dynamically import the class
            module_name, class_name = import_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            class_to_process = getattr(module, class_name)
            base_classes = [base.__name__ for base in class_to_process.__bases__]
            class_attributes = [
                name
                for name in dir(class_to_process)
                if not name.startswith("__")
                and not callable(getattr(class_to_process, name))
            ]
            # Try to get __init__ parameters for dependency identification
            init_signature = inspect.signature(class_to_process.__init__)
            init_parameters = [
                param.name
                for param in init_signature.parameters.values()
                if param.name != "self"
            ]

            # Get the standard out from running help() against the class,
            # which will hopefully provide the context.
            class_model = ClassDataModel(
                class_object=class_to_process,
                class_name=class_name,
                class_methods=function_names,
                class_attributes=class_attributes,
                init_params=init_parameters,
                base_classes=base_classes,
                absolute_path=import_path,
            )

            goal = "Refactor code to handle edge cases and improve efficiency."

            for method in function_names:
                function_to_implement = getattr(class_to_process, method)

                query = f"Implement the {method} method for the {class_name} class."
                try:
                    code, serialized_result, expected_output, context, pytest_tests = (
                        await llm_model_client.code_generator(
                            query,
                            function_to_implement,
                            goal=goal,
                            verbose=True,
                            debug=True,
                            skip_generate_fake_data=True,
                            class_model=class_model,
                        )
                    )

                    print(f"Generated code for {class_name}.{method}:")
                    print(code)
                    print("\nGenerated pytest tests:")
                    print(pytest_tests)
                    print("\n" + "=" * 50 + "\n")

                except Exception as e:
                    print(CustomLoggingFuncs.show_code_lines(e))


# %%


async def main3() -> None:
    # Assuming llm_model_client is already initialized
    await generate_code_for_classes(class_info, llm_model_client)


# Run the async main function
value = asyncio.run(main3())
# %%
# %%
