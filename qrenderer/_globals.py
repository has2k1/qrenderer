from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


EXCLUDE_PARAMETERS: dict[str, str | Sequence[str]] = {}
"""
Store object parameters to exclude from the documentation.

The specification is {object_path: parameter_name | parameter_names}.
"""

EXCLUDE_ATTRIBUTES: dict[str, str | Sequence[str]] = {}
"""
Store the attributes to exclude from the documentation.

The specification is {object_path: attribute_name | attribute_names}.
"""
