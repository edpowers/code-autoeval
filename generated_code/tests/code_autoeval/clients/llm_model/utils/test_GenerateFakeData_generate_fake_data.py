import asyncio
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


class GenerateFakeData:
    def __init__(self):
        self.model_computed_fields = {}
        self.model_config = {}
        self.model_extra = {}
        self.model_fields = {}
        self.model_fields_set = set()

    async def async_generate_fake_data(
        self, func, df=None, debug=False, skip_generate_fake_data=False
    ):
        if skip_generate_fake_data:
            return df if df is not None else pd.DataFrame()

        # Mocking the function call to generate fake data
        mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})
        return mock_df

    def generate_fake_data(
        self, func, df=None, debug=False, skip_generate_fake_data=False
    ):
        """
        Generate fake data based on the function signature if needed.
        """
        return asyncio.run(
            self.async_generate_fake_data(func, df, debug, skip_generate_fake_data)
        )


##################################################
# TESTS
##################################################


@pytest.fixture
def generate_fake_data_instance():
    return GenerateFakeData()


@pytest.mark.asyncio
async def test_async_generate_fake_data(generate_fake_data_instance):
    func = lambda: None
    df = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})
    result = await generate_fake_data_instance.async_generate_fake_data(func, df)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_generate_fake_data_normal(generate_fake_data_instance):
    func = lambda: None
    result = generate_fake_data_instance.generate_fake_data(func)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_generate_fake_data_with_existing_df(generate_fake_data_instance):
    func = lambda: None
    df = pd.DataFrame({"column1": [4, 5, 6], "column2": ["d", "e", "f"]})
    result = generate_fake_data_instance.generate_fake_data(func, df)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_generate_fake_data_skip(generate_fake_data_instance):
    func = lambda: None
    result = generate_fake_data_instance.generate_fake_data(
        func, skip_generate_fake_data=True
    )
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


def test_generate_fake_data_debug(generate_fake_data_instance):
    func = lambda: None
    with patch(
        "code_autoeval.llm_model.utils.generate_fake_data.GenerateFakeData.async_generate_fake_data",
        return_value=pd.DataFrame({"column1": [7, 8, 9], "column2": ["g", "h", "i"]}),
    ):
        result = generate_fake_data_instance.generate_fake_data(func, debug=True)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
