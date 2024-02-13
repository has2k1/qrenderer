from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

from quartodoc.pandoc.blocks import (
    BlockContent,
    Blocks,
    DefinitionItem,
    DefinitionList,
    Div,
    Header,
)
from quartodoc.pandoc.components import Attr
from quartodoc.pandoc.inlines import Code

from .._format import pretty_code, render_dataclass_parameter_declaration
from .doc import RenderDoc
from .mixin_call import RenderDocCallMixin
from .mixin_members import RenderDocMembersMixin

if TYPE_CHECKING:
    from griffe import dataclasses as dc
    from quartodoc import layout


@dataclass
class __RenderDocClass(RenderDocMembersMixin, RenderDocCallMixin, RenderDoc):
    """
    Render documentation for a class (layout.DocClass)
    """

    def __post_init__(self):
        super().__post_init__()
        # We narrow the type with a TypeAlias since we do not expect
        # any subclasses to have narrower types
        self.doc: layout.DocClass = self.doc
        self.obj: dc.Class = self.obj

    @cached_property
    def is_dataclass(self):
        """
        Return True if the class object is a dataclass
        """
        return "dataclass" in self.obj.labels

    @cached_property
    def _attribute_members(self) -> list[layout.DocAttribute]:
        """
        Override to exclude dataclass parameters
        """
        attributes = super()._attribute_members
        if self.is_dataclass:
            params = {p.name for p in self.function_parameters}
            attributes = [a for a in attributes if a.name not in params]
        return attributes

    def render_body(self) -> BlockContent:
        sections, kinds = self._sections

        if (
            not self.is_dataclass
            or "parameters" in set(kinds)
            or not len(self.function_parameters)
        ):
            return Blocks([sections, *self.render_members()])

        # FIXME: This is a mixture of RenderDoc.render_body and
        # RenderDocCallMixin.render_section
        header = Header(
            self.level + 1,
            "Parameter Attributes",
            Attr(classes=["doc-parameter-attributes"]),
        )

        items: list[DefinitionItem] = []
        for p in self.function_parameters:
            a = self.obj.attributes[p.name]
            stmt = render_dataclass_parameter_declaration(p, a)
            desc = (a.docstring and a.docstring.value) or ""
            items.append((Code(pretty_code(stmt)).html, desc))

        body = Div(
            DefinitionList(items),
            Attr(classes=["doc-definition-items"]),
        )

        content = Blocks([header, body])
        idx = 1 if kinds and kinds[0] == "text" else 0
        sections.insert(idx, content)
        return Blocks([sections, *self.render_members()])

    # NOTE: This method override is a temporary fix to
    # https://github.com/mkdocstrings/griffe/issues/233
    @cached_property
    def function_parameters(self):
        """
        Override mixin method to exclude non-parameters
        """
        from griffe import dataclasses as dc

        from .._utils import is_field_init_false

        parameters = super().function_parameters

        if self.is_dataclass:
            parameters = dc.Parameters(
                *[
                    p
                    for p in parameters
                    if (not is_field_init_false(p) and p.annotation)
                ]
            )

        return parameters


@dataclass
class RenderDocClass(__RenderDocClass):
    """
    Extend Rendering of a layout.DocClass object
    """
