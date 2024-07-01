"""Example for the code_autoeval client."""

# %%

import asyncio
from abc import ABC, abstractmethod

import nest_asyncio
import pandas as pd

nest_asyncio.apply()

from code_autoeval.clients.llm_model.llm_model import LLMModel

llm_model_client = LLMModel()

# %%

test_str = "code_autoeval.clients.llm_model.llm_model.LLMModel"

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
        "--cov=code_autoeval.clients.llm_model.llm_model.LLMModel",
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


example = ""

from pprint import pprint

pprint(example)

# %%
# %%


pprint(
    "import re\nimport traceback\nfrom pprint import pprint\nfrom typing import Any, Callable, Dict, Optional, Tuple\nimport pandas as pd\nfrom code_autoeval.clients.llm_model.utils.decipher_response import DeciperResponse\nfrom code_autoeval.clients.llm_model.utils.execute_generated_code import (\nfrom code_autoeval.clients.llm_model.utils.execute_unit_tests import ExecuteUnitTests\nfrom code_autoeval.clients.llm_model.utils.extract_function_attributes import (\nfrom code_autoeval.clients.llm_model.utils.generate_fake_data import GenerateFakeData\nfrom code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel\nfrom code_autoeval.clients.llm_model.utils.serializing_dataframes import (\nfrom code_autoeval.model.backend_model_kwargs import BackendModelKwargs"
)

# %%
