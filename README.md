# qrenderer

This is an experimental renderer for [quartodoc](https://github.com/machow/quartodoc).
It can only be installed from github and it will never be released on PyPi. Use it with caution, there will be breaking changes.

## Install

```console
$ pip install git+https://github.com/has2k1/qrenderer.git
```


## How to extend quartodoc

1. Import `QRenderer` which is the bridge between this renderer and
   quartodoc's current rendering system.

2. Import a decorator `extend_base_class` that will mark the classes
   created to extend quartodoc.

3. Import any Render classes that you want to extend. The options are:

   - `RenderDoc` - Base class for the renderers of python `classes`, `functions`,
     `attributes` and `modules`.
   - `RenderDocClass` - class that renderers python `classes`
   - `RenderDocFunction` - class that renderers python `functions`
   - `RenderDocAttribute` - class that renderers python `attributes`
   - `RenderDocModule` - class that renderers python `modules`
   - `RenderDocCallMixin` - mixin class for types that are callable. That is
     `functions` and class `methods`.
   - `RenderDocMembersMixin` - mixin class for types that contain other types.
     That is, `modules` and `classes`.
   - `RenderLayout` - class that renders the API / Reference page
   - `RenderPage` - class that renders a documentation page. The contents of the
     page will include one or more `classes`, `functions`, `attributes` and
     `modules`.
   - `RenderSection` - class that renders a section/group on the API / Reference
     page.

   Extending the base class (`RenderDoc`) or the mixing classes
   (`RenderDocCallMixin`, `RenderDocMembersMixin`) affects the render classes
   that derive from them.

   The common methods to override when extending are `render_title`, `render_signature`,
   `render_description`, `render_body` and `render_summary`. For some types, it does not make sense
   to extend some of these method, e.g. `modules` and `attributes` do not have signatures
   so for them to extend the `render_signature` method would not have an effect.

## Example

Keeping the original signature of a class, we add a line of text below it.

```
from quartodoc.pandoc.blocks import Blocks
from qrenderer import QRenderer, extend_base_class, RenderDocClass

class Renderer(QRenderer):
    pass

@extend_base_class
class _RenderDocClass(RenderDocClass):

    def render_signature(self):
        sig = super().render_signature()
        return Blocks([sig, "Line below the class signature"])
```
