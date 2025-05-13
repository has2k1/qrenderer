from __future__ import annotations

from typing import TYPE_CHECKING, cast

from quartodoc.pandoc.blocks import (
    Div,
    Header,
)
from quartodoc.pandoc.components import Attr
from tabulate import tabulate

from .base import RenderBase

if TYPE_CHECKING:
    from quartodoc.layout import Section

    from qrenderer.typing import RenderObjType


class __RenderSection(RenderBase):
    """
    Render a Section object (layout.Section)

    This is a section of the index/reference page
    """

    def __post_init__(self):
        self.section = cast("Section", self.layout_obj)
        """Section of the reference page"""

    def render_title(self):
        section = self.section
        if section.title:
            return Header(
                self.level + 1,
                f"{section.title}",
                Attr(classes=["doc-summary"]),
            )
        elif section.subtitle:
            return Header(
                self.level + 2,
                f"{section.subtitle}",
                Attr(classes=["doc-summary-subgroup"]),
            )

    def render_description(self):
        return self.section.desc

    def render_body(self):
        if not self.section.contents:
            return

        from . import get_render_type

        render_objs: list[RenderObjType] = [
            get_render_type(c)(c, self.renderer)  # type: ignore
            for c in self.section.contents
        ]
        rows = [row for r in render_objs for row in r.render_summary()]
        return Div(
            str(tabulate(rows, tablefmt="grid")),
            Attr(classes=["doc-summary-table"]),
        )


class RenderSection(__RenderSection):
    """
    Extend Rendering of a layout.Section object
    """
