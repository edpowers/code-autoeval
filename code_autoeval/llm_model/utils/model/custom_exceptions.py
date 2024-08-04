"""Custom Exceptions."""

import re
from pprint import pprint
from typing import List


class FormattingError(Exception):
    pass


class NoTestsInPytestFile(Exception):
    pass


class MissingCoverageException(BaseException):
    pass


class CoverageParsingError(Exception):
    pass


class NoTestsFoundError(ValueError):
    """Raised when no tests are found in the content."""

    @classmethod
    def validate_tests_str(cls, content):
        if not re.search(r"# Test|pytest tests|def test_", content, re.IGNORECASE):
            pprint(content)
            raise cls("No tests provided in the model response.")


class UnresolvedImportError(ImportError):
    """Raise for unresolved import error."""

    @classmethod
    def validate_no_unresolved_imports(cls, remaining_undefined: List) -> None:
        if remaining_undefined:
            raise cls(f"Unresolved import errors for: {', '.join(remaining_undefined)}")

    def __init__(self, message: str):
        super().__init__(message)
