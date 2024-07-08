from unittest.mock import MagicMock
import pytest
from code_autoeval.llm_model.utils.find_parent_class import FindParentClass
@pytest.fixture
def fixture_mock_findparentclass():
    mock = MagicMock(spec=FindParentClass)
    return mock