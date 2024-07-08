from code_autoeval.llm_model.utils.base_llm_class import BaseModelConfig
from code_autoeval.llm_model.utils.base_llm_class import BaseModelConfig
import pytest
from generated_code.fixtures.fixtures.commonattributes_fixture import fixture_mock_commonattributes
from code_autoeval.llm_model.utils.base_llm_class import CommonAttributes
from pathlib import Path
import logging
def test_mock_commonattributes(fixture_mock_commonattributes):
    assert isinstance(fixture_mock_commonattributes, CommonAttributes)
    assert hasattr(fixture_mock_commonattributes, 'project_root')
    assert isinstance(fixture_mock_commonattributes.project_root, Path)
    assert hasattr(fixture_mock_commonattributes, 'generated_base_dir')
    assert isinstance(fixture_mock_commonattributes.generated_base_dir, Path)
    assert hasattr(fixture_mock_commonattributes, 'generated_base_log_dir')
    assert isinstance(fixture_mock_commonattributes.generated_base_log_dir, Path)
    assert hasattr(fixture_mock_commonattributes, 'class_logger')
    assert isinstance(fixture_mock_commonattributes.class_logger, logging.Logger)
    assert isinstance(fixture_mock_commonattributes, BaseModelConfig)