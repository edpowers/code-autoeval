"""Example for the code_autoeval client."""

# %%

import asyncio
import sys
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Dict

import nest_asyncio

nest_asyncio.apply()

import pandas as pd
from multiuse.filepaths.find_classes_in_dir import FindClassesInDir
from multiuse.filepaths.find_project_root import FindProjectRoot
from multiuse.filepaths.system_utils import SystemUtils
from multiuse.model import class_data_model

from code_autoeval.llm_model import imports
from code_autoeval.llm_model.hierarchy.creation import create_class_hierarchy
from code_autoeval.llm_model.hierarchy.filtration import filter_class_hierarchy
from code_autoeval.llm_model.hierarchy.fixture_generation.fixture_generator import (
    FixtureGenerator,
)
from code_autoeval.llm_model.utils import extraction
from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass
from code_autoeval.llm_model.utils.model_response.stream_response import StreamResponse


def test_function():
    pass


# %%

created_hierarchy = (
    create_class_hierarchy.CreateClassHierarchy.construct_class_hierarchy()
)

# %%


created_hierarchy.class_hierarchy["LLMModelAttributes"]

# %%


created_hierarchy.filtered_hierarchy["LLMModelAttributes"]


# %%

# Format mock classes for the prompt
# formatted_classes = format_mock_classes_for_prompt(mock_classes, filtered_hierarchy)


# Create fixtures for other classes as needed

# %%

# Example usage
module_path = SystemUtils.get_class_file_path(test_function)

# Find the project root
project_root = FindProjectRoot.find_project_root(module_path)
directory = project_root.joinpath("code_autoeval")

unique_project_imports = imports.FindImportsFromDir.find_unique_imports_from_dir()

all_class_info = FindClassesInDir.find_classes_in_dir(
    str(project_root.joinpath("code_autoeval"))
)

class_data_factory = class_data_model.ClassDataModelFactory(project_root)
class_data_models = class_data_factory.create_from_class_info(all_class_info)

# %%


# %%

created_hierarchy = (
    create_class_hierarchy.CreateClassHierarchy.construct_class_hierarchy()
)
filter_hierarchy_classes = filter_class_hierarchy.FilterClassHierarchy()
filter_hierarchy_classes.build_hierarchy_levels(created_hierarchy.filtered_hierarchy)
hierarchy_levels = filter_hierarchy_classes.get_hierarchy_levels()
flattened_hierachy = filter_hierarchy_classes.flatten_hierarchy()
filter_hierarchy_classes.print_hierarchy_levels()

# %%


# %%


unique_project_imports["BaseModelConfig"]

# %%

test_methods = created_hierarchy.filtered_hierarchy["RunFlake8FixImports"]["methods"]
# test_methods = created_hierarchy.class_hierarchy["RunFlake8FixImports"]["methods"]

for method_name, method_type, inherited in test_methods:
    print(method_name, method_type, inherited)
    if method_name == "run_flake8_pipeline_with_temp_file":
        if method_type != "classmethod":
            raise ValueError(
                "The method run_flake8_pipeline_with_temp_file should be a class method."
            )

# %%

cls_obj = created_hierarchy.class_hierarchy["RunFlake8FixImports"]["class_obj"]

# %%

created_hierarchy.class_hierarchy["BaseLLMClass"]


# %%
# %%


async def main() -> None:
    fixture_gen = FixtureGenerator(
        stream_response=StreamResponse(),
        class_hierarchy=hierarchy_levels,
        class_data_factory=class_data_factory,
        base_output_dir=str(project_root.joinpath("generated_code/fixtures").resolve()),
        project_root=str(project_root),
        clean_output_dir=True,
    )

    await fixture_gen.generate_all_fixtures()

    # Run the main function


nest_asyncio.apply()

asyncio.run(main())

# %%


# %%

IMPORT_BANK = {
    "Path": "from pathlib import Path",
    "logging": "import logging",
    "datetime": "from datetime import datetime",
    "json": "import json",
    "re": "import re",
    "os": "import os",
    "sys": "import sys",
    # Add more as needed
}

class_info = created_hierarchy.filtered_hierarchy["BaseLLMClass"]
level = 4

class_hierarchy = hierarchy_levels

previous_levels = {l: class_hierarchy[l] for l in range(1, level)}


def is_custom_class(cls: type) -> bool:
    """
    Determine if a class is a custom class (not builtin or from standard library).
    """
    if cls.__module__ == "builtins":
        return False
    if cls.__module__.startswith("pydantic"):
        return False
    return cls.__module__ not in sys.stdlib_module_names


# Analyze class attributes to determine necessary imports
necessary_imports = set()
for attr_name, attr_type in class_info["attributes"].items():
    attr_type_str = str(attr_type)
    for type_key, import_statement in IMPORT_BANK.items():
        if type_key in attr_type_str:
            necessary_imports.add(import_statement)

# Create a list of previously defined fixtures
previous_fixtures = [
    f"fixture_mock_{cls.lower()}"
    for lvl in previous_levels.values()
    for cls in lvl.keys()
]

# Identify which parent classes and dependencies have fixtures
parent_fixtures = [
    f"fixture_mock_{parent.__name__.lower()}"
    for parent in class_info["parent_classes"]
    if f"fixture_mock_{parent.__name__.lower()}" in previous_fixtures
]
parent_imports = [
    f"from {parent.__module__} import {parent.__name__}"
    for parent in class_info["parent_classes"]
]

