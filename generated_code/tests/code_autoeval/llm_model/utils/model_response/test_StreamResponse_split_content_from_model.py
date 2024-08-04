## ",
##         }

##         code_str = code if re.search(r"|".join(test_patterns), code) else content

##         if match := re.search(r"|".join(test_patterns), code_str):
##             split_point = match.end()
##             code_parts = [code_str[:split_point].strip(), code_str[split_point:].strip()]
##             return code_parts[0], code_parts[1]

##         if "def test_" in content and "def test_" not in code:
##             if "### START OF TESTS" in content:
##                 split_index = content.find("### START OF TESTS") + len("### START OF TESTS")
##                 return content[:split_index].strip(), content[split_index:].strip()
##             else:
##                 raise NoTestsFoundError(
##                     "No tests found in the content. Please include tests in the content."
##                 )

##         class_def_exists = re.search(r"class [A-Z]{5,}", code) is not None
##         if not class_def_exists:
##             NoTestsFoundError.validate_tests_str(code)
##             return code.strip(), code.strip()

##         if "### Explanation:" in code:
##             split_index = code.find("### Explanation:") + len("### Explanation:")
##             code = code[:split_index].strip()

##         return code.strip(), code.strip()

import pytest
from unittest.mock import MagicMock
from code_autoeval.llm_model.utils.model_response.stream_response import StreamResponse, NoTestsFoundError

@pytest.fixture(scope='module')
def mock_streamresponse():
    return StreamResponse()

# Test case for normal use case with code blocks
def test_split_content_from_model_with_code_blocks(mock_streamresponse):
    content = """Some text before the code block.
```python
print("Hello, world!")
```
Some text after the code block."""
    
    expected_code = "print(\"Hello, world!\")"
    expected_tests = ""
    
    result = mock_streamresponse.split_content_from_model(content)
    
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected_code
    assert result[1] == expected_tests

# Test case for normal use case without code blocks
def test_split_content_from_model_without_code_blocks(mock_streamresponse):
    content = "No code block here."
    
    expected_code = "No code block here."
    expected_tests = ""
    
    result = mock_streamresponse.split_content_from_model(content)
    
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected_code
    assert result[1] == expected_tests

# Test case for edge case with no tests found in content
def test_split_content_from_model_no_tests_found(mock_streamresponse):
    content = "No tests here."
    
    with pytest.raises(NoTestsFoundError):
        mock_streamresponse.split_content_from_model(content)

# Test case for edge case with empty content
def test_split_content_from_model_empty_content(mock_streamresponse):
    content = ""
    
    expected_code = ""
    expected_tests = ""
    
    result = mock_streamresponse.split_content_from_model(content)
    
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected_code
    assert result[1] == expected_tests

# Test case for error condition with missing tests in code but present in content
def test_split_content_from_model_missing_tests_in_code(mock_streamresponse):
## ## ## ## ## ## ##     content = """Some text before the code block.