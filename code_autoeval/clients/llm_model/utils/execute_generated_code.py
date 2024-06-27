"""Execute the generated code."""

import importlib
import inspect
import logging
import os
import re
import subprocess
import sys
import tempfile
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from code_autoeval.clients.llm_model.utils import (
    preprocess_code_before_execution,
    serializing_dataframes,
)


class ExecuteGeneratedCode(
    serializing_dataframes.SerializeDataframes,
    preprocess_code_before_execution.PreProcessCodeBeforeExecution,
):

    imported_libraries: set = set()

    def get_imported_libraries(self) -> set:
        """Return the set of imported libraries."""
        return self.imported_libraries

    def execute_generated_code(
        self,
        code: str,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Executes the generated Python code and returns the result and context.

        :param code: The code to execute
        :param func: The original function object
        :param df: Optional dataframe to use in code execution
        :param debug: Whether to print debug information
        :return: A tuple containing the result and the execution context
        """
        if debug:
            print("Original code:\n", code)  # Debug print

        # Remove markdown code blocks if present
        code = self.clean_code(code)
        # Format the code using Black
        formatted_code = self.format_code_with_black(code)

        if func.__name__ not in formatted_code:
            raise ValueError(
                f"Function name '{func.__name__}' not found in the formatted code."
            )

        if debug:
            print("Formatted code:\n", formatted_code)  # Debug print

        # Create a new dictionary for local variables
        local_vars = {}

        # Add necessary imports and functions to the global scope
        global_vars = {
            "pd": pd,
            "np": np,
            "deserialize_dataframe": self.deserialize_dataframe,
            "logging": logging,  # Add logging explicitly
        }

        # Add all previously imported libraries
        for lib in self.imported_libraries:
            global_vars[lib] = importlib.import_module(lib)

        # Add the input dataframe to the local variables if provided
        if df is not None:
            local_vars["df"] = df

        # Extract import statements
        imports = self.extract_imports(formatted_code)
        print()
        print(f"{imports=}")
        print()
        # Execute imports separately
        exec(imports, global_vars)
        # Remove import statements from the main code
        main_code = re.sub(
            r"^(import|from) .*\n?", "", formatted_code, flags=re.MULTILINE
        )

        # Execute the code
        try:
            # Import required libraries
            self.import_required_libraries(main_code)
            # Update global_vars with newly imported libraries
            for lib in self.imported_libraries:
                if lib not in global_vars:
                    global_vars[lib] = importlib.import_module(lib)

            exec(main_code, global_vars, local_vars)

            self.func_name = self._find_func_name(func, local_vars)

            # Get the generated function
            generated_func: Callable = local_vars[self.func_name]

            # Find the arguments for the generated function
            args = self.find_args_for_generated_function(generated_func, df, debug)

            # Call the function with the prepared arguments
            result = generated_func(*args)

            # Deserialize the result if it's a DataFrame
            result = self.deserialize_dataframe(result)

            # Get the context (all variables in the local scope)
            context = {
                k: v
                for k, v in local_vars.items()
                if not k.startswith("__") and k != "df"
            }

            # Deserialize any DataFrames in the context
            context = {k: self.deserialize_dataframe(v) for k, v in context.items()}

            return result, context

        except Exception as e:
            raise Exception(
                f"Error executing code: {str(e)}\nCode:\n{formatted_code}"
            ) from e

    def import_required_libraries(self, code: str) -> None:
        """Import required libraries based on the generated code."""
        # Run flake8 to get import statements
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            flake8_result = subprocess.run(
                ["flake8", "--select=F401", temp_file_path],
                capture_output=True,
                text=True,
            )

            # Extract library names from flake8 output
            libraries = set()
            for line in flake8_result.stdout.splitlines():
                parts = line.split("'")
                if len(parts) >= 2:
                    lib = parts[1].split(".")[0]
                    libraries.add(lib)

            # Import libraries that are not already imported
            for lib in libraries:
                if lib not in sys.modules and lib not in self.imported_libraries:
                    try:
                        importlib.import_module(lib)
                        self.imported_libraries.add(lib)
                        print(f"Imported {lib}")
                    except ImportError:
                        print(f"Failed to import {lib}")
        finally:
            os.unlink(temp_file_path)

    def extract_imports(self, code: str) -> str:
        import_lines = []
        for line in code.split("\n"):
            if line.strip().startswith("import ") or line.strip().startswith("from "):
                import_lines.append(line)
        return "\n".join(import_lines)

    def _find_func_name(self, func: Callable, local_vars: dict) -> str:
        # Find the function name
        func_name = func.__name__

        if func_name not in local_vars or not callable(local_vars[func_name]):
            raise ValueError(f"Function '{func_name}' not found in the executed code.")

        return func_name

    def find_args_for_generated_function(
        self, generated_func: Callable, df: pd.DataFrame, debug: bool = False
    ) -> List[str | pd.DataFrame]:
        """Find the arguments for the generated function."""
        # Prepare arguments for the function call
        sig = inspect.signature(generated_func)
        args = []
        for param_name, param in sig.parameters.items():
            if param_name == "df":
                if df is not None:
                    args.append(df)
                else:
                    raise ValueError("DataFrame is required but not provided")
            elif param.annotation == str and df is not None and len(df.columns) > 0:
                # Assume string parameters are column names, use the first column if df is provided
                args.append(df.columns[0])
            elif param.default != inspect.Parameter.empty:
                # Use default value if available
                args.append(param.default)
            else:
                # For other cases, raise an error
                raise ValueError(
                    f"Unable to determine value for parameter '{param_name}'"
                )

        if debug:
            print(f"Calling {self.func_name} with args: {args}")

        return args
