"""Generate Fake Data."""

import random
import re
from typing import Any, Callable, Optional

import black
import pandas as pd
from faker import Faker

from code_autoeval.clients.llm_model.utils.preprocess_code_before_execution import (
    PreProcessCodeBeforeExecution,
)
from code_autoeval.clients.llm_model.utils.stream_response import StreamResponse


class GenerateFakeData(StreamResponse, PreProcessCodeBeforeExecution):
    """Generate the fake data."""

    async def generate_fake_data(self,func: Callable[..., Any], df: Optional[pd.DataFrame] = None, debug: bool = False, skip_generate_fake_data: bool = False) -> pd.DataFrame:
        """
        Generate fake data based on the function signature if needed.
        """
        if df is not None or skip_generate_fake_data:
            return df

        function_signature = f"def {func.__name__}{func.__annotations__}"
        function_docstring = f'"""{func.__doc__}"""' if func.__doc__ else ""

        fake_data_prompt = f"""
        Generate a Python script to create fake data for the following function:
        {function_signature}
        {function_docstring}
        Use only the Faker library to generate appropriate fake data.
        Create a pandas DataFrame named 'fake_data' containing the generated data.
        Ensure the generated data is diverse and suitable for testing the function.
        Do not use PandasProvider or any other external libraries besides Faker, random, and pandas.
        """

        fake_data_response = await self.ask_backend_model(
            fake_data_prompt, system_prompt=""
        )

        content = self.figure_out_model_response_for_faker(fake_data_response)

        if debug:
            print("Raw content from model:\n", content)

        # Extract the code part
        parts = re.split(r"[# ]{0,2}Expected Output:|### Expected Output:", content, maxsplit=1)
        code = parts[0].strip()

        code = self.clean_code(code)
        code = self.preprocess_code(code)

        # Format the code using Black
        try:
            code = black.format_str(code, mode=black.FileMode())
        except black.InvalidInput as e:
            raise Exception(f"Error formatting code: {str(e)}\nCode:\n{code}") from e

        try:
            # Set up the execution environment
            local_vars = {'pd': pd, 'Faker': Faker, 'random': random}

            # Execute the code
            exec(code, local_vars)

            # Retrieve the generated fake_data
            fake_data = local_vars.get('fake_data')

            if not isinstance(fake_data, pd.DataFrame):
                raise ValueError("The generated fake data is not a pandas DataFrame")

            if debug:
                print("\nGenerated fake DataFrame:")
                print(fake_data)
                print()

            return fake_data

        except Exception as e:
            raise Exception(f"Error creating fake data: {str(e)}\nCode:\n{code}")

    def figure_out_model_response_for_faker(self, response: Any) -> str:
        """
        Extract the content from the model's response.
        """
        if isinstance(response, str):
            return response
        elif isinstance(response, dict):
            if 'response' in response:
                return response['response']
            elif 'content' in response:
                return response['content']
        raise ValueError(f"Unexpected response format from the model: {response}")
