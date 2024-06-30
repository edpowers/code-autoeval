"""Extract the function attributes."""

import inspect
from typing import Callable

from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.clients.llm_model.utils.model.function_attributes import (
    FunctionAttributes,
)


def get_function_name(func: Callable, class_model: ClassDataModel = None) -> str:
    """Extract the function name."""
    return f"{class_model.class_name}.{func.__name__}" if class_model else func.__name__


def get_function_signature(func: Callable) -> str:
    """Extract the function signature."""
    return str(inspect.signature(func))


def get_function_docstring(func: Callable) -> str:
    """Extract the function docstring."""
    return inspect.getdoc(func) or ""


def get_function_body(func: Callable) -> str:
    """Extract the function body."""
    source_lines = inspect.getsourcelines(func)[0]
    # Remove decorator lines, if any
    while source_lines and source_lines[0].strip().startswith("@"):
        source_lines.pop(0)
    # Remove the function definition line
    source_lines.pop(0)
    # Remove docstring lines
    if source_lines and source_lines[0].strip().startswith('"""'):
        while source_lines and not source_lines.pop(0).strip().endswith('"""'):
            pass
    # Join the remaining lines and dedent
    return inspect.cleandoc("\n".join(source_lines))


def extract_function_attributes(
    func: Callable, class_model: ClassDataModel = None
) -> FunctionAttributes:
    """
    Extract all relevant attributes from a given function.

    Args:
        func (Callable): The function to extract attributes from.

    Returns:
        FunctionAttributes: A model containing all extracted function attributes.
    """
    return FunctionAttributes(
        func_name=get_function_name(func, class_model=class_model),
        function_signature=get_function_signature(func),
        function_docstring=get_function_docstring(func),
        function_body=get_function_body(func),
        init_params=class_model.init_params if class_model else [],
        class_attributes=class_model.class_attributes if class_model else [],
        base_classes=class_model.base_classes if class_model else [],
        absolute_path=class_model.absolute_path if class_model else "",
    )
