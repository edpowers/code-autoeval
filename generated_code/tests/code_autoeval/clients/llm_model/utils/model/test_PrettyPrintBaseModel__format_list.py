from typing import Any, List
from unittest.mock import patch

import pytest


# Function implementation provided by you
class PrettyPrintBaseModel:
    def __init__(self, data):
        self.data = data

    async def _format_list(self, items: List[Any]) -> str:
        if not items:
            return "[]"
        elif len(items) == 1:
            return f"[{repr(items[0])}]"
        else:
            formatted_items = ",\n                ".join(repr(item) for item in items)
            return f"[\n                {formatted_items}\n            ]"

# Analysis of the function:
# The function _format_list is designed to take a list of items and format it into a string representation.
# It handles three cases: an empty list, a single item list, and a multi-item list.
# For a single item, it uses repr() for simple formatting.
# For multiple items, it joins them with commas and newlines for better readability.

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.model.pretty_print_base_model.PrettyPrintBaseModel.__init__", return_value=None)
def test_empty_list(mock_init):
    # Arrange
    mock_instance = PrettyPrintBaseModel(data="test")
    
    # Act
    result = mock_instance._format_list([])
    
    # Assert
    assert result == "[]"

@patch("code_autoeval.clients.llm_model.utils.model.pretty_print_base_model.PrettyPrintBaseModel.__init__", return_value=None)
def test_single_item_list(mock_init):
    # Arrange
    mock_instance = PrettyPrintBaseModel(data="test")
    
    # Act
    result = mock_instance._format_list([42])
    
    # Assert
    assert result == "[42]"

@patch("code_autoeval.clients.llm_model.utils.model.pretty_print_base_model.PrettyPrintBaseModel.__init__", return_value=None)
def test_multi_item_list(mock_init):
    # Arrange
    mock_instance = PrettyPrintBaseModel(data="test")
    
    # Act
    result = mock_instance._format_list([1, 2, "three"])
    
    # Assert
    assert result == "[\n                1,\n                2,\n                'three'\n            ]"

@patch("code_autoeval.clients.llm_model.utils.model.pretty_print_base_model.PrettyPrintBaseModel.__init__", return_value=None)
def test_empty_list_with_mock(mock_init):
    # Arrange
    mock_instance = PrettyPrintBaseModel(data="test")
    
    # Act
    result = mock_instance._format_list([])
    
    # Assert
    assert result == "[]"

@patch("code_autoeval.clients.llm_model.utils.model.pretty_print_base_model.PrettyPrintBaseModel.__init__", return_value=None)
def test_none_input(mock_init):
    # Arrange
    mock_instance = PrettyPrintBaseModel(data="test")
    
    # Act & Assert
    with pytest.raises(TypeError):
        mock_instance._format_list(None)