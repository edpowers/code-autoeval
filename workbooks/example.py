"""Example for the code_autoeval client."""

# %%

import asyncio
from abc import ABC, abstractmethod
from pprint import pprint

import nest_asyncio
import pandas as pd

from code_autoeval.llm_model.utils.extraction.extract_imports_from_file import (
    ExtractImportsFromFile,
)

nest_asyncio.apply()

from code_autoeval.llm_model.llm_model import LLMModel

llm_model_client = LLMModel()

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


example = "'You are an expert Python code generator. Your task is to create Python code that solves a specific problem using a provided function signature.\n        Follow these instructions carefully:\n\n        1. Function Details:\n        Function Name: LLMModel.__init__\n        Function is async coroutine: False\n        Signature: (**data: 'Any') -> 'None'\n        Docstring: Create a new model by parsing and validating input data from keyword arguments.\n\nRaises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be\nvalidated to form a valid model.\n\n`self` is explicitly positional-only to allow `self` as a field name.\n\n        2. Task: Implement the __init__ method for the LLMModel class. - with Refactor code to handle edge cases and improve efficiency.\n\n        3. Code Generation Guidelines:\n        - Implement the function according to the given signature.\n        - Ensure all function arguments have their types explicitly mentioned.\n        - Create any necessary additional code to solve the task.\n        - Ensure the code is efficient, readable, and follows Python best practices.\n        - Include proper error handling if appropriate.\n        - Add brief, inline comments for clarity if needed.\n        - If any of the function args are pandas.DataFrame, pandas.Series, verify the index.\n\n        4. Output Format:\n        - Provide the Python code.\n        - After the code, on a new line, write "  # Expected Output:" followed by the expected output of the function for the given task.\n        - The expected output should be a string representation of the result.\n\n        5. Pytest Tests:\n        - After providing the main function and expected output, create pytest tests for the function.\n        - Create at least 3 test functions covering different scenarios, including edge cases and potential error conditions.\n        - Ensure 100% code coverage for the function being tested.\n\n        When writing pytest tests, please adhere to the following guidelines:\n\n        1. Only use variables that are explicitly defined within each test function.\n        2. Avoid relying on global variables or undefined mocks.\n        3. If you need to mock a method or function, define the mock within the test function using pytest.mock.patch as a decorator or context manager.\n        4. Ensure that each test function is self-contained and does not depend on the state from other tests.\n        5. Use descriptive names for test functions that clearly indicate what is being tested.\n        6. Follow the Arrange-Act-Assert (AAA) pattern in your tests:\n        - Arrange: Set up the test data and conditions.\n        - Act: Perform the action being tested.\n        - Assert: Check that the results are as expected.\n        7. Use assert statements to verify the expected behavior.\n        8. When testing for exceptions, use pytest.raises() as a context manager.\n\n        Example of expected response format:\n\n        ```python\n        # Expected Output: 7\n\n        import pandas as pd\n        import numpy as np\n\n        def example_func(arg1: int, arg2: int) -> int:\n            # Your code here\n            result = arg1 + arg2\n            return result\n\n        class TestExampleFunc:\n            def test_normal_case(self):\n                assert example_func(3, 4) == 7\n\n            def test_edge_case(self):\n                assert example_func(-2, -3) == -5\n\n            def test_zero(self):\n                assert example_func(0, 0) == 0\n\n        # Test the function\n        print(example_func(3, 4))\n\n        print(TestExampleFunc().test_normal_case())\n\n        # Tests\n        import pytest\n\n        def test_positive_numbers():\n            assert example_func(3, 4) == 7\n\n        def test_negative_numbers():\n            assert example_func(-2, -3) == -5\n\n        def test_zero():\n            assert example_func(0, 0) == 0\n\n        def test_large_numbers():\n            assert example_func(1000000, 2000000) == 3000000\n\n        def test_type_error():\n            with pytest.raises(TypeError):\n                example_func("3", 4)\n\n        def test_class_normal_case():\n            assert TestExampleFunc().test_normal_case() == None\n\n        Remember to provide the main function implementation, expected output, and pytest tests as described above.\n        Ensure 100% code coverage for the function being tested.'"

from pprint import pprint

pprint(example)

# %%
# %%


