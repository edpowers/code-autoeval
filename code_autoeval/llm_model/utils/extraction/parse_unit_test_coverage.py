"""Parse the unit test coverage."""

import re
from pathlib import Path
from pprint import pprint
from typing import Any, Dict, List, Optional, Tuple

from IPython.display import display

from code_autoeval.llm_model.utils import model
from code_autoeval.llm_model.utils.log_funcs import logging_funcs


class ParseUnitTestCoverage(logging_funcs.LoggingFuncs):
    """
    Example
    -------
    coverage_output = '''
    Name                                Stmts   Miss  Cover
    -------------------------------------------------------
    code_autoeval/llm_model/utils/extraction/parse_unit_test_coverage.py      53     53     0%
    -------------------------------------------------------
    TOTAL                                 53     53     0%
    '''
    project_root = Path("/path/to/project")
    relative_path = "code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage"
    func_name = "ParseUnitTestCoverage"
    summary = ParseUnitTestCoverage.run_parse_unit_test_cov(
        coverage_output, project_root, relative_path, func_name
    )

    >>> summary.uncovered_lines

    # For use as a staticmethod:
    >>> ParseUnitTestCoverage.get_coverage_report(func_name, coverage_output)
    """

    @staticmethod
    def wrap_run_parse_unit_test_cov(
        coverage_output: str,
        project_root: Path,
        relative_path: str,
        func_name: str,
        tests_failed: bool = False,
    ) -> model.UnitTestSummary:
        try:
            return ParseUnitTestCoverage.run_parse_unit_test_cov(
                coverage_output,
                project_root,
                relative_path,
                func_name,
                tests_failed,
            )
        except (ImportError, SyntaxError) as oe:
            raise model.FormattingError(
                "Error in importation, formatting, indentation etc.."
            ) from oe
        except model.CoverageParsingError as e:
            print(f"Error parsing coverage: {e}")
            # If "no tests ran" then throw an error, else return False
            if "no tests ran" in coverage_output:
                raise model.FormattingError(
                    "Error in importation, formatting, indentation etc.."
                ) from e

            raise Exception(
                "Tests failed or coverage is not 100% - raising exception"
            ) from e

    @classmethod
    def run_parse_unit_test_cov(
        cls,
        coverage_output: str,
        project_root: Path,
        relative_path: str,
        func_name: str,
        tests_failed: bool = False,
    ) -> model.UnitTestSummary:
        instance = cls()
        parse_result = instance._parse_coverage_output(coverage_output)
        if not parse_result:
            raise Exception("Failed to parse coverage output.")

        _, missing_ranges = parse_result
        file_path = project_root.joinpath(relative_path.replace(".", "/")).with_suffix(
            ".py"
        )

        parsed_ranges = instance._parse_missing_ranges(missing_ranges)
        instance._log_code(f"{missing_ranges}", "Missing ranges: ")
        uncovered_lines = instance._find_uncovered_lines(
            str(file_path),
            parsed_ranges,
            function_name=func_name,
        )

        for range_nums, content in uncovered_lines.items():
            print(f"Uncovered lines {range_nums}:")
            print(content)
            print("---")

        return model.UnitTestSummary(
            uncovered_lines=uncovered_lines,
            recalculated_coverage=instance._recalculate_coverage(
                missing_ranges, uncovered_lines
            ),
            extracted_coverage=instance._parse_coverage_v1(
                coverage_output, str(file_path)
            ),
            tests_failed=tests_failed,
        )

    def _parse_coverage_v1(self, output: str, target_file: str) -> float:
        coverage_data = {}

        # Remove ANSI escape codes
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        clean_output = ansi_escape.sub("", output)

        for line in clean_output.split("\n"):

            if "TOTAL" in line:
                parts = line.split()
                # Find the part that contains the coverage percentage
                for part in parts:
                    if part.endswith("%"):
                        try:
                            coverage_percentage = int(part.rstrip("%"))
                            coverage_data[target_file] = coverage_percentage
                        except ValueError as ve:
                            print(
                                f"Error parsing coverage percentage for {target_file}: {ve}"
                            )
                            print(f"Line content: {line}")
                        break

        if not coverage_data:
            display(pprint(output))  # type: ignore
            raise model.CoverageParsingError(
                "Coverage information not found in the output."
            )

        if target_file not in coverage_data:
            raise model.CoverageParsingError(
                f"Coverage for {target_file} not found in the output."
            )

        # Find the only key in the coverage data.
        coverage_data_key = list(coverage_data.keys())[0]
        return coverage_data[coverage_data_key]

    def _parse_coverage_output(self, coverage_output: str) -> Optional[Tuple[str, str]]:
        """
        Parse the coverage output to extract file path and missing ranges.
        This method splits the output line by line and looks for the percentage and missing ranges.
        """
        lines = coverage_output.split("\n")
        for line in lines:
            if ".py" in line and "%" in line:
                # Split the line at the percentage
                parts = re.split(r"\s+(\d+%)\s+", line)
                if len(parts) >= 3:
                    file_info = parts[0].strip()
                    missing_ranges = parts[-1].strip()

                    if file_path_match := re.search(r"(/[^\s]+\.py)", file_info):
                        file_path = file_path_match[1]

                        # The missing ranges are already in the correct format
                        return file_path, missing_ranges

        raise model.CoverageParsingError(
            "Failed to parse coverage output - likely due to error running tests."
        )

    def _find_function_bounds(
        self, file_path: str, function_name: str
    ) -> Optional[Tuple[int, int]]:
        with open(file_path, "r") as file:
            lines = file.readlines()

        start_line = None
        end_line = None
        in_function = False
        indent_level = 0

        for i, line in enumerate(lines, 1):
            if re.match(rf"\s*def\s+{re.escape(function_name)}\s*\(", line):
                start_line = i
                in_function = True
                indent_level = len(line) - len(line.lstrip())
            elif in_function:
                if line.strip() and len(line) - len(line.lstrip()) <= indent_level:
                    end_line = i - 1
                    break

        return (start_line, end_line) if start_line and end_line else None

    def _parse_missing_ranges(self, missing_ranges: str) -> List[Tuple[int, int]]:
        """
        Parse the missing ranges string into a list of tuples.

        Args:
        missing_ranges (str): String containing missing line numbers and ranges.

        Returns:
        List[Tuple[int, int]]: List of tuples representing single lines or ranges.
        """
        parsed_ranges = []
        for range_str in missing_ranges.split(", "):
            if "-" in range_str:
                start, end = map(int, range_str.split("-"))
                parsed_ranges.append((start, end))
            else:
                line_num = int(range_str)
                parsed_ranges.append((line_num, line_num))
        return parsed_ranges

    def _find_uncovered_lines(
        self,
        file_path: str,
        parsed_ranges: List[Tuple[int, int]],
        function_name: Optional[str] = None,
    ) -> Dict[Tuple[int, int], str]:
        uncovered_lines = {}

        with open(file_path, "r") as file:
            lines = file.readlines()

        function_bounds = None
        if function_name:
            function_bounds = self._find_function_bounds(file_path, function_name)

        for start, end in parsed_ranges:
            if function_bounds:
                # Only consider ranges that overlap with the function
                if end < function_bounds[0] or start > function_bounds[1]:
                    continue
                # Adjust the range to be within the function
                start = max(start, function_bounds[0])
                end = min(end, function_bounds[1])

            content = "".join(lines[start - 1 : end])
            uncovered_lines[(start, end)] = content.strip()

        # Verify that we found content for each range
        if len(uncovered_lines) != len(parsed_ranges):
            missing_ranges = set(parsed_ranges) - set(uncovered_lines.keys())
            print(f"Warning: Could not find content for ranges: {missing_ranges}")

        return uncovered_lines

    def _recalculate_coverage(
        self, range_string: str, concerned_lines: Dict[Tuple[int, int], str]
    ) -> float:
        def parse_range(s):
            result = []
            for part in s.split(","):
                if "-" in part:
                    a, b = map(int, part.split("-"))
                    result.extend(range(a, b + 1))
                else:
                    a = int(part)
                    result.append(a)
            return set(result)

        # Parse the range string
        all_lines = parse_range(range_string)

        # Convert concerned_lines to a set of line numbers
        concerned_set = {range for ranges in concerned_lines for range in ranges}

        # Find the intersection of all_lines and concerned_lines
        covered_lines = all_lines.intersection(concerned_set)

        # Calculate coverage
        if not concerned_set:
            return 100.0  # If there are no lines to be concerned about, consider it 100% covered

        coverage_percentage = (len(covered_lines) / len(concerned_set)) * 100

        return coverage_percentage

    def get_coverage_report(
        self,
        function_name: str,
        coverage_result: Any,
        error_message: Optional[str] = "",
    ) -> Dict[str, Any]:
        """Get the coverage report for the executed tests."""
        if error_message and "coverage is not 100%" not in error_message:
            return {
                "total_coverage": 0,
                "uncovered_lines": "None",
                "test_summary": "No test summary available.",
                "full_output": coverage_result.stdout,
            }

        # Initialize default values
        total_coverage = 0
        uncovered_lines = "None"

        # Parse the coverage report
        coverage_output = coverage_result.stdout

        # Find the line containing coverage information for our function
        coverage_pattern = rf"{function_name}\.py\s+\d+\s+\d+\s+(\d+)%\s+([\d,-]+)?"
        if match := re.search(coverage_pattern, coverage_output):
            total_coverage = int(match[1])
            uncovered_lines = match[2] or "None"

        # Extract test results summary
        test_summary = re.search(
            r"(=+ .*? =+)$", coverage_output, re.MULTILINE | re.DOTALL
        )
        test_summary = test_summary[1] if test_summary else "No test summary available."

        return {
            "total_coverage": total_coverage,
            "uncovered_lines": uncovered_lines,
            "test_summary": test_summary,
            "full_output": coverage_output,
        }
