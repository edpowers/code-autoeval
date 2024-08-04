"""Parsing fixtures."""

# %%

from pprint import pprint

from multiuse.filepaths.find_classes_in_dir import FindClassesInDir
from multiuse.filepaths.find_project_root import FindProjectRoot
from multiuse.model import class_data_model
from multiuse.filepaths.system_utils import SystemUtils

from code_autoeval.llm_model.utils.extraction.fixture_parser import FixtureParser

# %%

project_root = FindProjectRoot.find_project_root()
fixture_relativive_str = "generated_code/fixtures/fixtures"
fixture_base_dir = project_root.joinpath(fixture_relativive_str)

all_fixture_files = fixture_base_dir.rglob("*.py")

fixture_parser = FixtureParser()

for f in all_fixture_files:
    fixtures = fixture_parser.parse_file(f)
    for fixture in fixtures:
        pprint(fixture)

    break

# %%


fixture_parser_dir = FixtureParser()
fixture_parser_dir.parse_directory(fixture_base_dir)

# %%


fixture_parser_dir.fixtures_by_class

# %%

fixture_parser_dir.get_fixtures_for_class("RunFlake8FixImports")

# %%

# Find the project root
project_root = FindProjectRoot.find_project_root()

directory = project_root.joinpath("code_autoeval")
class_info_list = FindClassesInDir.find_classes_in_dir(str(directory))
class_data_factory = class_data_model.ClassDataModelFactory(project_root)
class_data_models = class_data_factory.create_from_class_info(class_info_list)


# %%


class_data_models[-1]

# %%


fixture_flake8 = fixture_parser_dir.get_fixtures_for_class("RunFlake8FixImports")

test_module_path = fixture_flake8.fixtures[0].module_path

relative_test_module_path = test_module_path.relative_to(project_root)


SystemUtils.format_path_for_import(test_module_path.relative_to(project_root))

# %%
