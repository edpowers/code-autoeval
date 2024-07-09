import pytest
from generated_code.fixtures.fixtures.extractcontextfromexception_fixture import fixture_mock_extractcontextfromexception
from code_autoeval.llm_model.utils.extraction.extract_context_from_exception import ExtractContextFromException
def test_mock_extractcontextfromexception(fixture_mock_extractcontextfromexception):
    assert isinstance(fixture_mock_extractcontextfromexception, ExtractContextFromException)
    assert hasattr(fixture_mock_extractcontextfromexception, '_get_relevant_code')
    assert callable(fixture_mock_extractcontextfromexception._get_relevant_code)
    assert hasattr(fixture_mock_extractcontextfromexception, 'create_llm_error_prompt')
    assert callable(fixture_mock_extractcontextfromexception.create_llm_error_prompt)
    assert hasattr(fixture_mock_extractcontextfromexception, 'format_error')
    assert callable(fixture_mock_extractcontextfromexception.format_error)