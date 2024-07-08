"""Create the class hierarchy."""

import inspect
import sys
from types import ModuleType
from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock

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

        # Generate mock classes
        # mock_classes = instance._generate_mock_classes(filtered_hierarchy)

        # formatted_classes = instance._format_mock_classes_for_prompt(
        #    mock_classes, filtered_hierarchy
        # )

        return ClassHierarchy(
            class_hierarchy=class_hierarchy,
            filtered_hierarchy=filtered_hierarchy,
            mock_classes={},
            formatted_classes="",
            # mock_classes=mock_classes,
            # formatted_classes=formatted_classes,
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

    def __extract_class_hierarchy(
        self, class_object: object, module: ModuleType
    ) -> Dict[str, Any]:

        def get_pydantic_fields(cls: object) -> Dict[str, Any]:
            if issubclass(cls, BaseModel):
                return {
                    field_name: field.annotation
                    for field_name, field in cls.model_fields.items()
                }
            return {}

        def is_custom_class(cls: type) -> bool:
            """
            Determine if a class is a custom class (not builtin or from standard library).
            """
            if cls.__module__ == "builtins":
                return False
            if cls.__module__.startswith("pydantic"):
                return False
            return cls.__module__ not in sys.stdlib_module_names

        def get_class_info(cls: object) -> Dict[str, Any]:
            methods = [
                name
                for name, obj in inspect.getmembers(cls)
                if inspect.isfunction(obj) and not name.startswith("__")
            ]

            attributes = {}
            dependencies: List[Tuple[str, Any]] = []

            for name, value in cls.__dict__.items():
                if name.startswith("__") or inspect.isfunction(value):
                    continue

                if issubclass(cls, BaseModel):
                    pydantic_fields = get_pydantic_fields(cls)
                    for field_name, field_type in pydantic_fields.items():
                        if field_name in [d[0] for d in dependencies]:
                            continue

                        if isinstance(field_type, type) and is_custom_class(field_type):
                            dependencies.append((field_name, field_type))
                        else:
                            attributes[field_name] = field_type

                if inspect.isclass(value):
                    if is_custom_class(value):
                        dependencies.append((name, value))
                    else:
                        attributes[name] = value
                elif isinstance(value, pydantic.fields.FieldInfo):
                    if inspect.isclass(value.default_factory) and is_custom_class(
                        value.default_factory
                    ):
                        dependencies.append((name, value.default_factory))
                    elif callable(value.default_factory) and is_custom_class(
                        value.default_factory
                    ):
                        dependencies.append((name, value.default_factory))
                    else:
                        attributes[name] = type(value.default)
                else:
                    attributes[name] = type(value)

            # Handle Pydantic model fields
            if issubclass(cls, BaseModel):
                for name, field in cls.model_fields.items():
                    if name not in attributes and name not in [
                        d[0] for d in dependencies
                    ]:
                        if inspect.isclass(field.annotation) and is_custom_class(
                            field.annotation
                        ):
                            dependencies.append((name, field.annotation))
                        else:
                            attributes[name] = field.annotation

            return {
                "parent_classes": [
                    base
                    for base in cls.__bases__
                    if is_custom_class(base)
                    and base.__name__ not in {"BaseModel", "Config"}
                ],
                "methods": methods,
                "attributes": attributes,
                "dependencies": list(set(dependencies)),
                "class_obj": cls,
            }

        def traverse_hierarchy(cls: object, module: ModuleType) -> Dict[str, Any]:
            hierarchy = {cls.__name__: get_class_info(cls)}

            for base in cls.__bases__:
                if base.__name__ not in {"object", "BaseModel", "Config", "set"}:
                    hierarchy.update(traverse_hierarchy(base, module))

            for dep_name, dep_class in hierarchy[cls.__name__]["dependencies"]:

                if dep_class.__module__ == "builtins":
                    continue

                if dep_class.__name__ not in hierarchy:
                    if hasattr(cls, dep_name):
                        hierarchy[dep_class.__name__] = get_class_info(dep_class)
                    else:
                        # If it's a separate class entirely and needs to be imported
                        hierarchy[dep_class.__name__] = get_class_info(dep_class)

            return hierarchy

        return traverse_hierarchy(class_object, module)

    def _filter_relevant_members(self, class_info: dict) -> dict:
        base_model = pydantic.BaseModel.__dict__.keys()

        relevant_methods = [
            method
            for method in class_info["methods"]
            if not method.startswith("_") and method not in base_model
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

    def _generate_mock_classes(self, hierarchy: dict) -> Dict[str, object]:
        mock_classes = {}

        def create_mock_class(class_name: str) -> object:
            if class_name in mock_classes:
                return mock_classes[class_name]

            class_info = hierarchy[class_name]
            bases = tuple(
                create_mock_class(parent) for parent in class_info["parent_classes"]
            ) or (MagicMock,)

            mock_class = type(f"Mock{class_name}", bases, {})

            for method in class_info["methods"]:
                setattr(mock_class, method, MagicMock())

            for attr in class_info["attributes"]:
                setattr(mock_class, attr, MagicMock())

            mock_classes[class_name] = mock_class
            return mock_class

        for class_name in hierarchy:
            create_mock_class(str(class_name))

        return mock_classes

    def _format_mock_classes_for_prompt(
        self, mock_classes: Dict[str, object], filtered_hierarchy: dict
    ) -> str:
        formatted_classes = []
        for class_name in mock_classes:
            class_info = filtered_hierarchy[class_name]
            formatted_class = f"""
        class Mock{class_name}({', '.join([f'Mock{parent}' for parent in class_info['parent_classes']]) or 'MagicMock'}):
            # Methods
            {chr(10).join([f'{method} = MagicMock()' for method in class_info['methods']])}

            # Attributes
            {chr(10).join([f'{attr} = MagicMock()' for attr in class_info['attributes']])}
        """
            formatted_classes.append(formatted_class)
        return "\n".join(formatted_classes)
