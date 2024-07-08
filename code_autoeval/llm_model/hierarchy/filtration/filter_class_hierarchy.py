"""Filter the Hierarchical Classes."""

from typing import Dict, Set


class FilterClassHierarchy:
    """

    Example
    -------
    >>> created_hierarchy = (
        create_class_hierarchy.CreateClassHierarchy.construct_class_hierarchy()
    )
    >>> filter_hierarchy_classes = FilterClassHierarchy()
    >>> filter_hierarchy_classes.build_hierarchy_levels(created_hierarchy.filtered_hierarchy)
    >>> hierarchy_levels = filter_hierarchy_classes.get_hierarchy_levels()
    >>> filter_hierarchy_classes.print_hierarchy_levels(hierarchy_levels)
    """

    def __init__(self) -> None:
        self.hierarchy_levels: Dict[int, Dict[str, dict]] = {}

    def get_dependencies(self, class_info: dict) -> Set[str]:
        return {
            dep[1].__name__
            for dep in class_info["dependencies"]
            if self.is_custom_class(dep[1])
        } | {parent.__name__ for parent in class_info["parent_classes"]}

    def build_hierarchy_levels(self, hierarchy: Dict[str, dict]) -> None:
        remaining_classes = set(hierarchy.keys())
        level = 1

        while remaining_classes:
            current_level_classes = {
                class_name: class_info
                for class_name, class_info in hierarchy.items()
                if class_name in remaining_classes
                and all(
                    dep not in remaining_classes
                    for dep in self.get_dependencies(class_info)
                )
            }

            if not current_level_classes:
                raise ValueError("Circular dependency detected in the class hierarchy.")

            self.hierarchy_levels[level] = current_level_classes
            remaining_classes -= set(current_level_classes.keys())
            level += 1

    def get_hierarchy_levels(self) -> Dict[int, Dict[str, dict]]:
        return self.hierarchy_levels

    @staticmethod
    def is_custom_class(value: type) -> bool:
        return isinstance(value, type) and value.__module__ != "builtins"

    @staticmethod
    def print_hierarchy_levels(hierarchy_levels: Dict[int, Dict[str, dict]]) -> None:
        for level, classes in hierarchy_levels.items():
            print(f"Level {level}:")
            for class_name, class_info in classes.items():
                print(f"  {class_name}")
                print(
                    f"    Parents: {[parent.__name__ for parent in class_info['parent_classes']]}"
                )
                print(
                    f"    Dependencies: {[dep[1].__name__ for dep in class_info['dependencies'] if FilterClassHierarchy.is_custom_class(dep[1])]}"
                )
                print(f"    All attributes: {class_info['attributes']}")
            print()
