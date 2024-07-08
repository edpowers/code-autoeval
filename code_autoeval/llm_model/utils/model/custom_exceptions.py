"""Custom Exceptions."""


class FormattingError(Exception):
    pass


class NoTestsInPytestFile(Exception):
    pass


class MissingCoverageException(BaseException):
    pass


class CoverageParsingError(Exception):
    pass
