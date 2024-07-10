from pathlib import Path
from unittest.mock import MagicMock

import pytest

from code_autoeval.llm_model.utils.base_llm_class import BaseLLMClass


@pytest.fixture
def fixture_mock_basellmclass():
    mock = MagicMock(spec=BaseLLMClass)
    mock.coverage_result = None
    mock.file_path = Path()
    mock.test_file_path = Path()
    mock.absolute_path_from_root = Path()
    mock.unique_imports_dict = {}
    return mock
