from qrenderer.tools import render_code_variable


def test_dataclass_with_keyword_only_signature():
    code = """
    from dataclasses import KW_ONLY, dataclass
    from typing import ClassVar

    @dataclass
    class Point:
        x: float
        _: KW_ONLY
        y: float
        z: float
    """
    qmd = render_code_variable(code, "Point")
    assert "Point(x, *, y, z)" in qmd


def test_position_only_and_keyword_only_signatures():
    code = """
    @dataclass
    def func(a, b, /, c, d, *, e, f):
        pass
    """
    qmd = render_code_variable(code, "func")
    assert "func(a, b, /, c, d, *, e, f)" in qmd
