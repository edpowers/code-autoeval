"""Validate regexes - that something isn't missing."""

import functools
from typing import Any, Callable


class ValidateRegexes:
    """Validate the results of the regexes."""

    def validate_func_in_code(self, code: str, func: Callable) -> None:
        """Validate that the function is in the code."""
        self.validate_func_name_in_code(code, func.__name__)

    def validate_func_name_in_code(self, code: str, func_name: str) -> None:
        """Validate that the function name is in the code."""
        if ".__init__" in func_name:
            func_name = func_name.split(".__init__")[0]

        if func_name not in code:
            raise ValueError(
                f"Function name '{func_name}' not found in the formatted code."
            )

    def validate_test_in_pytest_code(self, pytest_code: str) -> None:
        """Validate that the test is in the pytest code."""
        if "def test_" not in pytest_code:
            raise ValueError(f"pytest_tests must be in {pytest_code}")

    def validate_target_node(self, target_node: Any, func_name: str) -> None:
        """Validate target node."""
        if target_node is None:
            raise ValueError(f"Target node not found for function {func_name}")

    def validate_class_name_in_local_vars(
        self,
        class_name: str,
        local_vars: dict,
    ) -> None:
        """Validate that the parent name class is in the local vars."""
        if class_name not in local_vars:
            raise ValueError(
                f"Parent class name '{class_name}' not found in the local vars."
            )


def validate_code() -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(
            *args: Any, code_type: str = "", func_name: str = "", **kwargs: Any
        ) -> Any:
            """Validate the code.

            Kwargs
            ------
            code_type (str, default = "")
                The type of code to validate. Must be 'function' or 'pytest'
            """
            validator = ValidateRegexes()
            result = func(*args, **kwargs)

            if isinstance(result, tuple) and len(result) == 2:
                code, pytest_code = result
            elif isinstance(result, str):
                code = result
                pytest_code = None
            else:
                raise ValueError(
                    "Function must return either (code, pytest_code) or just code"
                )

            if (
                code_type == "function" and func_name
            ):  # Validate the function in the code
                validator.validate_func_name_in_code(code, func_name)
            elif code_type == "function":
                validator.validate_func_in_code(code, func)
            elif code_type == "pytest":
                validator.validate_test_in_pytest_code(pytest_code or code)

            return result

        return wrapper

    return decorator
