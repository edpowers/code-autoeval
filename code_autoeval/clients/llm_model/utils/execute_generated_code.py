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
    find_parent_class,
    preprocess_code_before_execution,
    serializing_dataframes,
    validation,
)


class ExecuteGeneratedCode(
    serializing_dataframes.SerializeDataframes,
    preprocess_code_before_execution.PreProcessCodeBeforeExecution,
    find_parent_class.FindParentClass,
    validation.validate_regexes.ValidateRegexes,
):

    imported_libraries: set = set()

    def get_imported_libraries(self) -> set:
        """Return the set of imported libraries."""
        return self.imported_libraries

    def execute_generated_code(
        self,
        original_code: str,
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
        # Create a new dictionary for local variables
        local_vars = {}

        self._log_code(original_code, "Original code:")
        # Remove markdown code blocks if present
        code = self.remove_non_code_patterns(
            original_code, code_type="function", func_name=self.init_kwargs.func_name
        )
        # Format the code using Black
        # formatted_code = self.format_code_with_black(
        #    code, code_type="function", func_name=self.init_kwargs.func_name
        # )

        self._log_code(formatted_code, "Formatted code:")

        # Add necessary imports and functions to the global scope
        global_vars = {
            "pd": pd,
            "np": np,
            "deserialize_dataframe": self.deserialize_dataframe,
            "logging": logging,  # Add logging explicitly
            "os": os,  # Add os explicitly
            "re": re,  # Add re explicitly
            "subprocess": subprocess,  # Add subprocess explicitly
            "sys": sys,  # Add sys explicitly
            "tempfile": tempfile,  # Add tempfile explicitly
            "importlib": importlib,  # Add importlib explicitly
            "inspect": inspect,  # Add inspect explicitly
        }

        # Add all previously imported libraries
        for lib in self.imported_libraries:
            global_vars[lib] = importlib.import_module(lib)

        # Add the input dataframe to the local variables if provided
        if df is not None:
            local_vars["df"] = df

        # Extract import statements
        imports = self.extract_imports(code)

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

            # Find and extract the target in the code
            method_name = func.__name__.split(".")[-1]
            # Find the target in the code
            target_node = self.find_target_in_code(
                main_code,
                method_name,
            )
            # Target source
            target_source, parent_class_name = self.find_and_extract_target(
                main_code, self.init_kwargs.func_name
            )

            self.validate_target_node(target_node, self.init_kwargs.func_name)

            exec(main_code, global_vars, local_vars)

            # self.func_name = self._find_func_name(func, local_vars)

            # Update local variable names to avoid conflicts
            local_vars = self.update_local_var_names(local_vars)

            if parent_class_name:
                self.validate_class_name_in_local_vars(parent_class_name, local_vars)

                parent_class = local_vars[parent_class_name]
                instance = parent_class()
                generated_func = getattr(instance, method_name)

                # Wrap the method to handle 'self' automatically
                def wrapped_method(*args, **kwargs):
                    return generated_func(*args, **kwargs)

                generated_func = wrapped_method
                # return wrapped_method, local_vars
            else:
                # Let's also make sure that the split function is in the local_vars
                parts = self.init_kwargs.func_name.split(".") + [
                    self.init_kwargs.func_name
                ]
                if not any(part in local_vars for part in parts):
                    # If the function is not in local_vars, explicitly execute its source
                    exec(target_source, global_vars, local_vars)

                if len(parts) == 3:
                    # It's a method
                    class_name, method_name = parts[:2]
                    class_obj = local_vars[class_name]
                    generated_func = getattr(class_obj, method_name)
                else:
                    generated_func = local_vars[func.__name__]

            # If it's a class, we need to get the method
            # if isinstance(target_node, ast.ClassDef):
            #    class_obj = local_vars[func.__name__]
            #   method_name = func.__name__.split(".")[-1]  # Get the method name
            #    generated_func = getattr(class_obj, method_name)
            # elif "." in func.__name__:
            #    # It's a method
            #    class_name, method_name = func.__name__.split(".")
            #    class_obj = local_vars[class_name]
            #    generated_func = getattr(class_obj, method_name)
            # else:
            #     generated_func = local_vars[func.__name__]

            # Get the generated function
            # generated_func: Callable = local_vars[self.func_name]

            # Find the arguments for the generated function
            args = self.find_args_for_generated_function(generated_func, df, debug)
            # Call the function with the prepared arguments
            # Deserialize the result if it's a DataFrame
            result = self.deserialize_dataframe(generated_func(*args))

            # Get the context (all variables in the local scope)
            # Deserialize any DataFrames in the context
            context = {
                k: self.deserialize_dataframe(v)
                for k, v in local_vars.items()
                if not k.startswith("__") and k != "df"
            }

            return result, context

        except Exception as e:
            raise Exception(
                f"Error executing code: {str(e)}\n Code:\n {formatted_code}"
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

            self._log_code("\n".join(self.imported_libraries), "Imported libraries:")

    def extract_imports(self, code: str) -> str:
        import_lines = [
            line
            for line in code.split("\n")
            if line.strip().startswith("import ") or line.strip().startswith("from ")
        ]

        self._log_code("\n".join(import_lines), "Extracted imports:")

        return "\n".join(import_lines)

    def _find_func_name(self, func: Callable, local_vars: dict) -> str:
        # Find the function name
        func_name = func.__name__

        if func_name not in local_vars:
            pass
            # raise ValueError(f"Function '{func_name}' not found in the executed code.")
        elif not callable(local_vars[func_name]):
            raise ValueError(f"'{func_name}' is not a callable function in the code.")

        return func_name

    def find_args_for_generated_function(
        self, generated_func: Callable, df: pd.DataFrame, debug: bool = False
    ) -> List[str | pd.DataFrame]:
        """Find the arguments for the generated function."""
        # Prepare arguments for the function call
        sig = inspect.signature(generated_func)
        args = []

        if not sig.parameters:
            return args

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
            elif str(param) in ["*args", "**kwargs"]:
                # Skip these parameters
                continue
            else:
                print(f"Unable to determine value for parameter '{param_name}'")
                # For other cases, raise an error
                # raise ValueError(  # TODO: Add back errors.
                #    f"Unable to determine value for parameter '{param_name}'"
                # )

        if debug:
            print(f"Calling {self.init_kwargs.func_name} with args: {args}")

        return args
