from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.log_funcs.common_logging_statements import CommonLoggingStatements
from generated_code.fixtures.fixtures.commonloggingstatements_fixture import fixture_mock_commonloggingstatements


@pytest.fixture(scope='module')
def mock_commonloggingstatements():
    return CommonLoggingStatements()

## def test_CommonLoggingStatements._log_max_retries(mock_commonloggingstatements):
    # Arrange
    self = MagicMock()
    max_retries = 5

    instance = mock_commonloggingstatements

    # Act
    result = instance._log_max_retries(self, max_retries)

    # Assert
    assert isinstance(result, type(None))
    self.common.class_logger.debug.assert_called_once_with(f"Failed to generate correct code with 100% coverage after {max_retries} attempts.")