# Expected Output: Implementing the get_imported_libraries method for the ExecuteGeneratedCode class.

from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.execute_generated_code import ExecuteGeneratedCode


@pytest.fixture(autouse=True)
def setup():
    with patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.__init__",
        return_value=None,
    ):
        yield


# Test the get_imported_libraries method
def test_get_imported_libraries_normal():
    # Arrange
    mock_instance = ExecuteGeneratedCode()
    mock_instance.imported_libraries = {"numpy", "pandas"}

    # Act
    result = mock_instance.get_imported_libraries()

    # Assert
    assert result == {"numpy", "pandas"}


def test_get_imported_libraries_empty():
    # Arrange
    mock_instance = ExecuteGeneratedCode()
    mock_instance.imported_libraries = set()

    # Act
    result = mock_instance.get_imported_libraries()

    # Assert
    assert result == set()


def test_get_imported_libraries_none():
    # Arrange
    mock_instance = ExecuteGeneratedCode()
    mock_instance.imported_libraries = None

    # Act
    result = mock_instance.get_imported_libraries()

    # Assert
    assert result is None


def test_get_imported_libraries_missing():
    # Arrange
    mock_instance = ExecuteGeneratedCode()
    with patch(
        "code_autoeval.llm_model.utils.execute_generated_code.ExecuteGeneratedCode.imported_libraries",
        new_callable=MagicMock,
    ) as mock_imported_libs:
        mock_imported_libs.__get__ = MagicMock(return_value=None)

    # Act
    result = mock_instance.get_imported_libraries()

    # Assert
    assert result is None
    # Assert
    assert result is None
