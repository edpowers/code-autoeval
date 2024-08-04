"""Remove the invalid imports."""

import re
import subprocess


class RemoveInvalidImports:

    @classmethod
    def remove_invalid_imports(cls, file_path: str) -> bool:
        """
        Run mypy to find import-not-found errors and remove those lines.
        Returns True if changes were made, False otherwise.
        """
        # Run mypy to find import-not-found errors
        mypy_result: str = cls.run_mypy_on_file(file_path)

        changes_made = False
        lines_to_remove = []

        # Parse the mypy output to find lines with import-not-found errors
        for line in mypy_result.splitlines():
            if "[import-not-found]" in line:
                if match := re.search(rf"{re.escape(file_path)}:(\d+):", line):
                    lines_to_remove.append(int(match[1]))

        if lines_to_remove:
            # Read the file
            with open(file_path, "r") as file:
                lines = file.readlines()

            # Remove the lines with import-not-found errors
            for line_num in sorted(lines_to_remove, reverse=True):
                if line_num <= len(lines):
                    print(f"Removing line {line_num} with import-not-found error")
                    del lines[line_num - 1]
                    changes_made = True

            # Write the modified content back to the file
            with open(file_path, "w") as file:
                file.writelines(lines)

        return changes_made

    @staticmethod
    def run_mypy_on_file(file_path: str) -> str:
        """Run mypy on the specified file and return the output."""
        result = subprocess.run(
            ["mypy", file_path],
            capture_output=True,
            text=True,
        )
        return result.stdout
