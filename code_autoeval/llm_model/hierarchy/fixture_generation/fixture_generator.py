import ast
import os
import sys
from pathlib import Path
from typing import Dict

from pydantic import BaseModel

from code_autoeval.llm_model.hierarchy.fixture_generation.split_and_verify_code import (
    CodeVerificationError,
    EmptyTestCodeError,
    SplitAndVerifyCode,
    TestCodeVerificationError,
)
from code_autoeval.llm_model.utils import extraction
from code_autoeval.llm_model.utils.model import class_data_model
from code_autoeval.llm_model.utils.model_response.stream_response import StreamResponse

IMPORT_BANK = {
    "Path": "from pathlib import Path",
    "logging": "import logging",
    "datetime": "from datetime import datetime",
    "json": "import json",
    "re": "import re",
    "os": "import os",
    "sys": "import sys",
    # Add more as needed
}


class FixtureGenerator(BaseModel):
    stream_response: StreamResponse  # Replace with the actual LLM model type
    class_hierarchy: Dict[int, Dict[str, dict]]
    class_data_factory: class_data_model.ClassDataModelFactory  # Instantiated
    base_output_dir: str
    project_root: str
    clean_output_dir: bool = True
    unique_project_imports: Dict[str, str] = (
        extraction.find_unique_imports_from_directory.FindUniqueImportsFromDirectory.find_unique_imports_from_dir()
    )

    class Config:
        arbitrary_types_allowed = True

    def get_project_structure(self) -> str:
        fixture_dir = Path(self.base_output_dir) / "fixtures"
        structure = ["Fixtures:"]

        for file_path in fixture_dir.rglob("*.py"):
            relative_path = file_path.relative_to(fixture_dir)
            structure.append(f"  {relative_path}")

        return "\n".join(structure)

    def clean_output_directory_before_run(self) -> None:
        # Find all files in the fixtures directory and delete them
        fixtures_dir = Path(self.base_output_dir)
        for file_path in fixtures_dir.rglob("*"):
            if file_path.is_file():
                os.remove(file_path)

    def write_code_to_file(self, code: str, file_path: str) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(code)

    def create_prompt_for_class(
        self,
        class_name: str,
        class_info: dict,
        level: int,
        previous_levels: Dict[int, Dict[str, dict]],
    ) -> str:
        project_structure = self.get_project_structure()

        IMPORT_BANK.update(self.unique_project_imports)

        # Analyze class attributes to determine necessary imports
        necessary_imports = set()
        for attr_name, attr_type in class_info["attributes"].items():
            attr_type_str = str(attr_type)
            for type_key, import_statement in IMPORT_BANK.items():
                if type_key in attr_type_str:
                    necessary_imports.add(import_statement)

        # Create a list of previously defined fixtures
        previous_fixtures = [
            f"fixture_mock_{cls.lower()}"
            for lvl in previous_levels.values()
            for cls in lvl.keys()
        ]

        # Identify which parent classes and dependencies have fixtures
        parent_fixtures = [
            f"fixture_mock_{parent.__name__.lower()}"
            for parent in class_info["parent_classes"]
            if f"fixture_mock_{parent.__name__.lower()}" in previous_fixtures
        ]
        parent_imports = [
            f"from {parent.__module__} import {parent.__name__}"
            for parent in class_info["parent_classes"]
        ]

        dependency_fixtures = [
            f"fixture_mock_{dep[1].__name__.lower()}"
            for dep in class_info["dependencies"]
            if self.is_custom_class(dep[1])
            and f"fixture_mock_{dep[1].__name__.lower()}" in previous_fixtures
        ]

        fixture_imports = [
            f"from generated_code.fixtures.fixtures.{fixture.replace('fixture_mock_', '')}_fixture import {fixture}"
            for fixture in parent_fixtures + dependency_fixtures
        ]

        is_pydantic_model = "BaseModel" in [
            parent.__name__ for parent in class_info["parent_classes"]
        ]

        fixture_content = f"""
        @pytest.fixture
        def fixture_mock_{class_name.lower()}():
            mock = MagicMock(spec={class_name})
        """

        if is_pydantic_model:
            fixture_content += """
            # Setup Config for Pydantic model
            mock.Config = MagicMock()
            mock.Config.arbitrary_types_allowed = True
            """

        for attr, type_ in class_info["attributes"].items():
            fixture_content += f"""
            mock.{attr} = {self.get_default_value(type_)}
            """

        fixture_content += """
        return mock
        """

        test_content = f"""
        def test_mock_{class_name.lower()}(fixture_mock_{class_name.lower()}):
            assert isinstance(fixture_mock_{class_name.lower()}, {class_name})
        """

        if is_pydantic_model:
            test_content += f"""
            assert hasattr(fixture_mock_{class_name.lower()}, 'Config')
            assert fixture_mock_{class_name.lower()}.Config.arbitrary_types_allowed is True
            """

        for attr, type_ in class_info["attributes"].items():
            if str(type_) != "typing.Any":
                test_content += f"""
            assert hasattr(mock_{class_name.lower()}, '{attr}')
            assert isinstance(mock_{class_name.lower()}.{attr}, {self.get_type_name(type_)})
        """
            else:
                test_content += f"""
            assert hasattr(mock_{class_name.lower()}, '{attr}')
            # Skipping isinstance check for 'Any' type
        """

        for parent in class_info["parent_classes"]:
            test_content += f"""
            assert isinstance(fixture_mock_{class_name.lower()}, {parent.__name__})
            """

        return f"""
        You are an AI assistant specialized in generating pytest fixtures and tests for Python classes. Your task is to create fixtures and tests for the following class in a complex class hierarchy:

        Project structure:
        {project_structure}

        Class details:
        - Name: {class_name}
        - Level in hierarchy: {level}
        - File path: {class_info['class_obj'].__module__}
        - Parent classes: {[parent.__name__ for parent in class_info['parent_classes']]}
        - Dependencies: {[dep[1].__name__ for dep in class_info['dependencies'] if self.is_custom_class(dep[1])]}
        - Methods: {class_info['methods']}
        - Attributes: {class_info['attributes']}

        Previously defined fixtures to be used:
        - Parent Fixtures: {parent_fixtures}
        - Dependency Fixtures: {dependency_fixtures}

        Please generate the following:
        1. Fixture file content (fixtures/{class_name.lower()}_fixture.py):
        - Include the following imports:
        from unittest.mock import MagicMock
        import pytest
        from {class_info['class_obj'].__module__} import {class_name}
        {chr(10).join(sorted(necessary_imports))}
        {chr(10).join(parent_imports)}
        - Include the following imports for previously defined fixtures:
        {chr(10).join(fixture_imports)}
        - Create a fixture function with the following structure:
        @pytest.fixture
        def fixture_mock_{class_name.lower()}():
            # Function body here
        - If you need to specify a name in the decorator, use: @pytest.fixture(name="fixture_mock_{class_name.lower()}")
        {fixture_content}

        2. Test file content (tests/test_{class_name.lower()}_fixture.py):
        - Include the following imports:
        import pytest
        from generated_code.fixtures.fixtures.{class_name.lower()}_fixture import fixture_mock_{class_name.lower()}
        from {class_info['class_obj'].__module__} import {class_name}
        {chr(10).join(sorted(necessary_imports))}
        - Create test functions that verify:
        a. The mock object is an instance of the class
        b. All methods are present and can be called
        c. All attributes are present and have appropriate default values
        d. The object correctly inherits from its parent classes
        e. Dependencies are properly mocked and accessible
        {test_content}

        3. Please generate the following:

            3.1. Fixture file content for fixtures/{class_name.lower()}_fixture.py
            3.2. Test file content for tests/test_{class_name.lower()}_fixture.py
            3.3. A brief explanation of what the fixture does, how it uses fixtures from previous levels, and how it can be used in testing. This line should start with a #

            IMPORTANT:
            - Provide the code exactly as it should appear in the Python files.
            - Do not use any markdown syntax, backticks, or formatting.
            - Do not include any comments in the code.
            - The code should be ready to run as-is when copied into a .py file.
            - Generate complete, ready-to-use code for both the fixture and test files.
            - Do not use placeholder comments or TODO statements.

            For each file:
            - Start with "File: [filename]" on a new line.
            - On the next line, provide the file content without any additional formatting.
            - Separate the two files with a blank line.

            Ensure the code is properly formatted, syntactically correct, and follows Python best practices. Use absolute imports starting from the project root (code_autoeval).

        """

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

    async def generate_fixture_and_test(
        self,
        class_name: str,
        class_info: dict,
        level: int,
        previous_levels: Dict[int, Dict[str, dict]],
    ) -> str:
        prompt = self.create_prompt_for_class(
            class_name, class_info, level, previous_levels
        )

        # Use the LLM model to generate the fixture and test code
        response = await self.stream_response.ask_backend_model(prompt)
        return self.stream_response.figure_out_model_response(response)

    async def generate_fixtures_for_level(self, level: int) -> None:
        classes = self.class_hierarchy[level]
        previous_levels = {l: self.class_hierarchy[l] for l in range(1, level)}

        for class_name, class_info in classes.items():

            if class_name == "Config":
                continue

            fixture_path = os.path.join(
                self.base_output_dir, "fixtures", f"{class_name.lower()}_fixture.py"
            )
            test_path = os.path.join(
                self.base_output_dir, "tests", f"test_{class_name.lower()}_fixture.py"
            )

            if Path(fixture_path).exists() and Path(test_path).exists():
                continue

            combined_code = await self.generate_fixture_and_test(
                class_name, class_info, level, previous_levels
            )

            try:
                fixture_code, test_code = SplitAndVerifyCode.split_and_verify_code(
                    combined_code,
                    self.class_data_factory.find_class_info(class_name),
                    unique_project_imports=self.unique_project_imports,
                )
            except CodeVerificationError as e:
                print(
                    f"Error generating {'fixture' if e.error_type == 'fixture' else 'test'} for {class_name}:"
                )
                print(f"Error message: {e.message}")
                print("Problematic code:")
                print(e.code)
                print("\nAST structure:")

                try:
                    tree = ast.parse(e.code)
                    print(SplitAndVerifyCode.ast_to_dict(tree))
                except SyntaxError:
                    print("Unable to parse AST due to syntax error")
                continue
            except TestCodeVerificationError as e:
                print(f"Error generating test for {class_name}:")
                print(f"Error message: {e.message}")
                print("Problematic node:")
                print(ast.dump(e.node, indent=2))
                continue
            except EmptyTestCodeError as e:
                print(f"Error generating test for {class_name}:")
                print(f"Error message: {e.message}")
                print("The generated test code is empty or contains no test functions.")
                continue

            self.write_code_to_file(fixture_code, fixture_path)
            self.write_code_to_file(test_code, test_path)

            print(f"Generated fixture and test for {class_name}")

    async def generate_all_fixtures(self) -> None:
        if self.clean_output_dir:
            self.clean_output_directory_before_run()

        for level in sorted(self.class_hierarchy.keys()):
            print(f"Generating fixtures for level {level}")
            await self.generate_fixtures_for_level(level)
            await self.generate_fixtures_for_level(level)
            await self.generate_fixtures_for_level(level)

    def get_default_value(self, type_: type) -> str:
        """Return a default value string for a given type."""
        type_str = str(type_)
        if "Path" in type_str:
            return "Path('/')"
        elif "Logger" in type_str:
            return "logging.getLogger('test')"
        elif "DataFrame" in type_str:
            return "pd.DataFrame()"
        elif "ndarray" in type_str:
            return "np.array([])"
        elif type_ == str:
            return "''"
        elif type_ in (int, float):
            return "0"
        elif type_ == bool:
            return "False"
        elif "datetime" in type_str:
            return "datetime.now()"
        elif "list" in type_str.lower():
            return "[]"
        elif "dict" in type_str.lower():
            return "{}"
        else:
            return "None"

    def get_type_name(self, type_: type) -> str:
        """Return the type name as a string."""
        type_str = str(type_)
        if "typing.Any" in type_str:
            return "object"  # Use 'object' as a fallback for 'Any'
        elif "Path" in type_str:
            return "Path"
        elif "Logger" in type_str:
            return "logging.Logger"
        elif "DataFrame" in type_str:
            return "pd.DataFrame"
        elif "ndarray" in type_str:
            return "np.ndarray"
        else:
            return type_.__name__
