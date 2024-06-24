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

path_cwd = Path(os.getcwd()).parent


if str(path_cwd) not in sys.path:
    sys.path.insert(0, str(path_cwd))

from abc import ABC, abstractmethod

import nest_asyncio
from dotenv import load_dotenv
from pydantic import create_model

nest_asyncio.apply()

print(logging, inspect, Parameter, create_model, load_dotenv, os)

from code_autoeval.clients.llm_model.llm_model import LLMModel

#%%


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

    content, result, expected_output, context = await llm_model_client.code_generator(
        query, AbstractClass.sum_of_numbers, verbose=True, debug=True
    )

    print("Final generated code:", content)
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
        content, result, expected_output, context = await llm_model_client.code_generator(
            query, function, verbose=True
        )

        # Clean up the expected output
        expected_output = expected_output.strip()
        expected_output = re.sub(r"^```|```$", "", expected_output).strip()

        print("Query:", query)
        print("Final generated code:", content)
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
asyncio.run(main())


#%%

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

    code, serialized_result, expected_output, context, pytest_tests = await llm_model_client.code_generator(
            query, function_to_implement, goal=goal, verbose=True, debug=True, skip_generate_fake_data=skip_generate_fake_data
        )


# Run the async main function
asyncio.run(main2())


# %%


# %%