dependency_fixtures = [
    f"fixture_mock_{dep[1].__name__.lower()}"
    for dep in class_info["dependencies"]
    if is_custom_class(dep[1])
    and f"fixture_mock_{dep[1].__name__.lower()}" in previous_fixtures
]

fixture_imports = [
    f"from generated_code.fixtures.fixtures.{fixture.replace('fixture_mock_', '')}_fixture import {fixture}"
    for fixture in parent_fixtures + dependency_fixtures
]

is_pydantic_model = "BaseModel" in [
    parent.__name__ for parent in class_info["parent_classes"]
]

pprint(f"{necessary_imports=}")
pprint(f"{parent_fixtures=}")
pprint(f"{dependency_fixtures=}")
pprint(f"{fixture_imports=}")
pprint(f"{is_pydantic_model=}")


pprint(f"{chr(10).join(sorted(necessary_imports))}")
pprint(f"{chr(10).join(parent_imports)}")
# - Include the following imports for previously defined fixtures:
pprint(f"{chr(10).join(fixture_imports)}")

# %%
# %%


def create_prompt_for_class_level(
    level: int, classes: Dict[str, dict], previous_levels: Dict[int, Dict[str, dict]]
) -> str:
    prompt = f"""
Using the base strategy provided, create pytest fixtures for the following classes at level {level} of the class hierarchy:

"""
    for class_name, class_info in classes.items():
        prompt += f"""
Class Name: {class_name}
Parents: {[parent.__name__ for parent in class_info['parent_classes']]}
Dependencies: {[dep[1].__name__ for dep in class_info['dependencies'] if filter_class_hierarchy.FilterClassHierarchy.is_custom_class(dep[1])]}
Methods: {class_info['methods']}
Attributes: {class_info['attributes']}

Please provide:

1. The fixture file content (fixtures/{class_name.lower()}_fixture.py)
   - Include necessary imports
   - Create a fixture function named mock_{class_name.lower()}
   - Use MagicMock with the spec of the class
   - Mock all methods listed for the class
   - Set all attributes with appropriate default values
   - For parent classes and dependencies, use the fixtures created in previous levels

2. The test file content to verify the fixture (tests/test_{class_name.lower()}_fixture.py)
   - Include necessary imports
   - Create a test function that verifies:
     a. The mock object is an instance of the class
     b. All methods are present and can be called
     c. All attributes are present and have appropriate default values
     d. The object correctly inherits from its parent classes
     e. Dependencies are properly mocked and accessible

3. A brief explanation of what the fixture does, how it uses fixtures from previous levels, and how it can be used in testing

Ensure the code is properly formatted, syntactically correct, and follows Python best practices.

"""
    return prompt


def generate_prompts_for_all_levels(
    hierarchy_levels: Dict[int, Dict[str, dict]]
) -> Dict[int, str]:
    prompts = {}
    for level, classes in hierarchy_levels.items():
        previous_levels = {l: hierarchy_levels[l] for l in range(1, level)}
        prompts[level] = create_prompt_for_class_level(level, classes, previous_levels)
    return prompts


# Usage
hierarchy_levels = filter_hierarchy_classes.get_hierarchy_levels()
all_prompts = generate_prompts_for_all_levels(hierarchy_levels)

for level, prompt in all_prompts.items():
    print(f"Prompt for Level {level}:")
    print(prompt)
    print("-" * 80)


# %%


pprint(list(BaseLLMClass.__dict__.keys()))

# %%


BaseLLMClass.__dict__["model_fields"]


# %%


import inspect
from typing import Any, Dict


def _extract_class_hierarchy(class_object: object) -> Dict[str, Any]:
    def get_class_info(cls: object) -> dict:
        return {
            "parent_classes": [
                base.__name__
                for base in cls.__bases__
                if (base.__name__ not in {"object", "BaseModel"})
            ],
            "methods": [
                name
                for name, obj in inspect.getmembers(cls)
                if inspect.isfunction(obj) and not name.startswith("__")
            ],
            "attributes": [
                name
                for name in cls.__dict__
                if not name.startswith("__")
                and not inspect.isfunction(cls.__dict__[name])
            ]
            + [name for name in cls.__dict__.get("model_fields", [])],
        }

    def traverse_hierarchy(cls: object) -> dict:
        hierarchy = {cls.__name__: get_class_info(cls)}
        for base in cls.__bases__:
            if base.__name__ not in {"object", "BaseModel"}:
                hierarchy.update(traverse_hierarchy(base))
        return hierarchy

    return traverse_hierarchy(class_object)


def _filter_relevant_members(class_info: dict) -> dict:
    pydantic_methods = {
        "model_copy",
        "model_dump",
        "model_dump_json",
        "model_post_init",
        "copy",
        "dict",
        "json",
        "_abc_impl",
        "model_config",
        "model_computed_fields",
    }
    pydantic_attributes = {"model_config", "model_fields", "model_computed_fields"}

    relevant_methods = [
        method
        for method in class_info["methods"]
        if not method.startswith("_")
        and (method not in pydantic_methods and method not in pydantic_attributes)
    ]
    relevant_attributes = [
        attr
        for attr in class_info["attributes"]
        if not attr.startswith("_")
        and (attr not in pydantic_methods and attr not in pydantic_attributes)
    ]

    return {
        "parent_classes": class_info["parent_classes"],
        "methods": relevant_methods,
        "attributes": relevant_attributes,
    }


extracted_hiearchy = _extract_class_hierarchy(LLMModelAttributes)

print("Extracted Hierarchy:")
pprint(extracted_hiearchy)

