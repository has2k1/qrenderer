from __future__ import annotations

from typing import Literal, TypeAlias

import griffe as gf
from quartodoc.layout import (
    Doc,
    DocAttribute,
    DocClass,
    DocFunction,
    DocModule,
    Layout,
    Link,
    MemberPage,
    Page,
    Section,
)
from quartodoc.pandoc.blocks import InlineContent

from qrenderer import (
    RenderDoc,
    RenderDocAttribute,
    RenderDocClass,
    RenderDocFunction,
    RenderDocModule,
    RenderLayout,
    RenderPage,
    RenderSection,
)

DisplayNameFormat: TypeAlias = Literal[
    "full", "name", "short", "relative", "canonical"
]
DocObjectKind: TypeAlias = Literal[
    "module",
    "class",
    "method",
    "function",
    "attribute",
    "alias",
    "type",
    "typevar",
]

DocstringDefinitionType: TypeAlias = (
    gf.DocstringParameter
    | gf.DocstringAttribute
    | gf.DocstringReturn
    | gf.DocstringYield
    | gf.DocstringReceive
    | gf.DocstringRaise
    | gf.DocstringWarn
)

Documentable: TypeAlias = (
    # _Docable, Doc
    DocClass
    | DocFunction
    | DocAttribute
    | DocModule
    # _Docable
    | Link
    # Structual
    | Page
    | Section
    | Layout
)

RenderObjType: TypeAlias = (
    RenderDoc
    | RenderDocClass
    | RenderDocFunction
    | RenderDocAttribute
    | RenderDocModule
    | RenderLayout
    | RenderPage
    | RenderSection
)

Annotation: TypeAlias = str | gf.Expr

DocType: TypeAlias = DocClass | DocFunction | DocAttribute | DocModule

DocMemberType: TypeAlias = MemberPage | Doc | Link

SummaryItem: TypeAlias = tuple[InlineContent, InlineContent]
