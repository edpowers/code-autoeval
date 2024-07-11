from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.extraction.find_parent_class import FindParentClass
@pytest.fixture
def fixture_mock_findparentclass():
    mock = MagicMock(spec=FindParentClass)
    mock.find_and_extract_target = MagicMock()
    mock.find_target_in_code = MagicMock()
    mock.update_local_var_names = MagicMock()
    return mock
