"""Model for function attributes."""

import asyncio
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

from multiuse.filepaths.system_utils import SystemUtils
from multiuse.model import class_data_model
from pydantic import BaseModel, Field


class FunctionAttributes(BaseModel):
    """Model for function attributes."""

    func_name: str
    function_signature: str
    function_docstring: str
    function_body: str
    function_params: dict[str, Any]
    function_return_type: Any = Field(
        default="Any", description="The return type of the function"
    )
    class_name: str = Field(
        default="",
        description="If the function is a method, this will be the class name",
    )
    method_name: str = Field(
        default="", description="Method name - if the function is a method"
    )
    is_coroutine: bool = Field(
        default=False, description="True if the function is a coroutine (async def)"
    )

    # File paths to the source module containing the function
    module_absolute_path: Path = Field(
        None, description="Absolute path to the module file"
    )

    module_relative_path: Path = Field(
        None, description="Relative path from the project root to the module file"
    )

    module_generated_absolute_path: Path = Field(
        None, description="Absolute path to the generated module file"
    )

    module_generated_relative_path: Path = Field(
        None, description="Relative path to the generated module file"
    )

    # File paths to unit tests generated for the function
    test_relative_file_path: Path = Field(
        None, description="Relative path to the generated test file"
    )
    test_absolute_file_path: Path = Field(
        None, description="Absolute path to the generated test file"
    )


class FunctionAttributesFactory:
    @staticmethod
    def create(
        func: Callable,
        generated_base_dir: Path,
        class_model: Optional[class_data_model.ClassDataModel] = None,
    ) -> FunctionAttributes:
        """
        Extract all relevant attributes from a given function and create a FunctionAttributes instance.

        Args:
            func (Callable): The function to extract attributes from.
            class_model (Optional[class_data_model.ClassDataModel]): The class model if the function is a method.

        Returns:
            FunctionAttributes: A model containing all extracted function attributes.
        """
        func_name = FunctionAttributesFactory._get_function_name(func, class_model)
        class_name, method_name = FunctionAttributesFactory._get_class_and_method_names(
            func_name
        )

        (
            test_relative_file_path,
            test_absolute_file_path,
            generated_relative_file_path,
            generated_absolute_file_path,
        ) = FunctionAttributesFactory._construct_file_paths(
            func_name, class_model.module_relative_path, generated_base_dir
        )

        return FunctionAttributes(
            func_name=func_name,
            function_signature=FunctionAttributesFactory._get_function_signature(func),
            function_params=FunctionAttributesFactory._get_function_params(func),
            function_docstring=FunctionAttributesFactory._get_function_docstring(func),
            function_body=FunctionAttributesFactory._get_function_body(func),
            function_return_type=inspect.signature(func).return_annotation,
            class_name=class_name,
            method_name=method_name,
            is_coroutine=FunctionAttributesFactory._is_coroutine(
                func, class_model, method_name
            ),
            module_absolute_path=class_model.module_absolute_path,
            module_relative_path=class_model.module_relative_path,
            test_relative_file_path=test_relative_file_path,
            test_absolute_file_path=test_absolute_file_path,
            module_generated_absolute_path=generated_absolute_file_path,
            module_generated_relative_path=generated_relative_file_path,
        )

    @staticmethod
    def _get_function_name(
        func: Callable, class_model: Optional[class_data_model.ClassDataModel] = None
    ) -> str:
        """Extract the function name."""
        return (
            f"{class_model.class_name}.{func.__name__}"
            if class_model
            else func.__name__
        )

    @staticmethod
    def _get_class_and_method_names(func_name: str) -> tuple[str, str]:
        """Extract class and method names from the full function name."""
        parts = func_name.split(".")
        return (".".join(parts[:-1]), parts[-1]) if len(parts) > 1 else ("", func_name)

    @staticmethod
    def _get_function_signature(func: Callable) -> str:
        """Extract the function signature."""
        return str(inspect.signature(func))

    @staticmethod
    def _get_function_docstring(func: Callable) -> str:
        """Extract the function docstring."""
        return inspect.getdoc(func) or ""

    @staticmethod
    def _get_function_body(func: Callable) -> str:
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

    @staticmethod
    def _get_function_params(func: Callable) -> Dict[str, Any]:
        signature = inspect.signature(func)
        params = {}

        for name, param in signature.parameters.items():
            if name in ("self", "cls"):
                params[name] = "instance" if name == "self" else "class"
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                params["*args"] = "tuple"
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                params["**kwargs"] = "dict"
            else:
                annotation = param.annotation
                if annotation is inspect.Parameter.empty:
                    params[name] = Any
                else:
                    params[name] = annotation

        return params

    @staticmethod
    def _is_coroutine(
        func: Callable,
        class_model: Optional[class_data_model.ClassDataModel],
        method_name: str,
    ) -> bool:
        """
        Check if the function is a coroutine.

        This method checks both the function object itself and the ClassDataModel's
        coroutine_methods attribute (if provided) to determine if the function is a coroutine.
        """
        # Check if the function is a coroutine based on its object properties
        if asyncio.iscoroutinefunction(func) or inspect.iscoroutinefunction(func):
            return True

        # If a ClassDataModel is provided, check its coroutine_methods attribute
        if class_model and hasattr(class_model, "coroutine_methods"):
            return method_name in class_model.coroutine_methods

        return False

    @staticmethod
    def _construct_file_paths(
        func_name: str, module_relative_path: Path, generated_base_dir: Path
    ) -> Tuple[Path, Path, Path, Path]:
        # Construct the test file paths
        test_relative_file_path = (
            Path("tests") / module_relative_path.parent / f"test_{func_name}.py"
        )
        # Generated relative file paths
        generated_relative_file_path = (
            generated_base_dir / module_relative_path.parent / f"{func_name}.py"
        )

        # Make the absolute path to the test file
        test_absolute_file_path = generated_base_dir / test_relative_file_path
        # Make the absolute path to the generated file
        generated_absolute_file_path = generated_base_dir / generated_relative_file_path

        # Handle dots in the file name
        if "." in func_name:
            test_relative_file_path = test_relative_file_path.with_stem(
                test_relative_file_path.stem.replace(".", "_")
            )
            test_absolute_file_path = test_absolute_file_path.with_stem(
                test_absolute_file_path.stem.replace(".", "_")
            )
            generated_relative_file_path = generated_relative_file_path.with_stem(
                generated_relative_file_path.stem.replace(".", "_")
            )

            generated_absolute_file_path = generated_absolute_file_path.with_stem(
                generated_absolute_file_path.stem.replace(".", "_")
            )

        # Ensure directories exist
        SystemUtils.make_file_dir(test_absolute_file_path)
        SystemUtils.make_file_dir(generated_absolute_file_path)

        return (
            test_relative_file_path,
            test_absolute_file_path,
            generated_relative_file_path,
            generated_absolute_file_path,
        )
