from __future__ import annotations

from typing import Literal, TypeAlias

import griffe.expressions as expr
from griffe.docstrings import dataclasses as ds
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
    ds.DocstringParameter
    | ds.DocstringAttribute
    | ds.DocstringReturn
    | ds.DocstringYield
    | ds.DocstringReceive
    | ds.DocstringRaise
    | ds.DocstringWarn
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

Annotation: TypeAlias = str | expr.Expr

DocType: TypeAlias = DocClass | DocFunction | DocAttribute | DocModule

DocMemberType: TypeAlias = MemberPage | Doc | Link

SummaryItem: TypeAlias = tuple[str, str]
