from __future__ import annotations

from typing import TYPE_CHECKING, overload

from quartodoc.layout import (
    DocAttribute,
    DocClass,
    DocFunction,
    DocModule,
    Layout,
    Page,
    Section,
)

from .docattribute import RenderDocAttribute
from .docclass import RenderDocClass
from .docfunction import RenderDocFunction
from .docmodule import RenderDocModule
from .layout import RenderLayout
from .page import RenderPage
from .section import RenderSection

if TYPE_CHECKING:
    from typing import Type

    from qrenderer.typing import Documentable, RenderObjType


_class_mapping: dict[Type[Documentable], Type[RenderObjType]] = {
    DocAttribute: RenderDocAttribute,
    DocClass: RenderDocClass,
    DocFunction: RenderDocFunction,
    DocModule: RenderDocModule,
    Layout: RenderLayout,
    Page: RenderPage,
    Section: RenderSection,
}


@overload
def get_render_type(obj: DocClass) -> Type[RenderDocClass]:
    ...


@overload
def get_render_type(obj: DocFunction) -> Type[RenderDocFunction]:
    ...


@overload
def get_render_type(obj: DocAttribute) -> Type[RenderDocAttribute]:
    ...


@overload
def get_render_type(obj: DocModule) -> Type[RenderDocModule]:
    ...


@overload
def get_render_type(obj: Layout) -> Type[RenderLayout]:
    ...


@overload
def get_render_type(obj: Page) -> Type[RenderPage]:
    ...


@overload
def get_render_type(obj: Section) -> Type[RenderSection]:
    ...


def get_render_type(obj: Documentable) -> Type[RenderObjType]:
    if type(obj) in _class_mapping:
        return _class_mapping[type(obj)]
    else:
        msg = f"Cannot document object of type {type(obj)}"
        raise ValueError(msg)
