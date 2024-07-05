import re
from typing import Tuple
from unittest.mock import MagicMock, patch

import pytest


class LLMModel:
    def __init__(self, **kwargs):
        self.init_kwargs = kwargs

    def remove_non_code_patterns(self, content: str, code_type: str) -> str:
        # Placeholder for the actual implementation of remove_non_code_patterns
        return content

    def validate_func_name_in_code(self, main_code: str, func_name: str):
        # Placeholder for the actual implementation of validate_func_name_in_code
        pass

    def validate_test_in_pytest_code(self, pytest_tests: str):
        # Placeholder for the actual implementation of validate_test_in_pytest_code
        pass

@patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)
def split_content_from_model(self, content: str) -> Tuple[str, str]:
    if not re.search("# Test|pytest tests|test", content):
        raise ValueError("No '# Tests' provided in the model response. Unable to parse regex.")

    code = ""
    if code_blocks := re.findall(r"

", content, re.DOTALL):
        code = "\n\n".join(block.strip() for block in code_blocks)
    else:
        code = content

    class_def_exists = re.search(r"class [A-Z]{5,}", code)
    if not class_def_exists:
        return code.strip(), code.strip()

    if "### Explanation:" in code:
        code_parts = re.split(r"### Explanation:", code, maxsplit=1)
        code = code_parts[0]

    # Split the code part to separate pytest tests
    code_parts = re.split(
        r"(?m)^# Test[s]?(?:\s|$)|[Pp]ytest [Tt]ests|(?m)^# Updated Pytest Tests:",
        code,
        maxsplit=1,
    )

    if len(code_parts) > 1:
        main_code = code_parts[0]
        pytest_tests = (
            (code_parts[1] + code_parts[2])
            if len(code_parts) > 2
            else code_parts[1]
        )
        pytest_tests = pytest_tests.strip()
        if not pytest_tests.startswith("import pytest"):
            pytest_tests = "import pytest\n" + pytest_tests
    else:
        main_code = code
        pytest_tests = ""

    return main_code.strip(), pytest_tests.strip()

import re
from typing import Tuple
from unittest.mock import patch

import pytest


class LLMModel:
    def __init__(self, **kwargs):
        self.init_kwargs = kwargs

    def remove_non_code_patterns(self, content: str, code_type: str) -> str:
        # Placeholder for the actual implementation of remove_non_code_patterns
        return content

    def validate_func_name_in_code(self, main_code: str, func_name: str):
        # Placeholder for the actual implementation of validate_func_name_in_code
        pass

    def validate_test_in_pytest_code(self, pytest_tests: str):
        # Placeholder for the actual implementation of validate_test_in_pytest_code
        pass

@patch("code_autoeval.llm_model.llm_model.LLMModel.__init__", return_value=None)
def split_content_from_model(self, content: str) -> Tuple[str, str]:
    if not re.search("# Test|pytest tests|test", content):
        raise ValueError("No '# Tests' provided in the model response. Unable to parse regex.")

    code = ""
    if code_blocks := re.findall(r"

", content, re.DOTALL):
        code = "\n\n".join(block.strip() for block in code_blocks)
    else:
        code = content

    class_def_exists = re.search(r"class [A-Z]{5,}", code)
    if not class_def_exists:
        return code.strip(), code.strip()

    if "### Explanation:" in code:
        code_parts = re.split(r"### Explanation:", code, maxsplit=1)
        code = code_parts[0]

    # Split the code part to separate pytest tests
    code_parts = re.split(
        r"(?m)^# Test[s]?(?:\s|$)|[Pp]ytest [Tt]ests|(?m)^# Updated Pytest Tests:",
        code,
        maxsplit=1,
    )

    if len(code_parts) > 1:
        main_code = code_parts[0]
        pytest_tests = (
            (code_parts[1] + code_parts[2])
            if len(code_parts) > 2
            else code_parts[1]
        )
        pytest_tests = pytest_tests.strip()
        if not pytest_tests.startswith("import pytest"):
            pytest_tests = "import pytest\n" + pytest_tests
    else:
        main_code = code
        pytest_tests = ""

    return main_code.strip(), pytest_tests.strip()

##################################################
# TESTS
##################################################

@pytest.mark.parametrize("content, expected_main_code, expected_pytest_tests", [
    (
        "Some text\n

",
        "def test_example():\n    assert True",
        "import pytest\ndef test_example():\n    assert True"
    ),
    (
        "More text\n# Test some_function\n

",
        "# Test some_function\n

",
        "import pytest\n# Test some_function\n

"
    ),
    (
        "No tests here",
        "No tests here",
        ""
    )
])
def test_split_content_from_model(mock_init, content, expected_main_code, expected_pytest_tests):
    result = split_content_from_model(MagicMock(), content)
    assert result == (expected_main_code, expected_pytest_tests)

@pytest.mark.parametrize("content", [
    "No tests at all",
    "

"
])
def test_split_content_from_model_error(mock_init, content):
    with pytest.raises(ValueError):
        split_content_from_model(MagicMock(), content)

@pytest.mark.parametrize("content", [
    "Class definition\n

"
])
def test_split_content_from_model_with_class(mock_init, content):
    result = split_content_from_model(MagicMock(), content)
    assert result == (content.strip(), "")

@pytest.mark.parametrize("content", [
    "Explanation\n### Explanation:\nCode with explanation"
])
def test_split_content_from_model_with_explanation(mock_init, content):
    result = split_content_from_model(MagicMock(), content)
    assert result == ("Explanation\nCode with explanation", "")

@pytest.mark.parametrize("content", [
    "Multiple code blocks\n

\n

"
])
def test_split_content_from_model_multiple_blocks(mock_init, content):
    result = split_content_from_model(MagicMock(), content)
    assert result == ("Multiple code blocks", "import pytest\ndef func1():\n    pass\ndef func2():\n    pass")