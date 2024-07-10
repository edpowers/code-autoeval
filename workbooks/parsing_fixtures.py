"""Parsing fixtures."""

# %%


from pprint import pprint

from multiuse.filepaths.find_project_root import FindProjectRoot

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
