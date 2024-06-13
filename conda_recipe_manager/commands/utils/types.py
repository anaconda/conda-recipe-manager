"""
File:           types.py
Description:    Contains types and constants used by CLI commands.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Final

# Pre-CEP-13 name of the recipe file
V0_FORMAT_RECIPE_FILE_NAME: Final[str] = "meta.yaml"
# Required file name for the recipe, specified in CEP-13
V1_FORMAT_RECIPE_FILE_NAME: Final[str] = "recipe.yaml"


class ExitCode(IntEnum):
    """
    Error codes to return upon script completion.

    All commands define their error codes here, so that they can interop with unique codes for errors without overlap.
    """

    ## All Scripts ##
    SUCCESS = 0
    CLICK_ERROR = 1  # Controlled by the `click` library
    CLICK_USAGE = 2  # Controlled by the `click` library
    NO_FILES_FOUND = 3
    # In bulk operation mode, this indicates that the % success threshold was not met
    MISSED_SUCCESS_THRESHOLD = 42
    TIMEOUT = 43

    ## convert  ##
    # Errors are roughly ordered by increasing severity
    RENDER_WARNINGS = 100
    RENDER_ERRORS = 101
    PARSE_EXCEPTION = 102
    RENDER_EXCEPTION = 103
    READ_EXCEPTION = 104
    PRE_PROCESS_EXCEPTION = 105

    ## rattler-bulk-build ##
    # NOTE: There may be overlap with rattler-build

    ## update-feedstock ##
