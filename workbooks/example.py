"""Example for the code_autoeval client."""
#%%

import asyncio
from abc import ABC, abstractmethod

import nest_asyncio
import pandas as pd

nest_asyncio.apply()

from code_autoeval.clients.llm_model.llm_model import LLMModel

llm_model_client = LLMModel()

#%%


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


async def main2() -> None:
    query = "Remove outliers from a numerical column in a pandas dataframe with temporal ordering."
    goal = "Refactor code to handle edge cases."

    function_to_implement = AbstractDataFrameClass.remove_outliers
    skip_generate_fake_data = False

    code, serialized_result, expected_output, context, pytest_tests = await llm_model_client.code_generator(
            query, function_to_implement, goal=goal, verbose=True, debug=True, skip_generate_fake_data=skip_generate_fake_data
        )


# Run the async main function
asyncio.run(main2())

# %%
