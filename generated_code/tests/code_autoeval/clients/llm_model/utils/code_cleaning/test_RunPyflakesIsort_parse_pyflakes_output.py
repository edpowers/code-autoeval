# Updated Implementation of RunPyflakesIsort.parse_pyflakes_output function.
class RunPyflakesIsort:
    def __init__(self, data):
        self.data = data

    def parse_pyflakes_output(self, output: str) -> list:
        unused_imports = []

        for line in output.splitlines():
            if "imported but unused" in line:
                parts = line.split("'")
                if len(parts) >= 2:
                    unused_imports.append(parts[1])
        
        return unused_imports

from unittest.mock import patch

# Updated pytest tests to achieve 100% code coverage.
import pytest


class RunPyflakesIsort:
    def __init__(self, data):
        self.data = data

    def parse_pyflakes_output(self, output: str) -> list:
        unused_imports = []

        for line in output.splitlines():
            if "imported but unused" in line:
                parts = line.split("'")
                if len(parts) >= 2:
                    unused_imports.append(parts[1])
        
        return unused_imports

##################################################
# TESTS
##################################################

def test_parse_pyflakes_output_normal():
    # Arrange
    output = "Some line with imported but unused 'module1'\nAnother line with nothing special"
    expected_result = ['module1']
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result

def test_parse_pyflakes_output_no_unused():
    # Arrange
    output = "All lines are used"
    expected_result = []
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result

def test_parse_pyflakes_output_multiple_unused():
    # Arrange
    output = "imported but unused 'module1'\nimported but unused 'module2'"
    expected_result = ['module1', 'module2']
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result

def test_parse_pyflakes_output_empty():
    # Arrange
    output = ""
    expected_result = []
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result

def test_parse_pyflakes_output_no_quotes():
    # Arrange
    output = "imported but unused module1"
    expected_result = []
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result

def test_parse_pyflakes_output_no_match():
    # Arrange
    output = "This line does not match the pattern"
    expected_result = []
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result

def test_parse_pyflakes_output_whitespace():
    # Arrange
    output = "   \n  imported but unused 'module1'  \n"
    expected_result = ['module1']
    
    run_pyflakes_isort = RunPyflakesIsort(None)
    
    # Act
    result = run_pyflakes_isort.parse_pyflakes_output(output)
    
    # Assert
    assert result == expected_result