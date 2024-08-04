"""Extract the fixture information from auto-generated code."""

import ast
from pathlib import Path
from typing import Dict, List

from code_autoeval.llm_model.utils import model


class FixtureParser:
    """Extract the fixture information from auto-generated code.

    Attributes
    ----------
    fixtures_by_file : Dict[str, List[model.FixtureInfo]]
        A dictionary mapping the file path to a list of fixture information.

    fixtures_by_class : Dict[str, model.ClassFixtures]
        A dictionary mapping the class name to the fixtures associated with that class.

    Example
    -------
    >>> parser = FixtureParser()
    >>> parser.parse_file("path/to/file.py")

    >>> parser.parse_directory("path/to/directory")

    ### Finding the fixtures for a class based on class name
    >>> parser.get_fixtures_for_class("ClassName")
    """

    fixtures_by_file: Dict[str, List[model.FixtureInfo]] = {}
    fixtures_by_class: Dict[str, model.ClassFixtures] = {}

    def __init__(self):
        ...
        # self.fixtures_by_file: Dict[str, List[model.FixtureInfo]] = {}
        # self.fixtures_by_class: Dict[str, model.ClassFixtures] = {}

    def parse_file(self, file_path: str) -> List[model.FixtureInfo]:
        with open(file_path, "r") as file:
            content = file.read()

        tree = ast.parse(content)
        fixtures = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if fixture_info := self._parse_fixture_function(node, file_path):
                    fixtures.append(fixture_info)

        self.fixtures_by_file[file_path] = fixtures
        return fixtures

    def parse_directory(self, directory_path: str) -> None:
        directory = Path(directory_path)
        for file_path in directory.rglob("*.py"):
            self.parse_file(str(file_path))

        # Print how many fixtures were found in total.
        self._log_total_fixtures_found()
        # Now iterate through the fixtures by file and map those to a dict
        # for each class name.
        self.associate_fixtures_with_classes()

    def _log_total_fixtures_found(self):
        total_fixtures = sum(
            len(fixtures) for fixtures in self.fixtures_by_file.values()
        )
        print(f"Total fixtures found: {total_fixtures}")

    def associate_fixtures_with_classes(self):
        all_fixtures = [
            fixture
            for fixtures in self.fixtures_by_file.values()
            for fixture in fixtures
        ]
        for fixture in all_fixtures:
            if fixture.imported_class_name:
                if fixture.imported_class_name not in self.fixtures_by_class:
                    self.fixtures_by_class[fixture.imported_class_name] = (
                        model.ClassFixtures(
                            class_name=fixture.imported_class_name, fixtures=[]
                        )
                    )
                self.fixtures_by_class[fixture.imported_class_name].fixtures.append(
                    fixture
                )

    def _parse_fixture_function(
        self, node: ast.FunctionDef, file_path: str
    ) -> model.FixtureInfo:
        if not self._is_fixture(node):
            return None
        fixture_name = node.name
        imported_class_name = None
        fixture_class_name = None

        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name) and target.id == "mock":
                        imported_class_name, fixture_class_name = (
                            self._extract_mock_info(stmt.value)
                        )

        return model.FixtureInfo(
            module_path=file_path,
            fixture_name=fixture_name,
            imported_class_name=imported_class_name,
            fixture_class_name=fixture_class_name,
            fixture_ast=node,
        )

    def _is_fixture(self, node: ast.FunctionDef) -> bool:
        return any(
            (isinstance(d, ast.Name) and d.id == "fixture")
            or (isinstance(d, ast.Attribute) and d.attr == "fixture")
            or (
                isinstance(d, ast.Call)
                and isinstance(d.func, (ast.Name, ast.Attribute))
                and (d.func.id if isinstance(d.func, ast.Name) else d.func.attr)
                == "fixture"
            )
            for d in node.decorator_list
        )

    def _extract_mock_info(self, value_node: ast.Call):
        imported_class_name = None
        fixture_class_name = None

        if isinstance(value_node.func, ast.Name) and value_node.func.id == "MagicMock":
            for keyword in value_node.keywords:
                if keyword.arg == "spec":
                    if isinstance(keyword.value, ast.Name):
                        imported_class_name = keyword.value.id
                    elif isinstance(keyword.value, ast.Attribute):
                        imported_class_name = keyword.value.attr
            fixture_class_name = "MagicMock"
        elif (
            isinstance(value_node.func, ast.Attribute)
            and value_node.func.attr == "Mock"
        ):
            imported_class_name = "Mock"
            fixture_class_name = "Mock"

        return imported_class_name, fixture_class_name

    def get_fixtures_for_class(self, class_name: str) -> model.ClassFixtures:
        return self.fixtures_by_class.get(
            class_name, model.ClassFixtures(class_name=class_name, fixtures=[])
        )

    def print_all_fixtures(self):
        for file_path, fixtures in self.fixtures_by_file.items():
            print(f"File: {file_path}")
            for fixture in fixtures:
                print(fixture)
            print()
