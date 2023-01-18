from pathlib import Path

import pytest

from ssr.core.macro import Macro


def test_macro_all(tmpdir):
    path = Path(tmpdir) / "macro.py"
    path.write_text(
        """def start(ctx):
    pass

def update(ctx):
    pass

def end(ctx):
    pass
"""
    )

    macro = Macro.from_file(path)

    assert callable(macro.start)
    assert macro.start.__code__.co_argcount == 1
    assert callable(macro.update)
    assert macro.update.__code__.co_argcount == 1
    assert callable(macro.end)
    assert macro.end.__code__.co_argcount == 1


def test_macro_update(tmpdir):
    path = Path(tmpdir) / "macro.py"
    path.write_text(
        """def update(ctx):
    pass
"""
    )

    macro = Macro.from_file(path)

    assert callable(macro.update)
    assert macro.update.__code__.co_argcount == 1
    assert macro.start is None
    assert macro.end is None


def test_macro_no_update(tmpdir):
    path = Path(tmpdir) / "macro.py"
    path.write_text("")

    with pytest.raises(SyntaxError) as e:
        macro = Macro.from_file(path)

    assert str(e.value) == "update関数は必須です"


def test_macro_invalid_args(tmpdir):
    path = Path(tmpdir) / "macro.py"
    path.write_text(
        """def update():
    pass
"""
    )

    with pytest.raises(SyntaxError) as e:
        macro = Macro.from_file(path)

    assert str(e.value) == "関数の引数は一つです"
