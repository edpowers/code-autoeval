"""LLM Backend Client Model."""

import re
import traceback
from typing import Any, Callable, Dict, Optional, Tuple

import pandas as pd
from IPython.display import display

# from code_autoeval.model.backend_model_kwargs import BackendModelKwargs
from code_autoeval.clients.llm_model.utils.decipher_response import DeciperResponse
from code_autoeval.clients.llm_model.utils.execute_generated_code import (
    ExecuteGeneratedCode,
)
from code_autoeval.clients.llm_model.utils.execute_unit_tests import ExecuteUnitTests
from code_autoeval.clients.llm_model.utils.generate_fake_data import GenerateFakeData
from code_autoeval.clients.llm_model.utils.serializing_dataframes import (
    SerializeDataframes,
)
from code_autoeval.clients.llm_model.utils.system_prompts import SystemPrompts
from code_autoeval.model.backend_model_kwargs import BackendModelKwargs


class LLMModel(GenerateFakeData, DeciperResponse, SystemPrompts, ExecuteGeneratedCode, SerializeDataframes, ExecuteUnitTests):
    """LLM Backend Client Model."""

    func_name: str = ""

    def __init__(self, **kwargs: BackendModelKwargs) -> None:
        """Initialize the LLM Backend Client Model."""
        super().__init__(**kwargs)


    async def code_generator(
        self,
        query: str,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        goal: Optional[str] = None,
        verbose: bool = True,
        debug: bool = False,
        max_retries: int = 3,
        skip_generate_fake_data: bool = False,
    ) -> Tuple[str, Any, str, Dict[str, Any], str]:
        """
        Generates Python code based on the query, provided function, and optional dataframe.

        :param query: The user's query describing the desired functionality
        :param func: The function to be implemented
        :param df: Optional dataframe to use for testing and validation
        :param goal: Optional specific goal for the function (e.g., "replace every instance of 'Australia'")
        :param verbose: Whether to print verbose output
        :param debug: Whether to print debug information
        :param max_retries: Maximum number of retries for code generation
        :param skip_generate_fake_data: Whether to skip generating fake data
        """
        function_signature = f"def {func.__name__}{func.__annotations__}"
        function_docstring = f'"""{func.__doc__}"""' if func.__doc__ else ""
        self.func_name = func.__name__
        self.base_dir = "generated_code"
        error_message = ""
        code = ""
        expected_output = ""
        pytest_tests = ""
        goal = goal or ""
        system_prompt = self.generate_system_prompt(
            query, goal, function_signature, function_docstring
        )

        # Generate fake data if needed
        df = await self.generate_fake_data(func, df, debug, skip_generate_fake_data=skip_generate_fake_data)

        for attempt in range(max_retries):
            if attempt > 0:

                coverage_report = self.get_coverage_report(function_name=self.func_name) if "coverage is not 100%" in error_message else None

                clarification_prompt = self.generate_clarification_prompt(
                    query,
                    self.func_name,
                    function_signature,
                    function_docstring,
                    error_message,
                    coverage_report=coverage_report,
                    previous_code=code,
                    pytest_tests=pytest_tests,
                )
                c = await self.ask_backend_model(
                    clarification_prompt,
                    system_prompt=system_prompt,
                    model="coder-lite:latest",
                )
            else:
                c = await self.ask_backend_model(
                    query, system_prompt=system_prompt, model="coder-lite:latest"
                )
            content = self.figure_out_model_response(c)

            if debug:
                print("Raw content from model:\n", content)  # Debug print

            # Split the content into code, expected output, and pytest tests
            parts = re.split(r"[# ]{0,2}Expected Output:|import pytest", content, maxsplit=2)
            if len(parts) == 3:
                code, expected_output, pytest_tests = parts
                pytest_tests = "import pytest\n" + pytest_tests
            elif len(parts) == 2:
                code, expected_output = parts
            else:
                code = content
                expected_output = "Expected output not provided"

            # Clean up the expected output
            expected_output = re.sub(r"^```|```$|,", "", expected_output.strip()).strip()

            try:
                # Execute the generated code
                result, context = self.execute_generated_code(code, func=func, df=df, debug=debug)

                # Serialize the result if it's a DataFrame
                serialized_result = self.serialize_dataframe(result)

                if verbose:
                    print(f"Execution result: {serialized_result}")

                # Write code and tests to files
                self.write_code_and_tests(code, pytest_tests, self.func_name)

                # Run pytest with coverage
                tests_passed = self.run_tests(self.func_name, df)

                # Verify the goal if specified
                # TODO: Fix with real implementation.
                # if goal and not self.verify_goal(result, goal, df):
                #    raise Exception("Generated code does not meet the specified goal")

                # Run pytest with coverage
                if not tests_passed:
                    raise Exception("Tests failed or coverage is not 100%")

                return code, serialized_result, expected_output, context, pytest_tests
            except Exception as e:
                error_message = f"Error: {str(e)}"
                if debug:
                    print(
                        f"Attempt {attempt + 1} - Error executing generated code or insufficient coverage: {error_message}"
                    )
                    display(traceback.format_exc())
                # Pass the error message to the next iteration
                continue

        # If we've exhausted all retries
        if verbose:
            print(f"Failed to generate correct code with 100% coverage after {max_retries} attempts.")
        return code, None, expected_output, {}, pytest_tests