pprint(
    '\n        The previous response encountered issues. Please address the following problems and improve the code:\n\n        Task: Implement the code_generator method for the LLMModel class.\n        Function signature: (self, query: str, func: Callable[..., Any], df: Optional[pandas.core.frame.DataFrame] = None, goal: Optional[str] = None, verbose: bool = True, debug: bool = False, max_retries: int = 3, skip_generate_fake_data: bool = False, class_model: code_autoeval.llm_model.utils.model.class_data_model.ClassDataModel = None) -> Tuple[str, Any, str, Dict[str, Any], str]\n        Function is async coroutine: True\n        Function docstring: Generates Python code based on the query, provided function, and optional dataframe.\n\n:param query: The user\'s query describing the desired functionality\n:param func: The function to be implemented\n:param df: Optional dataframe to use for testing and validation\n:param goal: Optional specific goal for the function (e.g., "replace every instance of \'Australia\'")\n:param verbose: Whether to print verbose output\n:param debug: Whether to print debug information\n:param max_retries: Maximum number of retries for code generation\n:param skip_generate_fake_data: Whether to skip generating fake data\n        \n            Execution error encountered:\n            Error: Failed to parse coverage output.\n\n            Please review the code and address the following:\n            1. Check for syntax errors or logical issues in the implementation.\n            2. Ensure all necessary imports are included.\n            3. Verify that the function handles all possible input scenarios correctly.\n\n            Previous code that generated the error:\n            import pytest\nfrom unittest.mock import patch, MagicMock\nfrom code_autoeval.llm_model.llm_model import LLMModel\nimport pandas as pd\nimport numpy as np\n\n# Mocking dependencies\n@patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)\ndef test_normal_case(mock_init):\n    # Arrange\n    mock_instance = LLMModel()\n    query = "example query"\n    func = lambda x: x + 1\n    df = pd.DataFrame({\'A\': [1, 2, 3]})\n    goal = None\n    verbose = True\n    debug = False\n    max_retries = 3\n    skip_generate_fake_data = False\n    class_model = None\n\n    # Act\n    result = mock_instance.code_generator(query, func, df, goal, verbose, debug, max_retries, skip_generate_fake_data, class_model)\n\n    # Assert\n    assert isinstance(result, tuple)\n    assert len(result) == 5\n    assert isinstance(result[0], str)\n    assert callable(result[1])\n    assert isinstance(result[2], str)\n    assert isinstance(result[3], dict)\n    assert isinstance(result[4], str)\n\ndef test_edge_case_with_no_df(mock_init):\n    # Arrange\n    mock_instance = LLMModel()\n    query = "example query"\n    func = lambda x: x + 1\n    goal = None\n    verbose = True\n    debug = False\n    max_retries = 3\n    skip_generate_fake_data = False\n    class_model = None\n\n    # Act\n    result = mock_instance.code_generator(query, func, df=None, goal, verbose, debug, max_retries, skip_generate_fake_data, class_model)\n\n    # Assert\n    assert isinstance(result, tuple)\n    assert len(result) == 5\n    assert isinstance(result[0], str)\n    assert callable(result[1])\n    assert isinstance(result[2], str)\n    assert isinstance(result[3], dict)\n    assert isinstance(result[4], str)\n\ndef test_error_condition_with_max_retries(mock_init):\n    # Arrange\n    mock_instance = LLMModel()\n    query = "example query"\n    func = lambda x: x + 1\n    df = pd.DataFrame({\'A\': [1, 2, 3]})\n    goal = None\n    verbose = True\n    debug = False\n    max_retries = 1\n    skip_generate_fake_data = False\n    class_model = None\n\n    # Act and Assert\n    with pytest.raises(Exception):\n        mock_instance.code_generator(query, func, df, goal, verbose, debug, max_retries, skip_generate_fake_data, class_model)\n\nimport pytest\nfrom unittest.mock import patch, MagicMock\nfrom code_autoeval.llm_model.llm_model import LLMModel\nimport pandas as pd\nimport numpy as np\n\n# Mocking dependencies\n@patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)\ndef test_normal_case(mock_init):\n    # Arrange\n    mock_instance = LLMModel()\n    query = "example query"\n    func = lambda x: x + 1\n    df = pd.DataFrame({\'A\': [1, 2, 3]})\n    goal = None\n    verbose = True\n    debug = False\n    max_retries = 3\n    skip_generate_fake_data = False\n    class_model = None\n\n    # Act\n    result = mock_instance.code_generator(query, func, df, goal, verbose, debug, max_retries, skip_generate_fake_data, class_model)\n\n    # Assert\n    assert isinstance(result, tuple)\n    assert len(result) == 5\n    assert isinstance(result[0], str)\n    assert callable(result[1])\n    assert isinstance(result[2], str)\n    assert isinstance(result[3], dict)\n    assert isinstance(result[4], str)\n\ndef test_edge_case_with_no_df(mock_init):\n    # Arrange\n    mock_instance = LLMModel()\n    query = "example query"\n    func = lambda x: x + 1\n    goal = None\n    verbose = True\n    debug = False\n    max_retries = 3\n    skip_generate_fake_data = False\n    class_model = None\n\n    # Act\n    result = mock_instance.code_generator(query, func, df=None, goal, verbose, debug, max_retries, skip_generate_fake_data, class_model)\n\n    # Assert\n    assert isinstance(result, tuple)\n    assert len(result) == 5\n    assert isinstance(result[0], str)\n    assert callable(result[1])\n    assert isinstance(result[2], str)\n    assert isinstance(result[3], dict)\n    assert isinstance(result[4], str)\n\ndef test_error_condition_with_max_retries(mock_init):\n    # Arrange\n    mock_instance = LLMModel()\n    query = "example query"\n    func = lambda x: x + 1\n    df = pd.DataFrame({\'A\': [1, 2, 3]})\n    goal = None\n    verbose = True\n    debug = False\n    max_retries = 1\n    skip_generate_fake_data = False\n    class_model = None\n\n    # Act and Assert\n    with pytest.raises(Exception):\n        mock_instance.code_generator(query, func, df, goal, verbose, debug, max_retries, skip_generate_fake_data, class_model)\n            \n        Please provide:\n        1. An updated implementation of the LLMModel.code_generator function.\n        2. A comprehensive set of pytest tests that cover all code paths.\n        3. Expected output for a sample input.\n\n        Remember to handle all possible scenarios, including:\n        - Empty inputs (e.g., empty DataFrames, empty columns)\n        - Invalid inputs (e.g., non-existent columns, incorrect data types)\n        - Edge cases (e.g., very large or very small values, NaN values)\n        - Various data types (e.g., integers, floats, strings, dates)\n\n        Ensure that your implementation is robust and handles errors gracefully.\n        '
)

# %%

extract_imports = ExtractImportsFromFile()
# %%


from code_autoeval.llm_model.utils.extraction.extract_classes_from_file import (
    PythonClassManager,
)

file_path = "/Users/eddyt/Algo/projects/code-autoeval/generated_code/tests/code_autoeval/clients/llm_model/test_LLMModel_split_content_from_model.py"
content = ""

manager = PythonClassManager(file_path, content=content)

class_definitions = manager.find_class_definitions()

# %%


manager.extract_remove_class_from_file("LLMModel", file_path=file_path)

# %%
