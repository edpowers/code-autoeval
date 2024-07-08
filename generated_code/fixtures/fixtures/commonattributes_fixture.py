from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.base_llm_class import CommonAttributes
from pathlib import Path
import logging
from code_autoeval.llm_model.utils.base_llm_class import BaseModelConfig
from generated_code.fixtures.fixtures.basemodelconfig_fixture import fixture_mock_basemodelconfig
@pytest.fixture
def fixture_mock_commonattributes():
    mock = MagicMock(spec=CommonAttributes)
    mock.project_root = Path('/')
    mock.generated_base_dir = Path('/')
    mock.generated_base_log_dir = Path('/')
    mock.class_logger = logging.getLogger('test')
    return mock