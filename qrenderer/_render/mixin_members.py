from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, cast

from griffe import dataclasses as dc
from quartodoc import layout
from quartodoc.pandoc.blocks import (
    Block,
    BlockContent,
    Blocks,
    Header,
)
from quartodoc.pandoc.components import Attr
from tabulate import tabulate

from .._utils import isDoc
from .doc import RenderDoc

if TYPE_CHECKING:
    from typing import Literal


@dataclass
class RenderedMembersGroup(Block):
    title: Header | None = None
    summary: str | None = None
    members_body: Block | None = None

    def __str__(self):
        return str(Blocks([self.title, self.summary, self.members_body]))


@dataclass
class __RenderDocMembersMixin(RenderDoc):
    """
    Mixin to render Doc objects that have members

    i.e. modules and classes
    """

    show_members: bool = field(init=False, default=True)
    """All members (attributes, classes and functions) """
    show_attributes: bool = field(init=False, default=True)
    show_classes: bool = field(init=False, default=True)
    show_functions: bool = field(init=False, default=True)

    show_members_summary: bool = field(init=False, default=True)
    """All member (attribute, class and function) summaries"""
    show_attributes_summary: bool = field(init=False, default=True)
    show_classes_summary: bool = field(init=False, default=True)
    show_functions_summary: bool = field(init=False, default=True)

    show_members_body: bool = field(init=False, default=True)
    """All member (attribute, class and function) bodies"""
    show_attributes_body: bool = field(init=False, default=True)
    show_classes_body: bool = field(init=False, default=True)
    show_functions_body: bool = field(init=False, default=True)

    def __post_init__(self):
        super().__post_init__()
        self.doc = cast(layout.DocClass | layout.DocModule, self.doc)  # pyright: ignore[reportUnnecessaryCast]
        self.obj = cast(dc.Class | dc.Module, self.obj)  # pyright: ignore[reportUnnecessaryCast]

    def render_body(self) -> BlockContent:
        """
        Render the docstring and member docs
        """
        docstring = super().render_body()
        return Blocks([docstring, *self.render_members()])

    def render_members(self) -> list[RenderedMembersGroup | None]:
        """
        Render the docs of member objects

        The member objects are attributes, classes and functions/methods
        """
        if not self.show_members:
            return []
        return [
            self.render_attributes(),
            self.render_classes(),
            self.render_functions(),
        ]

    @cached_property
    def _attribute_members(self) -> list[layout.DocAttribute]:
        return [x for x in self.doc.members if isDoc.Attribute(x)]

    @cached_property
    def _class_members(self) -> list[layout.DocClass]:
        return [x for x in self.doc.members if isDoc.Class(x)]

    @cached_property
    def _function_members(self) -> list[layout.DocFunction]:
        return [x for x in self.doc.members if isDoc.Function(x)]

    def render_classes(self) -> RenderedMembersGroup | None:
        """
        Render the class members of the Doc
        """
        return (
            self._render_members_group("classes")
            if self.show_classes
            else None
        )

    def render_functions(self) -> RenderedMembersGroup | None:
        """
        Render the function members of the Doc
        """
        return (
            self._render_members_group("functions")
            if self.show_functions
            else None
        )

    def render_attributes(self) -> RenderedMembersGroup | None:
        """
        Render the function members of the Doc
        """
        return (
            self._render_members_group("attributes")
            if self.show_attributes
            else None
        )

    def _render_members_group(
        self,
        group: Literal["classes", "functions", "attributes"],
    ) -> RenderedMembersGroup | None:
        """
        Render all of class, function or attribute members

        Parameters
        ----------
        docables
            List of layout.Doc subclasses. One for each member.

        member_group
            An identifier for the type of the members.
        """
        from . import RenderDocAttribute, RenderDocClass, RenderDocFunction

        if group == "classes":
            docables, Render = self._class_members, RenderDocClass
        elif group == "attributes":
            docables, Render = self._attribute_members, RenderDocAttribute
        else:
            docables, Render = self._function_members, RenderDocFunction

        if not docables:
            return None

        show_summary: bool = getattr(self, f"show_{group}_summary")
        show_body: bool = getattr(self, f"show_{group}_body")
        slug = (
            "methods"
            if group == "functions" and isinstance(self.doc, layout.DocClass)
            else group
        )

        title = Header(
            self.level + 1,
            group.title(),
            Attr(classes=[f"doc-{slug}"]),
        )

        render_objs = [
            Render(obj, self.renderer, self.level + 2).clear_page_path()
            for obj in docables
        ]

        if self.show_members_summary and show_summary:
            rows = [row for r in render_objs for row in r.render_summary()]
            summary = tabulate(rows, ("Name", "Description"), "grid")
        else:
            summary = None

        body = Blocks(render_objs) if show_body else None
        return RenderedMembersGroup(title, summary, body)


@dataclass
class RenderDocMembersMixin(__RenderDocMembersMixin, RenderDoc):
    """
    Extend Rendering of objects that have members
    """
