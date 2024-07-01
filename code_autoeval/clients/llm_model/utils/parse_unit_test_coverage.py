"""Parse the unit test coverage."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from code_autoeval.clients.llm_model.utils.logging_statements.logging_statements import (
    LoggingStatements,
)


class ParseUnitTestCoverage(LoggingStatements):

    @classmethod
    def run_parse_unit_test_cov(
        cls,
        coverage_output: str,
        project_root: Path,
        relative_path: str,
        func_name: str,
    ) -> Tuple[Dict[Tuple[int, int], str], float]:
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

        recalculated_coverage = instance._recalculate_coverage(
            missing_ranges, uncovered_lines
        )

        print(f"Recalculated coverage: {recalculated_coverage:.2f}%")

        return uncovered_lines, recalculated_coverage

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

                    # Extract file path
                    file_path_match = re.search(r"(/[^\s]+\.py)", file_info)
                    if file_path_match:
                        file_path = file_path_match.group(1)

                        # The missing ranges are already in the correct format
                        return file_path, missing_ranges

        raise Exception("Failed to parse coverage output.")

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

        if start_line and end_line:
            return (start_line, end_line)
        return None

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
        concerned_set = set(
            range for ranges in concerned_lines.keys() for range in ranges
        )

        # Find the intersection of all_lines and concerned_lines
        covered_lines = all_lines.intersection(concerned_set)

        # Calculate coverage
        if not concerned_set:
            return 100.0  # If there are no lines to be concerned about, consider it 100% covered

        coverage_percentage = (len(covered_lines) / len(concerned_set)) * 100

        return coverage_percentage
