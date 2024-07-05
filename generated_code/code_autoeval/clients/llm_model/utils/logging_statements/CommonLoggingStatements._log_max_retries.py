# Updated Implementation of CommonLoggingStatements._log_max_retries function
class CommonLoggingStatements:
    def __init__(self, data):
        self.data = data

    async def _log_max_retries(self, max_retries: int) -> None:
        if not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer")

        if self.data.verbose:
            print(f"Failed to generate correct code with 100% coverage after {max_retries} attempts.")

import pytest
from unittest.mock import patch
from code_autoeval.llm_model.utils.logging_statements.common_logging_statements import CommonLoggingStatements

@pytest.fixture
def setup_common_logging():
    return CommonLoggingStatements(data={"verbose": True})

@pytest.mark.asyncio
async def test_log_max_retries_normal_case(setup_common_logging):
    with patch('builtins.print') as mock_print:
        await setup_common_logging._log_max_retries(5)
        mock_print.assert_called_with("Failed to generate correct code with 100% coverage after 5 attempts.")

@pytest.mark.asyncio
async def test_log_max_retries_zero_attempts(setup_common_logging):
    with patch('builtins.print') as mock_print:
        await setup_common_logging._log_max_retries(0)
        mock_print.assert_called_with("Failed to generate correct code with 100% coverage after 0 attempts.")

@pytest.mark.asyncio
async def test_log_max_retries_negative_attempts(setup_common_logging):
    with pytest.raises(ValueError):
        await setup_common_logging._log_max_retries(-1)

@pytest.mark.asyncio
async def test_log_max_retries_non_integer_attempts(setup_common_logging):
    with pytest.raises(ValueError):
        await setup_common_logging._log_max_retries("not an integer")

@pytest.mark.asyncio
async def test_log_max_retries_verbose_false(setup_common_logging):
    mock_data = {"verbose": False}
    with patch('builtins.print') as mock_print:
        setup_common_logging = CommonLoggingStatements(data=mock_data)
        await setup_common_logging._log_max_retries(5)
        assert not mock_print.called

Failed to generate correct code with 100% coverage after 5 attempts.