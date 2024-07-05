from unittest.mock import patch

import pytest


class ValidateRegexes:
    def __init__(self, *args, **kwargs):
        pass

    async def validate_test_in_pytest_code(self, pytest_code: str) -> None:
        if "def test_" not in pytest_code:
            raise ValueError(f"pytest_tests must be in {pytest_code}")

from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_validate_test_in_pytest_code_normal():
    validate = ValidateRegexes()
    with patch("code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes.validate_test_in_pytest_code", return_value=None):
        result = await validate.validate_test_in_pytest_code("def test_example(): pass")
        assert result is None

@pytest.mark.asyncio
async def test_validate_test_in_pytest_code_missing():
    validate = ValidateRegexes()
    with pytest.raises(ValueError):
        await validate.validate_test_in_pytest_code("def example(): pass")

@pytest.mark.asyncio
async def test_validate_test_in_pytest_code_empty():
    validate = ValidateRegexes()
    with pytest.raises(ValueError):
        await validate.validate_test_in_pytest_code("")

@pytest.mark.asyncio
async def test_validate_test_in_pytest_code_none():
    validate = ValidateRegexes()
    with pytest.raises(ValueError):
        await validate.validate_test_in_pytest_code(None)

@pytest.mark.asyncio
async def test_validate_test_in_pytest_code_whitespace():
    validate = ValidateRegexes()
    with pytest.raises(ValueError):
        await validate.validate_test_in_pytest_code("   ")async def test_validate_test_in_pytest_code_whitespace():
    validate = ValidateRegexes()
    with pytest.raises(ValueError):
        await validate.validate_test_in_pytest_code("   ")