# Updated Implementation of GenerateFakeData.async_generate_fake_data function
import random
import re
from typing import Any, Callable, Optional
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
from faker import Faker


class GenerateFakeData:
    def __init__(self):
        self.debug = False

    async def ask_backend_model(self, prompt: str, system_prompt: str = "") -> str:
        # Mock implementation for testing purposes
        return "Expected Output:\n

"

    def generate_fake_data_prompt(self, func: Callable[..., Any]) -> str:
        # Mock implementation for testing purposes
        return "Generate fake data based on the function signature."

    def figure_out_model_response_for_faker(self, response: str) -> str:
        # Mock implementation for testing purposes
        return response.split("Expected Output:\n")[1].strip()

    def run_preprocess_pipeline(self, code: str, code_type: str = "") -> str:
        # Mock implementation for testing purposes
        return code

    def _log_code(self, code: str):
        # Mock implementation for logging (not relevant for test coverage)
        pass

    def _log_fake_gen_data(self, fake_data: pd.DataFrame):
        # Mock implementation for logging (not relevant for test coverage)
        pass

    @staticmethod
    async def async_generate_fake_data(
        self,
        func: Callable[..., Any],
        df: Optional[pd.DataFrame] = None,
        debug: bool = False,
        skip_generate_fake_data: bool = False,
    ) -> pd.DataFrame:
        if df is not None or skip_generate_fake_data:
            return df

        self.debug = debug

        fake_data_prompt = self.generate_fake_data_prompt(func)

        fake_data_response = await self.ask_backend_model(
            fake_data_prompt, system_prompt=""
        )

        content = self.figure_out_model_response_for_faker(fake_data_response)

        parts = re.split(r"[# ]{0,2}Expected Output:|### Expected Output:", content, maxsplit=1)

        code = parts[0].strip()
        code = self.run_preprocess_pipeline(code, code_type="")
        self._log_code(code)

        try:
            local_vars = {"pd": pd, "Faker": Faker, "random": random}
            exec(code, local_vars)
            fake_data = local_vars.get("fake_data")

            if not isinstance(fake_data, pd.DataFrame):
                raise ValueError("The generated fake data is not a pandas DataFrame")

            self._log_fake_gen_data(fake_data)

            return fake_data

        except Exception as e:
            raise Exception(f"Error creating fake data: {str(e)}\nCode:\n{code}")

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_normal(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    fake_data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
    # Act
    result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func, df=fake_data)
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'col1' in result.columns
    assert 'col2' in result.columns

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_skip(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    fake_data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    
    # Act
    result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func, df=fake_data, skip_generate_fake_data=True)
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'col1' in result.columns
    assert 'col2' in result.columns

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_error(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    
    # Mocking a function that will raise an error
    def mock_ask_backend_model(*args, **kwargs):
        return "Invalid response"
    
    with patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.ask_backend_model", new=mock_ask_backend_model):
        # Act & Assert
        with pytest.raises(Exception):
            GenerateFakeData.async_generate_fake_data(mock_self, mock_func)

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_debug(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    
    def mock_ask_backend_model(*args, **kwargs):
        return "Expected Output:\n

"
    
    with patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.ask_backend_model", new=mock_ask_backend_model):
        # Act
        result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func, debug=True)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'col1' in result.columns
        assert 'col2' in result.columns

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_empty_df(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    fake_data = pd.DataFrame({'col1': [], 'col2': []})
    
    # Act
    result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func, df=fake_data)
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert 'col1' in result.columns
    assert 'col2' in result.columns

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_invalid_column(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    fake_data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    fake_data['invalid_column'] = 'This should not be here'
    
    # Act & Assert
    with pytest.raises(KeyError):
        GenerateFakeData.async_generate_fake_data(mock_self, mock_func, df=fake_data)

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_no_df(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    
    def mock_ask_backend_model(*args, **kwargs):
        return "Expected Output:\n

"
    
    with patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.ask_backend_model", new=mock_ask_backend_model):
        # Act
        result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'col1' in result.columns
        assert 'col2' in result.columns

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_large_df(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    fake_data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
    fake_data = pd.concat([fake_data] * 1000, ignore_index=True)
    
    # Act
    result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func, df=fake_data)
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2000
    assert 'col1' in result.columns
    assert 'col2' in result.columns

@patch("code_autoeval.clients.llm_model.utils.generate_fake_data.GenerateFakeData.__init__", return_value=None)
def test_async_generate_fake_data_nan_values(mock_init):
    # Arrange
    mock_self = MagicMock()
    mock_func = lambda: None
    fake_data = pd.DataFrame({'col1': [np.nan, 2], 'col2': ['a', np.nan]})
    
    # Act
    result = GenerateFakeData.async_generate_fake_data(mock_self, mock_func, df=fake_data)
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'col1' in result.columns
    assert 'col2' in result.columns
    assert np.isnan(result['col1'][0])
    assert np.isnan(result['col2'][1])