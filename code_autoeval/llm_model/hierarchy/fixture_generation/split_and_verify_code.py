"""Split and verify the test/fixture code."""

import ast
import re
from pprint import pprint
from typing import Any, Dict

from multiuse.model import class_data_model

from code_autoeval.llm_model.utils.code_cleaning.run_flake8_fix_imports import (
    RunFlake8FixImports,
)
from code_autoeval.llm_model.utils.extraction.extract_imports_from_file import (
    ExtractImportsFromFile,
)


class CodeVerificationError(Exception):
    def __init__(self, message: str, code: str, error_type: str):
        self.message = message
        self.code = code
        self.error_type = error_type
        super().__init__(self.message)


class TestCodeVerificationError(Exception):
    def __init__(self, message: str, node: ast.AST):
        self.message = message
        self.node = node
        super().__init__(self.message)


class SyntaxErrorWithCode(SyntaxError):
    def __init__(self, msg: str, code: str):
        super().__init__(msg)
        self.code = code


class EmptyTestCodeError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SplitAndVerifyCode:

    @classmethod
    def split_and_verify_code(
        cls,
        code: str,
        class_model: class_data_model.ClassDataModel,
        unique_project_imports: Dict[str, str],
    ) -> tuple[str, str]:
        """
        Split the code into fixture and test parts, and verify their contents.
        """
        instance = cls()
        fixture_code = ""
        test_code = ""
        # Try to split by our specified headers first
        # Try to split by our specified headers first
        parts = code.split("# File: fixtures/")
        if len(parts) == 2:
            fixture_and_test = parts[1].split("# File: tests/")
            if len(fixture_and_test) == 2:
                fixture_code = fixture_and_test[0].strip()
                test_code = fixture_and_test[1].strip()
        else:
            # If that fails, try to extract code from markdown code blocks
            code_blocks = re.findall(r"```python\n(.*?)```", code, re.DOTALL)
            if len(code_blocks) >= 2:
                fixture_code = code_blocks[0].strip()
                test_code = code_blocks[-1].strip()
            else:
                # If both methods fail, try to split based on the structure of the pasted content
                parts = code.split("# File: tests/")
                if len(parts) == 2:
                    fixture_code = parts[0].split("# File: fixtures/")[1].strip()
                    test_code = parts[1].strip()
                else:
                    pprint(code)
                    raise ValueError(
                        "Could not find separate fixture and test code sections"
                    )

        # Remove any remaining markdown or comments
        fixture_code = cls.clean_code(fixture_code)
        test_code = cls.clean_code(test_code)

        original_code, original_imports = (
            ExtractImportsFromFile.find_original_code_and_imports(class_model)
        )

        # Using the flake8 and the full import dict,
        fixture_code, was_modified = (
            RunFlake8FixImports.run_flake8_pipeline_with_temp_file(
                fixture_code,
                class_model=class_model,
                original_imports=original_imports,
                unique_project_imports=unique_project_imports,
            )
        )
        # Using the flake8 and the full import dict,
        test_code, was_modified = (
            RunFlake8FixImports.run_flake8_pipeline_with_temp_file(
                test_code,
                class_model=class_model,
                original_imports=original_imports,
                unique_project_imports=unique_project_imports,
            )
        )

        try:
            if not instance.verify_fixture_code(fixture_code):
                raise CodeVerificationError(
                    "Fixture code verification failed", fixture_code, "fixture"
                )
        except SyntaxError as e:
            raise CodeVerificationError(
                f"Syntax error in fixture code: {str(e)}", fixture_code, "fixture"
            )

        try:
            if not instance.verify_test_code(test_code):
                raise CodeVerificationError(
                    "Test code verification failed", test_code, "test"
                )
        except SyntaxError as e:
            raise CodeVerificationError(
                f"Syntax error in test code: {str(e)}", test_code, "test"
            )

        return fixture_code, test_code

    @classmethod
    def verify_fixture_code(cls, code: str) -> bool:
        try:
            tree = ast.parse(code)
            has_mock_import = False
            has_pytest_import = False
            has_class_import = False
            has_fixture = False

            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    for name in node.names:
                        if name.name == "MagicMock" or name.name == "unittest.mock":
                            has_mock_import = True
                        elif name.name == "pytest":
                            has_pytest_import = True
                        elif "code_autoeval" in getattr(node, "module", ""):
                            has_class_import = True
                elif isinstance(node, ast.FunctionDef):
                    decorators = node.decorator_list
                    if any(cls.is_pytest_fixture_decorator(d) for d in decorators):
                        has_fixture = True
                        # Check if the fixture name is correct (either in function name or decorator)
                        correct_name = node.name.startswith("fixture_mock_") or any(
                            cls.has_correct_fixture_name(d) for d in decorators
                        )
                        if not correct_name:
                            pprint(code)
                            raise CodeVerificationError(
                                "Fixture name is incorrect", code, "fixture"
                            )

            if not all(
                (has_mock_import, has_pytest_import, has_class_import, has_fixture)
            ):
                raise CodeVerificationError(
                    "Fixture code verification failed", code, "fixture"
                )

            return (
                has_mock_import
                and has_pytest_import
                and has_class_import
                and has_fixture
            )
        except SyntaxError as e:
            raise SyntaxErrorWithCode(str(e), code) from e

    @staticmethod
    def has_correct_fixture_name(decorator: Any) -> bool:
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == "name" and isinstance(keyword.value, ast.Str):
                    return keyword.value.s.startswith("mock_")
        return False

    @classmethod
    def verify_test_code(cls, code: str) -> bool:
        """
        Verify that the test code contains only test-related content.
        """
        if not code.strip():
            raise EmptyTestCodeError("The generated test code is empty.")

        try:
            tree = ast.parse(code)
            test_function_count = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("test_"):
                        raise TestCodeVerificationError(
                            f"Function '{node.name}' does not start with 'test_'", node
                        )
                    # Ensure no decorators are present
                    if getattr(node, "decorator_list", []):
                        raise TestCodeVerificationError(
                            f"Function '{node.name}' has unexpected decorators", node
                        )
                    test_function_count += 1
                elif isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef)):
                    raise TestCodeVerificationError(
                        f"Unexpected {type(node).__name__} found", node
                    )

            if test_function_count == 0:
                raise EmptyTestCodeError(
                    "No test functions found in the generated code."
                )

            return True
        except SyntaxError as e:
            raise SyntaxErrorWithCode(str(e), code) from e
        except TestCodeVerificationError as e:
            print(f"Test code verification failed: {e.message}")
            print(f"Problematic node: {ast.dump(e.node, indent=2)}")
            return False

    @staticmethod
    def ast_to_dict(node: Any) -> dict:
        """Convert an AST node to a dictionary."""
        return {
            key: (
                SplitAndVerifyCode.ast_to_dict(value)
                if isinstance(value, ast.AST)
                else (
                    [SplitAndVerifyCode.ast_to_dict(item) for item in value]
                    if isinstance(value, list)
                    else value
                )
            )
            for key, value in ast.iter_fields(node)
            if key != "ctx"
        }

    @staticmethod
    def is_pytest_fixture_decorator(decorator: Any) -> bool:
        if isinstance(decorator, ast.Name) and decorator.id == "pytest":
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == "fixture":
            return True
        if isinstance(decorator, ast.Call):
            func = decorator.func
            return (isinstance(func, ast.Name) and func.id == "pytest") or (
                isinstance(func, ast.Attribute) and func.attr == "fixture"
            )
        return False

    @staticmethod
    def clean_code(code: str) -> str:
        # If the first line strip() ends with .py, then add a # to the start of the line
        if code.strip().split("\n")[0].strip().endswith(".py"):
            code = "# " + code

        # Remove markdown code block syntax if present
        code = re.sub(r"```python\n|```$", "", code, flags=re.MULTILINE)

        # Remove comments that start with #
        code = re.sub(r"#.*$", "", code, flags=re.MULTILINE)

        # Remove empty lines
        code = "\n".join(line for line in code.split("\n") if line.strip())

        return code.strip().strip("```python")
