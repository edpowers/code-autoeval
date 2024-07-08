import inspect
import sys
from types import ModuleType
from typing import Any, Dict, List, Tuple

import pydantic
from pydantic import BaseModel


class ClassHierarchyExtractor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_pydantic_fields(cls: object) -> Dict[str, Any]:
        if issubclass(cls, BaseModel):
            return {
                field_name: field.annotation
                for field_name, field in cls.model_fields.items()
            }
        return {}

    @staticmethod
    def is_custom_class(cls: type) -> bool:
        """
        Determine if a class is a custom class (not builtin or from standard library).
        """
        if cls.__module__ == "builtins":
            return False
        if cls.__module__.startswith("pydantic"):
            return False
        return cls.__module__ not in sys.stdlib_module_names

    def get_class_info(self, cls: object) -> Dict[str, Any]:
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
                pydantic_fields = self.get_pydantic_fields(cls)
                for field_name, field_type in pydantic_fields.items():
                    if field_name in [d[0] for d in dependencies]:
                        continue

                    if isinstance(field_type, type) and self.is_custom_class(
                        field_type
                    ):
                        dependencies.append((field_name, field_type))
                    else:
                        attributes[field_name] = field_type

            if inspect.isclass(value):
                if self.is_custom_class(value):
                    dependencies.append((name, value))
                else:
                    attributes[name] = value
            elif isinstance(value, pydantic.fields.FieldInfo):
                if inspect.isclass(value.default_factory) and self.is_custom_class(
                    value.default_factory
                ):
                    dependencies.append((name, value.default_factory))
                elif callable(value.default_factory) and self.is_custom_class(
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
                if name not in attributes and name not in [d[0] for d in dependencies]:
                    if inspect.isclass(field.annotation) and self.is_custom_class(
                        field.annotation
                    ):
                        dependencies.append((name, field.annotation))
                    else:
                        attributes[name] = field.annotation

        return {
            "parent_classes": [
                base
                for base in cls.__bases__
                if self.is_custom_class(base)
                and base.__name__ not in {"BaseModel", "Config"}
            ],
            "methods": methods,
            "attributes": attributes,
            "dependencies": list(set(dependencies)),
            "class_obj": cls,
        }

    def traverse_hierarchy(self, cls: object, module: ModuleType) -> Dict[str, Any]:
        hierarchy = {cls.__name__: self.get_class_info(cls)}

        for base in cls.__bases__:
            if base.__name__ not in {"object", "BaseModel", "Config", "set"}:
                hierarchy.update(self.traverse_hierarchy(base, module))

        for dep_name, dep_class in hierarchy[cls.__name__]["dependencies"]:
            if dep_class.__module__ == "builtins":
                continue

            if dep_class.__name__ not in hierarchy:
                if hasattr(cls, dep_name):
                    hierarchy[dep_class.__name__] = self.get_class_info(dep_class)
                else:
                    # If it's a separate class entirely and needs to be imported
                    hierarchy[dep_class.__name__] = self.get_class_info(dep_class)

        return hierarchy

    def extract_class_hierarchy(
        self, class_object: object, module: ModuleType
    ) -> Dict[str, Any]:
        return self.traverse_hierarchy(class_object, module)