filtered_hierarchy = extracted_hiearchy.copy()

for class_name, class_info in extracted_hiearchy.items():
    filtered_hierarchy[class_name] = _filter_relevant_members(class_info)


print(f"Filtered Hierarchy:")
pprint(filtered_hierarchy)


# %%

test_str = "code_autoeval.llm_model.llm_model.LLMModel"

test_str.rsplit(".", maxsplit=1)[0]

# %%
# %%


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


# %%


async def main2() -> None:
    query = "Remove outliers from a numerical column in a pandas dataframe with temporal ordering."
    goal = "Refactor code to handle edge cases."

    function_to_implement = AbstractDataFrameClass.remove_outliers
    skip_generate_fake_data = False

    code, serialized_result, expected_output, context, pytest_tests = (
        await llm_model_client.code_generator(
            query,
            function_to_implement,
            df=cleaned_data,
            goal=goal,
            verbose=True,
            debug=True,
            skip_generate_fake_data=skip_generate_fake_data,
        )
    )


# Run the async main function
asyncio.run(main2())


# %%


from pprint import pprint

pprint(
    """import pytest\nfor the `LLMModel.__init__` method:\n\n```python\nimport pytest\nfrom code_autoeval.model import LLMModel, BackendModelKwargs\n\ndef test_normal_case():\n    # Test normal use case with no additional kwargs\n    model = LLMModel()\n    assert hasattr(model, 'kwargs') and model.kwargs is None\n\ndef test_edge_case_with_kwargs():\n    # Test edge case with some kwargs provided\n    kwargs = {'key1': 'value1', 'key2': 42}\n    model = LLMModel(**kwargs)\n    assert hasattr(model, 'kwargs') and model.kwargs == kwargs\n\ndef test_error_condition_with_invalid_arg():\n    # Test error condition with invalid argument type\n    with pytest.raises(TypeError):\n        LLMModel(invalid_arg='not a valid kwarg')\n\ndef test_index_and_data_integrity_with_pandas():\n    # Test that the method handles pandas DataFrame and Series correctly\n    import pandas as pd\n    \n    df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})\n    series = pd.Series([10, 20])\n    \n    model_df = LLMModel(data=df)\n    assert isinstance(model_df.kwargs['data'], pd.DataFrame) and model_df.kwargs['data'].equals(df)\n    \n    model_series = LLMModel(data=series)\n    assert isinstance(model_series.kwargs['data'], pd.Series) and model_series.kwargs['data'].equals(series)\n```\n\nThese tests cover normal use cases, edge cases, and error conditions to ensure the `LLMModel.__init__` method behaves as expected."""
)

# %%

pprint(
    """import pytest\nthe function\ndef test_normal_case():\n    # Normal use case where kwargs are provided\n    model = LLMModel(param1='value1', param2='value2')\n    assert hasattr(model, 'param1') and getattr(model, 'param1') == 'value1'\n    assert hasattr(model, 'param2') and getattr(model, 'param2') == 'value2'\n\ndef test_edge_case_no_kwargs():\n    # Edge case where no kwargs are provided\n    model = LLMModel()\n    assert not hasattr(model, 'param1')\n    assert not hasattr(model, 'param2')\n\ndef test_error_condition_invalid_kwarg():\n    # Error condition where an invalid kwarg is provided\n    with pytest.raises(TypeError):\n        model = LLMModel(invalid_param='value')\n\n# Add more tests to ensure 100% coverage\n```\nThis set of tests ensures that the `LLMModel` class can be initialized correctly with valid and invalid keyword arguments, as well as handle cases where no arguments are provided."""
)

# %%

code = "# REMOVED DUE TO PARSING ERROR: The `LLMModel.__init__` method is a constructor that initializes an instance of the `LLMModel` class, inheriting from its superclass and passing any provided keyword arguments (`**kwargs`) to it. This method does not return anything but sets up the object's state based on the provided parameters.\n\n\n# Assuming LLMModel is defined somewhere in your codebase\nclass LLMModel:\n    def __init__(self, **kwargs):\n        super().__init__(**kwargs)\n"

import ast


def find_target_in_code(code: str, target_name: str) -> ast.AST:
    """
    Parse the code and find the target function or class.

    :param code: The code string to parse
    :param target_name: The name of the function or class to find
    :return: The AST node of the target function or class, or None if not found
    """
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.ClassDef))
            and node.name == target_name
        ):
            return node

    return None


target_name = "LLMModel.__init__"
target_node = find_target_in_code(code, target_name)


# %%
# %%


tree = ast.parse(code)
tree
# %%

for node in ast.walk(tree):
    print(node)

    if isinstance(node, ast.ClassDef):
        break

# %%


display(dir(node))

# %%

node.name

# %%


subprocess.run(
    [
        "pytest",
        "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/clients/llm_model/test_LLMModel.py",
        "-v",
        "--cov=/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/clients/llm_model/test_LLMModel.py",
        "--cov-report=term-missing",
        "--cov-fail-under=100",
    ]
)

# %%
import subprocess

subprocess.run(
    args=[
        "pytest",
        "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/clients/llm_model/test_LLMModel.py",
        "-v",
        "--cov=code_autoeval.llm_model.llm_model.LLMModel",
        "--cov-report=term-missing",
        "--cov-fail-under=100",
    ],
)

# %%

subprocess.run(
    args=[
        "pytest",
        "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/clients/llm_model/test_LLMModel.py",
        "-v",
        "--cov=code_autoeval",
        "--cov-report=term-missing",
        "--cov-fail-under=100",
    ],
)
# %%


