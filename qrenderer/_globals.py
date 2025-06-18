from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


EXCLUDE_PARAMETERS: dict[str, str | Sequence[str]] = {}
"""
The parameters of callables to exclude from the documentation.

The specification is {callable_object_path: parameter_name | parameter_names}.
"""

EXCLUDE_ATTRIBUTES: dict[str, str | Sequence[str]] = {}
"""
The attributes to exclude from the documentation.

The specification is {parent_object_path: attribute_name | attribute_names}.
"""
