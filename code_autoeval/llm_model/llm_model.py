"""LLM Backend Client Model."""

from pprint import pprint
from typing import Any, Callable, Dict, Optional, Tuple

import pandas as pd
from multiuse.model import class_data_model

from code_autoeval.llm_model.utils import (
    execute_generated_code,
    execute_unit_tests,
    extraction,
    generate_fake_data,
    model,
)
from code_autoeval.model.backend_model_kwargs import BackendModelKwargs


class LLMModel(
    execute_generated_code.ExecuteGeneratedCode,
    execute_unit_tests.ExecuteUnitTests,
    extraction.extract_context_from_exception.ExtractContextFromException,
    generate_fake_data.GenerateFakeData,
):
    """LLM Backend Client Model."""

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
        class_model: Optional[class_data_model.ClassDataModel] = None,
    ) -> Tuple[str, Any, Dict[str, Any], str]:
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
        self.unique_imports_dict: Dict[str, str] = (
            extraction.find_imports_from_dir.FindImportsFromDir.find_unique_imports_from_dir()
        )
        function_attributes = (
            model.function_attributes.FunctionAttributesFactory.create(
                func, self.common.generated_base_dir, class_model
            )
        )
        # Extract function attributes
        self.init_kwargs.__dict__.update(**function_attributes.__dict__)
        self.init_kwargs.debug = debug
        self.init_kwargs.verbose = verbose

        # Replace the self.common class_logger with the class_model class
        self.common.class_logger = class_model.class_logger

        error_message = ""
        error_formatter = (
            extraction.extract_context_from_exception.ExtractContextFromException()
        )
        code = ""
        pytest_tests = ""
        unit_test_coverage_missing: Dict[str, Any] = {}
        goal = goal or ""
        system_prompt = self.generate_system_prompt(
            query, goal, function_attributes, class_model=class_model
        )

        self._log_code(system_prompt, intro_message="System prompt")

        # Generate fake data if needed - if valid df then this will get skipped.
        df = self.generate_fake_data(
            func,
            df,
            debug=self.init_kwargs.debug,
            skip_generate_fake_data=skip_generate_fake_data,
        )

        for attempt in range(max_retries):
            try:
                if return_tuple := self.parse_existing_tests_or_raise_exception(
                    function_attributes, df, class_model, attempt, error_message
                ):
                    # If the first item of the return dict is valid, then return it.
                    if return_tuple[0]:
                        return return_tuple

                if (
                    attempt == 0
                    or not function_attributes.test_absolute_file_path.exists()
                ):
                    c = await self.ask_backend_model(query, system_prompt=system_prompt)
                else:
                    coverage_report = (
                        self.get_coverage_report(
                            function_name=self.init_kwargs.func_name
                        )
                        if "coverage is not 100%" in error_message
                        else None
                    )

                    clarification_prompt = self.generate_clarification_prompt(
                        query,
                        error_message,
                        coverage_report=coverage_report,
                        previous_code=code,
                        pytest_tests=pytest_tests,
                        unit_test_coverage_missing=unit_test_coverage_missing,
                        function_attributes=function_attributes,
                    )
                    c = await self.ask_backend_model(
                        clarification_prompt,
                        system_prompt=system_prompt,
                    )

                content = self.figure_out_model_response(c)

                # Removing - need a flag for is_pytest generation vs is code generation
                # self.validate_func_name_in_code(content, self.init_kwargs.func_name)
                self._log_code(content, intro_message="Raw content from model")

                code, pytest_tests = self.split_content_from_model(content)

                if code != pytest_tests:
                    self._log_code(code, intro_message="Split result - code")
                self._log_code(
                    pytest_tests, intro_message="Split result - pytest_tests"
                )

                if class_model:
                    result, context = {}, {}
                else:
                    # Execute the generated code
                    result, context = self.execute_generated_code(
                        code,
                        func=func,
                        df=df,
                        debug=debug,
                    )

                # Write code and tests to files
                self.write_code_and_tests(
                    code, pytest_tests, func, class_model, function_attributes
                )

                unit_test_coverage_missing = self.run_tests(
                    self.init_kwargs.func_name,
                    function_attributes.module_absolute_path,
                    function_attributes.test_absolute_file_path,
                    df,
                    class_model=class_model,
                )

                if not unit_test_coverage_missing:
                    return (
                        code,
                        self.serialize_dataframe(result),
                        context,
                        pytest_tests,
                    )
                else:
                    raise model.custom_exceptions.MissingCoverageException(
                        "Tests failed or coverage is not 100%"
                    )

            # Catch alls for code - formatting errors.
            except model.custom_exceptions.FormattingError as se:

                file_path_to_remove = function_attributes.test_absolute_file_path
                self._log_code(
                    f"Attempt {attempt + 1} - removing test {file_path_to_remove=} - {se}",
                    "Syntax error: ",
                )
                # Remove the file and try again from the beginning
                file_path_to_remove.unlink(missing_ok=True)
                continue

            except model.custom_exceptions.MissingCoverageException as e:
                error_message = str(e)
                self._log_code(
                    f"Attempt {attempt + 1} - {error_message}",
                    "Insufficient coverage: ",
                )
                # Pass the error message to the next iteration
                continue
            except Exception as e:
                formatted_error = error_formatter.format_error(e)
                error_message = error_formatter.create_llm_error_prompt(formatted_error)

                # Now let's add in the context for what caused this error - including
                # the line numbers and the code that was generated.
                if debug:
                    print(
                        f"Attempt {attempt + 1} - Error executing generated code {error_message}"
                    )
                    pprint(formatted_error)
                # Pass the error message to the next iteration
                continue

        self._log_max_retries(max_retries)

        return code, None, {}, pytest_tests