subprocess.run(
    args=[
        "pytest",
        "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/clients/llm_model/test_LLMModel.py",
        "-v",
        "--cov=code_autoeval",
        "--cov-report=term-missing",
        "--cov-fail-under=100",
    ],
)


# %%


example = '''import pytest\nimport pandas as pd\nfrom unittest.mock import patch, MagicMock\nfrom typing import Callable, Any, Optional, Dict, Tuple\nimport asyncio\nimport numpy as np\n\nclass LLMModel:\n    def __init__(self):\n        self.unique_imports_dict = {}\n        self.init_kwargs = MagicMock()\n\n    async def code_generator(self, query: str, func: Callable[..., Any], df: Optional[pd.DataFrame] = None, goal: Optional[str] = None, verbose: bool = True, debug: bool = False, max_retries: int = 3, skip_generate_fake_data: bool = False, class_model: \'ClassDataModel\' = None) -> Tuple[str, Any, Dict[str, Any], str]:\n        """\n        Generates Python code based on the query, provided function, and optional dataframe.\n\n        :param query: The user\'s query describing the desired functionality\n        :param func: The function to be implemented\n        :param df: Optional dataframe to use for testing and validation\n        :param goal: Optional specific goal for the function (e.g., "replace every instance of \'Australia\'")\n        :param verbose: Whether to print verbose output\n        :param debug: Whether to print debug information\n        :param max_retries: Maximum number of retries for code generation\n        :param skip_generate_fake_data: Whether to skip generating fake data\n        """\n        self.unique_imports_dict = {}  # Mocking the unique imports dictionary\n        function_attributes = MagicMock()  # Mocking function attributes\n        self.init_kwargs.__dict__.update(**function_attributes.__dict__)\n        self.init_kwargs.debug = debug\n        self.init_kwargs.verbose = verbose\n        error_message = ""\n        code = ""\n        pytest_tests = ""\n        unit_test_coverage_missing: Dict[str, Any] = {}\n        goal = goal or ""\n        system_prompt = self.generate_system_prompt(query, goal, function_attributes, class_model=class_model)  # Mocking the system prompt generation\n\n        df = self.generate_fake_data(func, df, debug=self.init_kwargs.debug, skip_generate_fake_data=skip_generate_fake_data)  # Mocking fake data generation\n\n        for attempt in range(max_retries):\n            try:\n                if return_tuple := self.parse_existing_tests_or_raise_exception(function_attributes, df, debug, class_model, attempt, error_message):\n                    if return_tuple[0]:\n                        return return_tuple\n\n                if attempt == 0 or not function_attributes.test_absolute_file_path.exists():\n                    c = await self.ask_backend_model(query, system_prompt=system_prompt)  # Mocking the backend model query\n                else:\n                    coverage_report = None  # Mocking coverage report generation\n                    clarification_prompt = self.generate_clarification_prompt(query, error_message, coverage_report=coverage_report, previous_code=code, pytest_tests=pytest_tests, unit_test_coverage_missing=unit_test_coverage_missing, function_attributes=function_attributes)  # Mocking clarification prompt generation\n                    c = await self.ask_backend_model(clarification_prompt, system_prompt=system_prompt)  # Mocking the backend model query for clarification\n\n                content = self.figure_out_model_response(c)  # Mocking the model response figure out\n                code, pytest_tests = self.split_content_from_model(content)  # Mocking the content split\n\n                if class_model:\n                    result, context = {}, {}\n                else:\n                    result, context = self.execute_generated_code(code, func=func, df=df, debug=debug)  # Mocking code execution\n\n                self.write_code_and_tests(code, pytest_tests, func, class_model, function_attributes)  # Mocking writing code and tests\n\n                unit_test_coverage_missing = self.run_tests(self.init_kwargs.func_name, function_attributes.module_absolute_path, function_attributes.test_absolute_file_path, df, debug=debug, class_model=class_model)  # Mocking test running\n\n                if not unit_test_coverage_missing:\n                    return code, self.serialize_dataframe(result), context, pytest_tests\n                else:\n                    raise Exception("Tests failed or coverage is not 100%")\n\n            except Exception as e:\n                error_message = str(e)\n                continue\n\n        return code, None, {}, pytest_tests'''

from pprint import pprint

pprint(example)

# %%

