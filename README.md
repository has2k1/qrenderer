# qrenderer

This is an experimental renderer for [quartodoc](https://github.com/machow/quartodoc).
It can only be installed from github and it will never be released on PyPi. Some version
of it may find its way into quartodoc. Use it with caution, there will be
breaking changes.

## Install

```console
$ pip install git+https://github.com/has2k1/qrenderer.git
```

## How to extend quartodoc with qrenderer

1. Import `QRenderer` which is the bridge between this renderer and
   quartodoc's current rendering system.

2. Import the decorator `extend_base_class` that make makes it
   possible to modify the classes that you extend.

3. Import any Render classes that you want to extend. The options are:

   - `RenderDoc` to extend the common parts to `classes`,
     `functions`, `attributes` and `modules`.

   - `RenderDocClass` to extend rendering of `classes`

   - `RenderDocFunction` to extend rendering of `functions`

   - `RenderDocAttribute` to extend rendering of `attributes`

   - `RenderDocModule` to extend rendering of `modules`

   - `RenderDocCallMixin` to extend rendering of the common parts
      of `functions` and class `methods` i.e. callables

   - `RenderDocMembersMixin` to extend rendering of the common parts
     of `modules` and `classes` i.e. objects with members

   - `RenderLayout` to extend rendering of the API / Reference page

   - `RenderSection` to extend rendering of a section/group of
     objects on Reference page.

   - `RenderPage `to extend rendering of page that contains the
      documentation of one or more objects. i.e. links from the
      Reference lead to this type of page.

4. When overriding the defaults, the common methods to extend are:

   - `render_title`
   - `render_signature`
   - `render_description`
   - `render_body`
   - `render_summary`

   Though for some types, it does not make sense to extend some of these
   methods. e.g. `modules` and `attributes` do not have signatures so
   extending the `render_signature` method would not have an effect.

5. Download qrenderer stylesheet(s) into your doc directory.
   [qrenderer.scss](https://raw.githubusercontent.com/has2k1/qrenderer/main/doc/qrenderer.scss)
   into your `doc` directory.

   ```bash
   cd doc
   python -m qrenderer.stylesheets.install .
   ```


## Example

Keeping the original signature of a class, we add a line of text below it.

**\_renderer.py**

```python
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

Then your minimal configuration file should have

**\_quarto.yml**

```yaml
project:
  type: website

format:
  html:
    toc: true
    theme:
      - lumen           # bootswatch theme
      - qrenderer.scss  # qrenderer's customisation
      - custom.scss     # your customisation (if any)

quartodoc:
  package: your_package
  renderer:
    style: _renderer.py
    typing_module_paths:
      - your_package.typing  # path to your type annotations
```

The easiest customisation you can make is to change the primary color of your documentation.

**custom.scss**

```scss
/*-- scss:defaults --*/
$primary: #9E2F68;

/*-- scss:mixins --*/

/*-- scss:rules --*/

/*-- scss:functions --*/

/*-- scss:uses --*/

```

Consult the [quarto](https://quarto.org/) documentation on [theming](https://quarto.org/docs/output-formats/html-themes.html) for [more](https://quarto.org/docs/output-formats/html-themes-more.html)
