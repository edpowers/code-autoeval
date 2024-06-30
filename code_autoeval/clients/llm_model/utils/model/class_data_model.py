"""Model the class data getting passed into generate code."""

from typing import List

from pydantic import BaseModel


class ClassDataModel(BaseModel):
    """Class data."""

    class_object: object  # The actual class object
    class_name: str  # The name of the class
    class_methods: List[str]  # The methods (functions) of the class
    class_attributes: List[str]  # The attributes of the class
    init_params: List[str]  # The parameters of the __init__ method
    base_classes: List[str]  # The base classes of the class
    absolute_path: str  # The absolute path to the class file - full path on host system
