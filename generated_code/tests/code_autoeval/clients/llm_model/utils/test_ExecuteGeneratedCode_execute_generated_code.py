import importlib
import inspect
import logging
import subprocess
import sys
import tempfile
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest


class ExecuteGeneratedCode:
    def __init__(self, init_kwargs):
        self.init_kwargs = init_kwargs
        self.imported_libraries = []

    def execute_generated_code(
        self,
        original_code: str,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Executes the generated Python code and returns the result and context.

        :param original_code: The code to execute
        :param func: The original function object
        :param df: Optional dataframe to use in code execution
        :param debug: Whether to print debug information
        :return: A tuple containing the result and the execution context
        """
        local_vars = {}

        self._log_code(original_code, "Original code:")
        # Remove markdown code blocks if present
        code = self.remove_non_code_patterns(
            original_code, code_type="function", func_name=self.init_kwargs.func_name
        )
        self._log_code(code, "Formatted code:")

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

        for lib in self.imported_libraries:
            global_vars[lib] = importlib.import_module(lib)

        if df is not None:
            local_vars["df"] = df

        imports = self.extract_imports_from_gen_code(code)
        exec(imports, global_vars)
        main_code = re.sub(r"^(import|from) .*\n?", "", code, flags=re.MULTILINE)

        try:
            self.import_required_libraries(main_code)
            for lib in self.imported_libraries:
                if lib not in global_vars:
                    global_vars[lib] = importlib.import_module(lib)

            method_name = func.__name__.split(".")[-1]
            target_node = self.find_target_in_code(main_code, method_name)
            target_source, parent_class_name = self.find_and_extract_target(
                main_code, self.init_kwargs.func_name
            )

            self.validate_target_node(target_node, self.init_kwargs.func_name)

            exec(main_code, global_vars, local_vars)

            local_vars = self.update_local_var_names(local_vars)

            if parent_class_name:
                self.validate_class_name_in_local_vars(parent_class_name, local_vars)
                parent_class = local_vars[parent_class_name]
                instance = parent_class()
                generated_func = getattr(instance, method_name)

                def wrapped_method(*args, **kwargs):
                    return generated_func(*args, **kwargs)

                generated_func = wrapped_method
            else:
                parts = self.init_kwargs.func_name.split(".") + [
                    self.init_kwargs.func_name
                ]
                if all(part not in local_vars for part in parts):
                    exec(target_source, global_vars, local_vars)

                if len(parts) == 3:
                    class_name, method_name = parts[:2]
                    class_obj = local_vars[class_name]
                    generated_func = getattr(class_obj, method_name)
                else:
                    generated_func = local_vars[func.__name__]

            args = self.find_args_for_generated_function(generated_func, df, debug)
            result = self.deserialize_dataframe(generated_func(*args))

            context = {
                k: self.deserialize_dataframe(v)
                for k, v in local_vars.items()
                if not k.startswith("__") and k != "df"
            }

            return result, context

        except Exception as e:
            raise Exception(f"Error executing code: {str(e)}\n Code:\n {code}") from e


from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest


class ExecuteGeneratedCode:
    def __init__(self, init_kwargs):
        self.init_kwargs = init_kwargs
        self.imported_libraries = []

    def execute_generated_code(
        self,
        original_code: str,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
    ) -> Tuple[Any, Dict[str, Any]]:
        """
        Executes the generated Python code and returns the result and context.

        :param original_code: The code to execute
        :param func: The original function object
        :param df: Optional dataframe to use in code execution
        :param debug: Whether to print debug information
        :return: A tuple containing the result and the execution context
        """
        local_vars = {}

        self._log_code(original_code, "Original code:")
        # Remove markdown code blocks if present
        code = self.remove_non_code_patterns(
            original_code, code_type="function", func_name=self.init_kwargs.func_name
        )
        self._log_code(code, "Formatted code:")

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

        for lib in self.imported_libraries:
            global_vars[lib] = importlib.import_module(lib)

        if df is not None:
            local_vars["df"] = df

        imports = self.extract_imports_from_gen_code(code)
        exec(imports, global_vars)
        main_code = re.sub(r"^(import|from) .*\n?", "", code, flags=re.MULTILINE)

        try:
            self.import_required_libraries(main_code)
            for lib in self.imported_libraries:
                if lib not in global_vars:
                    global_vars[lib] = importlib.import_module(lib)

            method_name = func.__name__.split(".")[-1]
            target_node = self.find_target_in_code(main_code, method_name)
            target_source, parent_class_name = self.find_and_extract_target(
                main_code, self.init_kwargs.func_name
            )

            self.validate_target_node(target_node, self.init_kwargs.func_name)

            exec(main_code, global_vars, local_vars)

            local_vars = self.update_local_var_names(local_vars)

            if parent_class_name:
                self.validate_class_name_in_local_vars(parent_class_name, local_vars)
                parent_class = local_vars[parent_class_name]
                instance = parent_class()
                generated_func = getattr(instance, method_name)

                def wrapped_method(*args, **kwargs):
                    return generated_func(*args, **kwargs)

                generated_func = wrapped_method
            else:
                parts = self.init_kwargs.func_name.split(".") + [
                    self.init_kwargs.func_name
                ]
                if all(part not in local_vars for part in parts):
                    exec(target_source, global_vars, local_vars)

                if len(parts) == 3:
                    class_name, method_name = parts[:2]
                    class_obj = local_vars[class_name]
                    generated_func = getattr(class_obj, method_name)
                else:
                    generated_func = local_vars[func.__name__]

            args = self.find_args_for_generated_function(generated_func, df, debug)
            result = self.deserialize_dataframe(generated_func(*args))

            context = {
                k: self.deserialize_dataframe(v)
                for k, v in local_vars.items()
                if not k.startswith("__") and k != "df"
            }

            return result, context

        except Exception as e:
            raise Exception(f"Error executing code: {str(e)}\n Code:\n {code}") from e


##################################################
# TESTS
##################################################


@patch(
    "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
    return_value=None,
)
def test_normal_case(mock_init):
    mock_instance = ExecuteGeneratedCode(MagicMock())
    result, context = mock_instance.execute_generated_code(
        "print('Hello, World!')", print
    )
    assert result == None
    assert "df" not in context


@patch(
    "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
    return_value=None,
)
def test_with_dataframe(mock_init):
    df = pd.DataFrame({"A": [1, 2, 3]})
    mock_instance = ExecuteGeneratedCode(MagicMock())
    result, context = mock_instance.execute_generated_code("print(df)", print, df=df)
    assert "df" in context
    assert isinstance(context["df"], pd.DataFrame)
    assert len(context["df"]) == 3


@patch(
    "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
    return_value=None,
)
def test_error_condition(mock_init):
    mock_instance = ExecuteGeneratedCode(MagicMock())
    with pytest.raises(Exception):
        mock_instance.execute_generated_code("non_existent_function()", print)


@patch(
    "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
    return_value=None,
)
def test_debug_logging(mock_init):
    with patch(
        "code_autoeval.llm_model.utils.execute_generated_code.logging.info"
    ) as mock_log:
        mock_instance = ExecuteGeneratedCode(MagicMock())
        mock_instance.execute_generated_code(
            "print('Hello, World!')", print, debug=True
        )
        mock_log.assert_called()


@patch(
    "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
    return_value=None,
)
def test_parent_class(mock_init):
    class ParentClass:
        def method(self):
            return "Hello"

    code = """
    class ChildClass(ParentClass):
        def main(self):
            return self.method()
    """
    mock_instance = ExecuteGeneratedCode(MagicMock())
    result, context = mock_instance.execute_generated_code(code, ParentClass().main)
    assert result == "Hello"
