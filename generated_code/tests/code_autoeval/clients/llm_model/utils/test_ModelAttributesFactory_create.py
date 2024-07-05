import os
from unittest.mock import MagicMock

from dotenv import find_dotenv, load_dotenv

from code_autoeval.llm_model.utils.base_llm_class import (
    LLMModelAttributes, ModelAttributesFactory)


def create():
    """
    Create and return the attributes for an LLM model using environment variables.

    Returns:
        LLMModelAttributes: An instance of LLMModelAttributes with model name and URL from environment variables.
    """
    load_dotenv(find_dotenv())

    llm_model_name = os.getenv("OPENAI_MODEL_NAME", "coder-lite:latest")
    llm_model_url = os.getenv("OPENAI_BASE_URL", "")

    return LLMModelAttributes(llm_model_name=llm_model_name, llm_model_url=llm_model_url)

import os
from unittest.mock import patch

import pytest
from dotenv import find_dotenv, load_dotenv

from code_autoeval.llm_model.utils.base_llm_class import (
    LLMModelAttributes, ModelAttributesFactory)


# Mock environment variables for testing
@patch.dict(os.environ, {"OPENAI_MODEL_NAME": "test-model", "OPENAI_BASE_URL": "http://test-url"})
def test_create_normal():
    """Test the normal use case of create function."""
    result = ModelAttributesFactory.create()
    assert isinstance(result, LLMModelAttributes)
    assert result.llm_model_name == "test-model"
    assert result.llm_model_url == "http://test-url"

def test_create_missing_env_var():
    """Test the case where an environment variable is missing."""
    with patch.dict(os.environ, {"OPENAI_MODEL_NAME": "test-model"}, clear=True):
        result = ModelAttributesFactory.create()
        assert isinstance(result, LLMModelAttributes)
        assert result.llm_model_name == "test-model"
        assert result.llm_model_url == ""

def test_create_empty_env_var():
    """Test the case where an environment variable is empty."""
    with patch.dict(os.environ, {"OPENAI_MODEL_NAME": "", "OPENAI_BASE_URL": ""}, clear=True):
        result = ModelAttributesFactory.create()
        assert isinstance(result, LLMModelAttributes)
        assert result.llm_model_name == "coder-lite:latest"
        assert result.llm_model_url == ""

@patch.dict(os.environ, {"OPENAI_MODEL_NAME": "test-model", "OPENAI_BASE_URL": "http://test-url"})
def test_create_with_dotenv():
    """Test the create function with dotenv loading."""
    load_dotenv = MagicMock()
    find_dotenv = MagicMock(return_value="mocked_path")
    with patch("code_autoeval.llm_model.utils.base_llm_class.load_dotenv", load_dotenv):
        with patch("code_autoeval.llm_model.utils.base_llm_class.find_dotenv", find_dotenv):
            result = ModelAttributesFactory.create()
            assert isinstance(result, LLMModelAttributes)
            assert result.llm_model_name == "test-model"
            assert result.llm_model_url == "http://test-url"
            load_dotenv.assert_called_once_with("mocked_path")
            find_dotenv.assert_called_once()    with patch("code_autoeval.llm_model.utils.base_llm_class.load_dotenv", load_dotenv):
        with patch("code_autoeval.llm_model.utils.base_llm_class.find_dotenv", find_dotenv):
            result = ModelAttributesFactory.create()
            assert isinstance(result, LLMModelAttributes)
            assert result.llm_model_name == "test-model"
            assert result.llm_model_url == "http://test-url"
            load_dotenv.assert_called_once_with("mocked_path")
            find_dotenv.assert_called_once()