example2 = ''''```python\nimport pytest\nimport pandas as pd\nfrom unittest.mock import patch, MagicMock\nfrom typing import Callable, Any, Optional, Dict, Tuple\nimport asyncio\nimport numpy as np\n\nclass LLMModel:\n    def __init__(self):\n        self.unique_imports_dict = {}\n        self.init_kwargs = MagicMock()\n\n    async def code_generator(self, query: str, func: Callable[..., Any], df: Optional[pd.DataFrame] = None, goal: Optional[str] = None, verbose: bool = True, debug: bool = False, max_retries: int = 3, skip_generate_fake_data: bool = False, class_model: \'ClassDataModel\' = None) -> Tuple[str, Any, Dict[str, Any], str]:\n        """\n        Generates Python code based on the query, provided function, and optional dataframe.\n\n        :param query: The user\'s query describing the desired functionality\n        :param func: The function to be implemented\n        :param df: Optional dataframe to use for testing and validation\n        :param goal: Optional specific goal for the function (e.g., "replace every instance of \'Australia\'")\n        :param verbose: Whether to print verbose output\n        :param debug: Whether to print debug information\n        :param max_retries: Maximum number of retries for code generation\n        :param skip_generate_fake_data: Whether to skip generating fake data\n        """\n        self.unique_imports_dict = {}  # Mocking the unique imports dictionary\n        function_attributes = MagicMock()  # Mocking function attributes\n        self.init_kwargs.__dict__.update(**function_attributes.__dict__)\n        self.init_kwargs.debug = debug\n        self.init_kwargs.verbose = verbose\n        error_message = ""\n        code = ""\n        pytest_tests = ""\n        unit_test_coverage_missing: Dict[str, Any] = {}\n        goal = goal or ""\n        system_prompt = self.generate_system_prompt(query, goal, function_attributes, class_model=class_model)  # Mocking the system prompt generation\n\n        df = self.generate_fake_data(func, df, debug=self.init_kwargs.debug, skip_generate_fake_data=skip_generate_fake_data)  # Mocking fake data generation\n\n        for attempt in range(max_retries):\n            try:\n                if return_tuple := self.parse_existing_tests_or_raise_exception(function_attributes, df, debug, class_model, attempt, error_message):\n                    if return_tuple[0]:\n                        return return_tuple\n\n                if attempt == 0 or not function_attributes.test_absolute_file_path.exists():\n                    c = await self.ask_backend_model(query, system_prompt=system_prompt)  # Mocking the backend model query\n                else:\n                    coverage_report = None  # Mocking coverage report generation\n                    clarification_prompt = self.generate_clarification_prompt(query, error_message, coverage_report=coverage_report, previous_code=code, pytest_tests=pytest_tests, unit_test_coverage_missing=unit_test_coverage_missing, function_attributes=function_attributes)  # Mocking clarification prompt generation\n                    c = await self.ask_backend_model(clarification_prompt, system_prompt=system_prompt)  # Mocking the backend model query for clarification\n\n                content = self.figure_out_model_response(c)  # Mocking the model response figure out\n                code, pytest_tests = self.split_content_from_model(content)  # Mocking the content split\n\n                if class_model:\n                    result, context = {}, {}\n                else:\n                    result, context = self.execute_generated_code(code, func=func, df=df, debug=debug)  # Mocking code execution\n\n                self.write_code_and_tests(code, pytest_tests, func, class_model, function_attributes)  # Mocking writing code and tests\n\n                unit_test_coverage_missing = self.run_tests(self.init_kwargs.func_name, function_attributes.module_absolute_path, function_attributes.test_absolute_file_path, df, debug=debug, class_model=class_model)  # Mocking test running\n\n                if not unit_test_coverage_missing:\n                    return code, self.serialize_dataframe(result), context, pytest_tests\n                else:\n                    raise Exception("Tests failed or coverage is not 100%")\n\n            except Exception as e:\n                error_message = str(e)\n                continue\n\n        return code, None, {}, pytest_tests\n```\nThis implementation provides a basic structure for the `code_generator` method of the `LLMModel` class. It includes mocks for all dependencies and functions to ensure that the function can be tested without running into issues with external dependencies or complex logic. The actual functionality would need to be implemented based on the specific requirements and behavior of the `LLMModel` class.'''

pprint(example2)


# %%

