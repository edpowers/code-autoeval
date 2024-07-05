import pytest
from typing import List, Any

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

##################################################
# TESTS
##################################################

@pytest.mark.asyncio
async def test_empty_list():
    model = PrettyPrintBaseModel(None)
    result = await model._format_list([])
    assert result == "[]"

@pytest.mark.asyncio
async def test_single_item_list():
    model = PrettyPrintBaseModel(None)
    result = await model._format_list([42])
    assert result == "[42]"

@pytest.mark.asyncio
async def test_multiple_items_list():
    model = PrettyPrintBaseModel(None)
    result = await model._format_list([1, 2, "three"])
    expected = (
        "[\n"
        "                1,\n"
        "                2,\n"
        '                "three"\n'
        "            ]"
    )
    assert result == expected

@pytest.mark.asyncio
async def test_empty_list_with_docstring():
    model = PrettyPrintBaseModel(None)
    docstring_model = PrettyPrintBaseModel("")
    result = await docstring_model._format_list([])
    assert result == "[]"

@pytest.mark.asyncio
async def test_none_input():
    model = PrettyPrintBaseModel(None)
    with pytest.raises(TypeError):
        await model._format_list(None)