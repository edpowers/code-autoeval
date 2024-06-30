"""Model for function attributes."""

from typing import List

from pydantic import BaseModel


class FunctionAttributes(BaseModel):
    """Model for function attributes."""

    func_name: str
    function_signature: str
    function_docstring: str
    function_body: str
    init_params: List[str]
    base_classes: List[str]
    class_attributes: List[str]
    absolute_path: str