system_prompt = ''''\n        You are an expert Python code analyst and test writer.\n        Your task is to analyze an existing Python function and create comprehensive tests for it.\n\n        Follow these instructions carefully:\n\n        1. Function Details:\n        Function Name: LLMModel.code_generator\n        Function is async coroutine: True\n        Signature: (self, query: str, func: Callable[..., Any], df: Optional[pandas.core.frame.DataFrame] = None, goal: Optional[str] = None, verbose: bool = True, debug: bool = False, max_retries: int = 3, skip_generate_fake_data: bool = False, class_model: code_autoeval.llm_model.utils.model.class_data_model.ClassDataModel = None) -> Tuple[str, Any, Dict[str, Any], str]\n        Docstring: Generates Python code based on the query, provided function, and optional dataframe.\n\n:param query: The user\'s query describing the desired functionality\n:param func: The function to be implemented\n:param df: Optional dataframe to use for testing and validation\n:param goal: Optional specific goal for the function (e.g., "replace every instance of \'Australia\'")\n:param verbose: Whether to print verbose output\n:param debug: Whether to print debug information\n:param max_retries: Maximum number of retries for code generation\n:param skip_generate_fake_data: Whether to skip generating fake data\n        Function Body:\n        self,\n\n    query: str,\n\n    func: Callable[..., Any],\n\n    df: Optional[pd.DataFrame] = None,\n\n    goal: Optional[str] = None,\n\n    verbose: bool = True,\n\n    debug: bool = False,\n\n    max_retries: int = 3,\n\n    skip_generate_fake_data: bool = False,\n\n    class_model: model.class_data_model.ClassDataModel = None,\n\n) -> Tuple[str, Any, Dict[str, Any], str]:\n\n    """\n\n    Generates Python code based on the query, provided function, and optional dataframe.\n\n\n\n    :param query: The user\'s query describing the desired functionality\n\n    :param func: The function to be implemented\n\n    :param df: Optional dataframe to use for testing and validation\n\n    :param goal: Optional specific goal for the function (e.g., "replace every instance of \'Australia\'")\n\n    :param verbose: Whether to print verbose output\n\n    :param debug: Whether to print debug information\n\n    :param max_retries: Maximum number of retries for code generation\n\n    :param skip_generate_fake_data: Whether to skip generating fake data\n\n    """\n\n    self.unique_imports_dict: Dict[str, str] = (\n\n        extraction.find_imports_from_dir.FindImportsFromDir.find_unique_imports_from_dir()\n\n    )\n\n    function_attributes = (\n\n        model.function_attributes.FunctionAttributesFactory.create(\n\n            func, self.common.generated_base_dir, class_model\n\n        )\n\n    )\n\n    # Extract function attributes\n\n    self.init_kwargs.__dict__.update(**function_attributes.__dict__)\n\n    self.init_kwargs.debug = debug\n\n    self.init_kwargs.verbose = verbose\n\n    error_message = ""\n\n    error_formatter = (\n\n        extraction.extract_context_from_exception.ExtractContextFromException()\n\n    )\n\n    code = ""\n\n    pytest_tests = ""\n\n    unit_test_coverage_missing: Dict[str, Any] = {}\n\n    goal = goal or ""\n\n    system_prompt = self.generate_system_prompt(\n\n        query, goal, function_attributes, class_model=class_model\n\n    )\n\n\n\n    # Generate fake data if needed - if valid df then this will get skipped.\n\n    df = self.generate_fake_data(\n\n        func,\n\n        df,\n\n        debug=self.init_kwargs.debug,\n\n        skip_generate_fake_data=skip_generate_fake_data,\n\n    )\n\n\n\n    for attempt in range(max_retries):\n\n        try:\n\n            if return_tuple := self.parse_existing_tests_or_raise_exception(\n\n                function_attributes, df, debug, class_model, attempt, error_message\n\n            ):\n\n                # If the first item of the return dict is valid, then return it.\n\n                if return_tuple[0]:\n\n                    return return_tuple\n\n\n\n            if (\n\n                attempt == 0\n\n                or not function_attributes.test_absolute_file_path.exists()\n\n            ):\n\n                c = await self.ask_backend_model(query, system_prompt=system_prompt)\n\n            else:\n\n                coverage_report = (\n\n                    self.get_coverage_report(\n\n                        function_name=self.init_kwargs.func_name\n\n                    )\n\n                    if "coverage is not 100%" in error_message\n\n                    else None\n\n                )\n\n\n\n                clarification_prompt = self.generate_clarification_prompt(\n\n                    query,\n\n                    error_message,\n\n                    coverage_report=coverage_report,\n\n                    previous_code=code,\n\n                    pytest_tests=pytest_tests,\n\n                    unit_test_coverage_missing=unit_test_coverage_missing,\n\n                    function_attributes=function_attributes,\n\n                )\n\n                c = await self.ask_backend_model(\n\n                    clarification_prompt,\n\n                    system_prompt=system_prompt,\n\n                )\n\n\n\n            content = self.figure_out_model_response(c)\n\n\n\n            self.validate_func_name_in_code(content, self.init_kwargs.func_name)\n\n            self._log_code(content, intro_message="Raw content from model")\n\n\n\n            code, pytest_tests = self.split_content_from_model(content)\n\n\n\n            if code != pytest_tests:\n\n                self._log_code(code, intro_message="Split result - code")\n\n            self._log_code(\n\n                pytest_tests, intro_message="Split result - pytest_tests"\n\n            )\n\n\n\n            if class_model:\n\n                result, context = {}, {}\n\n            else:\n\n                # Execute the generated code\n\n                result, context = self.execute_generated_code(\n\n                    code,\n\n                    func=func,\n\n                    df=df,\n\n                    debug=debug,\n\n                )\n\n\n\n            # Write code and tests to files\n\n            self.write_code_and_tests(\n\n                code, pytest_tests, func, class_model, function_attributes\n\n            )\n\n\n\n            unit_test_coverage_missing = self.run_tests(\n\n                self.init_kwargs.func_name,\n\n                function_attributes.module_absolute_path,\n\n                function_attributes.test_absolute_file_path,\n\n                df,\n\n                debug=debug,\n\n                class_model=class_model,\n\n            )\n\n\n\n            if not unit_test_coverage_missing:\n\n                return (\n\n                    code,\n\n                    self.serialize_dataframe(result),\n\n                    context,\n\n                    pytest_tests,\n\n                )\n\n            else:\n\n                raise execute_unit_tests.MissingCoverageException(\n\n                    "Tests failed or coverage is not 100%"\n\n                )\n\n\n\n        # Catch alls for code - formatting errors.\n\n        except execute_unit_tests.FormattingError as se:\n\n\n\n            file_path_to_remove = function_attributes.test_absolute_file_path\n\n            self._log_code(\n\n                f"Attempt {attempt + 1} - removing test {file_path_to_remove=} - {se}",\n\n                "Syntax error: ",\n\n            )\n\n            # Remove the file and try again from the beginning\n\n            file_path_to_remove.unlink(missing_ok=True)\n\n            continue\n\n\n\n        except execute_unit_tests.MissingCoverageException as e:\n\n            error_message = str(e)\n\n            self._log_code(\n\n                f"Attempt {attempt + 1} - {error_message}",\n\n                "Insufficient coverage: ",\n\n            )\n\n            # Pass the error message to the next iteration\n\n            continue\n\n        except Exception as e:\n\n            formatted_error = error_formatter.format_error(e)\n\n            error_message = error_formatter.create_llm_error_prompt(formatted_error)\n\n\n\n            # Now let\'s add in the context for what caused this error - including\n\n            # the line numbers and the code that was generated.\n\n            if debug:\n\n                print(\n\n                    f"Attempt {attempt + 1} - Error executing generated code {error_message}"\n\n                )\n\n                pprint(formatted_error)\n\n            # Pass the error message to the next iteration\n\n            continue\n\n\n\n    self._log_max_retries(max_retries)\n\n\n\n    return code, None, {}, pytest_tests\n\n        If there are base classes, initialization parameters, or class attributes,\n        please mock all of the dependencies so that we can properly unit test.\n        Use unittest.mock or any other pytest.patch method to mock these dependencies.\n\n        Please use the following relative path provided for all mocking:\n        code_autoeval.llm_model.llm_model.LLMModel\n\n        Function Base Classes:\n        [\'DeciperResponse\', \'ExecuteGeneratedCode\', \'ExecuteUnitTests\', \'ExtractContextFromException\', \'GenerateFakeData\']\n\n        Initialization Parameters:\n        [\'kwargs\']\n\n        Class Attributes:\n        [\'_abc_impl\', \'model_computed_fields\', \'model_config\', \'model_extra\', \'model_fields\', \'model_fields_set\']\n\n        Mocking __init__ functions should return None, like the following:\n        @patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)\n\n        2. Task: Implement the code_generator method for the LLMModel class. - with Refactor code to handle edge cases and improve efficiency.\n\n        \n        3. Code Generation Guidelines:\n        - Implement the function according to the given signature.\n        - Ensure all function arguments have their types explicitly mentioned.\n        - Create any necessary additional code to solve the task.\n        - Ensure the code is efficient, readable, and follows Python best practices.\n        - Include proper error handling if appropriate.\n        - Add brief, inline comments for clarity if needed.\n        - If any of the function args are pandas.DataFrame, pandas.Series, verify the index.\n\n        4. Test Generation Guidelines:\n        - Create pytest tests for the function.\n        - Write at least 5 test functions covering different scenarios, including:\n            a) Normal use cases\n            b) Edge cases\n            c) Potential error conditions\n        - Ensure 100% code coverage for the function being tested.\n        - If any of the function args are pandas.DataFrame or pandas.Series, include tests that verify the index and data integrity.\n\n        When writing pytest tests, please adhere to the following guidelines:\n\n        1. Only use variables that are explicitly defined within each test function.\n        2. Avoid relying on global variables or undefined mocks.\n        3. If you need to mock a method or function, define the mock within the test function using pytest.mock.patch as a decorator or context manager.\n        4. Ensure that each test function is self-contained and does not depend on the state from other tests.\n        5. Use descriptive names for test functions that clearly indicate what is being tested.\n        6. Follow the Arrange-Act-Assert (AAA) pattern in your tests:\n        - Arrange: Set up the test data and conditions.\n        - Act: Perform the action being tested.\n        - Assert: Check that the results are as expected.\n        7. Use assert statements to verify the expected behavior.\n        8. When testing for exceptions, use pytest.raises() as a context manager.\n        9. Do not use any fixtures that are not explicitly defined within the test file or imported from a known source. Specifically:\n            - Do not use a \'setup\' fixture unless you define it in the test file.\n            - Do not use a \'mock_init\' fixture unless you explicitly define it.\n            - If you need setup or teardown operations, include them directly in the test functions or use pytest\'s built-in fixtures like \'tmp_path\' or \'capsys\'.\n            - If mocking is required, create the mocks within each test function using pytest.mock.patch as a decorator or context manager.\n        \n\n        if function_attributes.is_coroutine=True, then use pytest-asyncio to test async functions.\n        For example:\n        @pytest.mark.asyncio\n        async def test_async_function():\n            result = await your_async_function()\n            assert result == expected_value\n\n        5. Output Format:\n        - Provide a brief analysis of the function (2-3 sentences).\n        - Then, provide the pytest tests.\n\n        Example of expected response format:\n\n        ```python\n        # Expected Output: 7\n\n        import pytest\n        import pandas as pd\n        import numpy as np\n\n        def example_func_provided(arg1: int, arg2: int) -> int:\n            # Your code here\n            result = arg1 + arg2\n            return result\n\n        # Test the function\n        print(example_func_provided(3, 4))\n\n        ##################################################\n        # TESTS\n        ##################################################\n\n        def test_normal_case():\n            # Test normal use case\n            assert function_name(normal_args) == expected_output\n\n        def test_edge_case_1():\n            # Test an edge case\n            assert function_name(edge_case_args) == expected_edge_output\n\n        def test_error_condition():\n            # Test an error condition\n            with pytest.raises(ExpectedErrorType):\n                function_name(error_inducing_args)\n\n        # Add more tests to ensure 100% coverage\n        '''

