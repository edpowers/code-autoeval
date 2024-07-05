import inspect
from typing import Any, List
from unittest.mock import MagicMock, patch

import pytest


class ClassDataModelFactory:
    @staticmethod
    def _get_coroutine_methods(class_to_process: Any) -> List[str]:
        return [
            name
            for name, method in inspect.getmembers(class_to_process)
            if inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(method)
        ]


# Test the function
@pytest.mark.asyncio
async def test_normal_case():
    mock_class = MagicMock()
    mock_class.__name__ = "TestClass"
    mock_class.a_method = MagicMock()
    mock_class.b_method = MagicMock(spec=inspect.isasyncgenfunction)

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._get_coroutine_methods",
        return_value=["a_method", "b_method"],
    ):
        result = await ClassDataModelFactory._get_coroutine_methods(mock_class)
        assert result == ["a_method", "b_method"]


@pytest.mark.asyncio
async def test_no_coroutine_methods():
    mock_class = MagicMock()
    mock_class.__name__ = "TestClass"
    mock_class.a_method = MagicMock()

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._get_coroutine_methods",
        return_value=[],
    ):
        result = await ClassDataModelFactory._get_coroutine_methods(mock_class)
        assert result == []


@pytest.mark.asyncio
async def test_non_existent_class():
    mock_class = None  # Non-existent class to simulate an error case

    with pytest.raises(TypeError):
        await ClassDataModelFactory._get_coroutine_methods(mock_class)


@pytest.mark.asyncio
async def test_non_class_object():
    mock_obj = MagicMock()

    with patch(
        "code_autoeval.llm_model.utils.model.class_data_model.ClassDataModelFactory._get_coroutine_methods",
        return_value=[],
    ):
        result = await ClassDataModelFactory._get_coroutine_methods(mock_obj)
        assert result == []
