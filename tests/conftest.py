import griffe.dataclasses as dc
import quartodoc.layout as layout
from griffe.tests import temporary_visited_package

from qrenderer import (
    QRenderer,
    RenderDocAttribute,
    RenderDocClass,
    RenderDocFunction,
    RenderDocModule,
)


def render(code: str, name: str | None = None) -> str:
    """
    Render named variable in code

    If name is None, return code rendered as a module
    """
    def toDocObject(obj: dc.Object):
        members = [
            toDocObject(m) for m in obj.members.values()
            # imported variables are of type dc.Alias and we are
            # not interested in dealing with them.
            if not isinstance(m, dc.Alias)
        ]
        return layout.Doc.from_griffe(obj.name, obj, members=members)

    with temporary_visited_package("package", {"__init__.py": code}) as m:
        obj = m[name] if name else m

    match layout_obj := toDocObject(obj):
        case layout.DocAttribute():
            _Render = RenderDocAttribute
        case layout.DocClass():
            _Render = RenderDocClass
        case layout.DocFunction():
            _Render = RenderDocFunction
        case layout.DocModule():
            _Render = RenderDocModule

    robj = _Render(layout_obj, QRenderer())
    return str(robj)