pprint(system_prompt)


# %%
# %%
from pprint import pprint

pprint(
    '''import tempfile\nfrom typing import Optional\nimport pandas as pd\n\nclass SerializeDataframes:\n    def store_df_in_temp_file(self, df: Optional[pd.DataFrame] = None) -> str:\n        """Store the dataframe in a temporary file."""\n        df_path = ""\n\n        # Create a temporary file to store the dataframe if provided\n        if df is not None:\n            with tempfile.NamedTemporaryFile(mode="wb", suffix=".pkl", delete=False) as temp_df_file:\n                df.to_pickle(temp_df_file.name)\n                df_path = temp_df_file.name\n\n        return df_path\n\nimport pytest\nfrom unittest.mock import MagicMock\nimport pandas as pd\n\n@pytest.fixture\ndef mock_serializedataframes():\n    mock = MagicMock(spec=SerializeDataframes)\n    mock.store_df_in_temp_file.return_value = "dummy_path"\n    return mock\n\n# Test case for normal use case where a DataFrame is provided\ndef test_store_df_in_temp_file_normal(mock_serializedataframes):\n    # Arrange\n    instance = mock_serializedataframes\n    df = pd.DataFrame({\'col1\': [1, 2], \'col2\': [\'a\', \'b\']})\n    \n    # Act\n    result = instance.store_df_in_temp_file(df)\n    \n    # Assert\n    assert isinstance(result, str)\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(df)\n\n# Test case for edge case where no DataFrame is provided\ndef test_store_df_in_temp_file_none(mock_serializedataframes):\n    # Arrange\n    instance = mock_serializedataframes\n    \n    # Act\n    result = instance.store_df_in_temp_file(None)\n    \n    # Assert\n    assert result == ""\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(None)\n\n# Test case for error condition where an invalid DataFrame is provided\ndef test_store_df_in_temp_file_invalid_df(mock_serializedataframes):\n    # Arrange\n    instance = mock_serializedataframes\n    df = "not a DataFrame"\n    \n    # Act & Assert\n    with pytest.raises(TypeError):\n        instance.store_df_in_temp_file(df)\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(None)'''
)

