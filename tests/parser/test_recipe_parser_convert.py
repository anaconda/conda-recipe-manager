"""
File:           test_recipe_parser_convert.py
Description:    Unit tests for the RecipeParserConvert class
"""

from __future__ import annotations

import pytest

from conda_recipe_manager.parser.recipe_parser_convert import RecipeParserConvert
from conda_recipe_manager.parser.types import MessageCategory
from tests.file_loading import TEST_FILES_PATH, load_file, load_recipe_convert


@pytest.mark.parametrize(
    "input_file,expected_file",
    [
        ("simple-recipe_environ.yaml", "pre-processed-simple-recipe_environ.yaml"),
        ("simple-recipe.yaml", "simple-recipe.yaml"),  # Unchanged file
    ],
)
def test_pre_process_recipe_text(input_file: str, expected_file: str) -> None:
    """
    Validates the pre-processor phase of the conversion process. A recipe file should come in
    as a string and return a modified string, if applicable.
    :param input_file: Test input recipe file name
    :param expected_file: Name of the file containing the expected output of a test instance
    """
    assert RecipeParserConvert.pre_process_recipe_text(load_file(f"{TEST_FILES_PATH}/{input_file}")) == load_file(
        f"{TEST_FILES_PATH}/{expected_file}"
    )


@pytest.mark.parametrize(
    "file_base,errors,warnings",
    [
        (
            "simple-recipe.yaml",
            [],
            [
                "A non-list item had a selector at: /package/name",
                "A non-list item had a selector at: /requirements/empty_field2",
            ],
        ),
        (
            "multi-output.yaml",
            [],
            [],
        ),
        (
            "huggingface_hub.yaml",
            [],
            [],
        ),
        (
            "types-toml.yaml",
            [],
            [],
        ),
        # Regression test: Contains a `test` section that caused an empty dictionary to be inserted in the conversion
        # process, causing an index-out-of-range exception.
        (
            "pytest-pep8.yaml",
            [],
            [],
        ),
        # Regression test: Contains selectors and test section data that caused previous conversion issues.
        (
            "google-cloud-cpp.yaml",
            [],
            [
                "A non-list item had a selector at: /outputs/0/script",
                "A non-list item had a selector at: /outputs/1/script",
                "A non-list item had a selector at: /outputs/0/script",
                "A non-list item had a selector at: /outputs/1/script",
            ],
        ),
        # Tests for transformations related to the new `build/dynamic_linking` section
        (
            "dynamic-linking.yaml",
            [],
            [],
        ),
        # Regression: Tests for proper indentation of a list item inside a collection node element
        (
            "boto.yaml",
            [],
            [],
        ),
        # Regression: Tests a recipe that has multiple `source`` objects in `/source` AND an `about` per `output`
        # TODO Issue #50 tracks an edge case caused by this project that is not currently handled.
        (
            "cctools-ld64.yaml",
            [],
            [],
        ),
        # TODO complete: The `rust.yaml` test contains many edge cases and selectors that aren't directly supported in
        # the V1 recipe format
        # (
        #    "rust.yaml",
        #    [],
        #    [],
        # ),
        # TODO Complete: The `curl.yaml` test is far from perfect. It is very much a work in progress.
        # (
        #    "curl.yaml",
        #    [],
        #    [
        #        "A non-list item had a selector at: /outputs/0/build/ignore_run_exports",
        #    ],
        # ),
    ],
)
def test_render_to_v1_recipe_format(file_base: str, errors: list[str], warnings: list[str]) -> None:
    """
    Validates rendering a recipe in the V1 format.
    :param file_base: Base file name for both the input and the expected out
    """
    parser = load_recipe_convert(file_base)
    result, tbl, _ = parser.render_to_v1_recipe_format()
    assert result == load_file(f"{TEST_FILES_PATH}/v1_format/v1_{file_base}")
    assert tbl.get_messages(MessageCategory.ERROR) == errors
    assert tbl.get_messages(MessageCategory.WARNING) == warnings
    # Ensure that the original file was untouched
    assert not parser.is_modified()
    assert parser.diff() == ""
