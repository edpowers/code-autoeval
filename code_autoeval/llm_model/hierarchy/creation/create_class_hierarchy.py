"""Create the class hierarchy."""

from typing import Any, Dict

import pydantic
from pydantic import BaseModel

from code_autoeval.llm_model.hierarchy.creation.class_hierarchy_extractor import (
    ClassHierarchyExtractor,
)


class ClassHierarchy(BaseModel):
    """Class hierarchy."""

    class_hierarchy: Dict[str, Any]  # The class hierarchy
    filtered_hierarchy: Dict[str, Any]  # The filtered class hierarchy
    mock_classes: Dict[str, object]  # The mock classes for the class hierarchy
    formatted_classes: str  # The formatted mock classes for the class hierarchy

    def __repr__(self) -> str:
        return f"""
        Class Hierarchy:
        {self.class_hierarchy}
        Filtered Hierarchy:
        {self.filtered_hierarchy}
        Mock Classes:
        {self.mock_classes}
        Formatted Classes:
        {self.formatted_classes}
        """


class CreateClassHierarchy:
    """Create the class hierarchy for a given directory."""

    @classmethod
    def construct_class_hierarchy(
        cls, class_path: str = "code_autoeval.llm_model.llm_model.LLMModel"
    ) -> ClassHierarchy:
        instance = cls()
        class_hierarchy = instance._analyze_class(class_path)

        # Apply this filter to your class hierarchy
        filtered_hierarchy = {
            class_name: instance._filter_relevant_members(class_info)
            for class_name, class_info in class_hierarchy.items()
            if class_name not in {"BaseModel", "Config"}
        }

        return ClassHierarchy(
            class_hierarchy=class_hierarchy,
            filtered_hierarchy=filtered_hierarchy,
            mock_classes={},
            formatted_classes="",
        )

    def _analyze_class(self, class_path: str) -> Dict[str, Any]:

        hierarchy_extractor = ClassHierarchyExtractor()
        try:
            module_name, class_name = class_path.rsplit(".", 1)
            module = __import__(module_name, fromlist=[class_name])
            class_obj = getattr(module, class_name)

            return hierarchy_extractor.extract_class_hierarchy(class_obj, module)
        except Exception as e:
            print(f"Error analyzing class: {e}")
            return None

    def _filter_relevant_members(self, class_info: dict) -> dict:
        base_model = pydantic.BaseModel.__dict__.keys()

        relevant_methods = [
            (name, method_type, inherited)
            for name, method_type, inherited in class_info["methods"]
            if (name not in base_model and inherited == "defined")
        ]

        relevant_attributes = {
            attr: value
            for attr, value in class_info["attributes"].items()
            if not attr.startswith("_") and attr not in base_model
        }

        return {
            "parent_classes": class_info["parent_classes"],
            "methods": relevant_methods,
            "attributes": relevant_attributes,
            "dependencies": class_info["dependencies"],
            "class_obj": class_info["class_obj"],
        }