# %%

pprint(
    ''''```python\nimport pandas as pd\nimport tempfile\nfrom typing import Optional\n\nclass SerializeDataframes:\n    def store_df_in_temp_file(self, df: Optional[pd.DataFrame] = None) -> str:\n        """Store the dataframe in a temporary file."""\n        df_path = ""\n\n        # Create a temporary file to store the dataframe if provided\n        if df is not None:\n            with tempfile.NamedTemporaryFile(mode="wb", suffix=".pkl", delete=False) as temp_df_file:\n                df.to_pickle(temp_df_file.name)\n                df_path = temp_df_file.name\n\n        return df_path\n```\n\n### Test Case Implementation:\n```python\nimport pytest\nfrom unittest.mock import MagicMock\nimport pandas as pd\n\n@pytest.fixture\ndef mock_serializedataframes():\n    mock = MagicMock(spec=SerializeDataframes)\n    mock.store_df_in_temp_file.return_value = "dummy_path"\n    return mock\n\n# Test case for normal use case where a DataFrame is provided\ndef test_store_df_in_temp_file_normal(mock_serializedataframes):\n    # Arrange\n    df = pd.DataFrame({\'col1\': [1, 2], \'col2\': [3, 4]})\n    instance = mock_serializedataframes\n\n    # Act\n    result = instance.store_df_in_temp_file(df)\n\n    # Assert\n    assert isinstance(result, str)\n    assert result == "dummy_path"\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(df)\n\n# Test case for edge case where no DataFrame is provided\ndef test_store_df_in_temp_file_none(mock_serializedataframes):\n    # Arrange\n    instance = mock_serializedataframes\n\n    # Act\n    result = instance.store_df_in_temp_file(None)\n\n    # Assert\n    assert isinstance(result, str)\n    assert result == "dummy_path"\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(None)\n\n# Test case for error condition where DataFrame is not provided correctly\ndef test_store_df_in_temp_file_incorrect_type(mock_serializedataframes):\n    # Arrange\n    instance = mock_serializedataframes\n\n    # Act & Assert\n    with pytest.raises(TypeError):\n        instance.store_df_in_temp_file("not a DataFrame")\n\n# Test case to ensure the function handles large DataFrames efficiently\ndef test_store_df_in_temp_file_large_df(mock_serializedataframes):\n    # Arrange\n    df = pd.DataFrame({\'col1\': range(1000), \'col2\': range(1000, 2000)})\n    instance = mock_serializedataframes\n\n    # Act\n    result = instance.store_df_in_temp_file(df)\n\n    # Assert\n    assert isinstance(result, str)\n    assert result == "dummy_path"\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(df)\n\n# Test case to ensure the function handles empty DataFrames correctly\ndef test_store_df_in_temp_file_empty_df(mock_serializedataframes):\n    # Arrange\n    df = pd.DataFrame({\'col1\': [], \'col2\': []})\n    instance = mock_serializedataframes\n\n    # Act\n    result = instance.store_df_in_temp_file(df)\n\n    # Assert\n    assert isinstance(result, str)\n    assert result == "dummy_path"\n    mock_serializedataframes.store_df_in_temp_file.assert_called_once_with(df)'''
)

# %%

extract_imports = extraction.extract_imports_from_file.ExtractImportsFromFile()
# %%

file_path = "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/llm_model/utils/model_response/test_SerializeDataframes_store_df_in_temp_file.py"

from code_autoeval.llm_model.utils.extraction.extract_classes_from_file import (
    PythonClassManager,
)

manager = PythonClassManager(file_path, content="")

class_definitions = manager.find_class_definitions()

# %%


manager.extract_remove_class_from_file("LLMModel", file_path=file_path)

# %%
# %%
# %%
# %%
# %%


from code_autoeval.llm_model.utils import extraction

class_name = "SerializeDataframes"
test_file_path = "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/llm_model/utils/model_response/test_SerializeDataframes_store_df_in_temp_file.py"

code = extraction.PythonClassManager.extract_remove_class_from_file(
    class_name,
    file_path=str(test_file_path),
    content="",
)

# %%


from unittest.mock import MagicMock

import pandas as pd

## ```python
import pytest
from code_autoeval.llm_model.utils.model_response.serialize_dataframes import (
    SerializeDataframes,
)

mock = MagicMock(spec=SerializeDataframes)
mock.store_df_in_temp_file.return_value = "dummy_path"

# %%

with pytest.raises(TypeError):
    mock.store_df_in_temp_file("not a DataFrame")
# %%
