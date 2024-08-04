import pytest
from generated_code.fixtures.fixtures.llmmodelattributes_fixture import fixture_mock_llmmodelattributes
from code_autoeval.llm_model.utils.base_llm_class import LLMModelAttributes
def test_mock_llmmodelattributes(fixture_mock_llmmodelattributes):
    assert isinstance(fixture_mock_llmmodelattributes, LLMModelAttributes)
    assert hasattr(fixture_mock_llmmodelattributes, 'llm_model_name')
    assert isinstance(fixture_mock_llmmodelattributes.llm_model_name, str)
    assert fixture_mock_llmmodelattributes.llm_model_name == "example_model"
    assert hasattr(fixture_mock_llmmodelattributes, 'llm_model_url')
    assert isinstance(fixture_mock_llmmodelattributes.llm_model_url, str)
    assert fixture_mock_llmmodelattributes.llm_model_url == "http://example.com"