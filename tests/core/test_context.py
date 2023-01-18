from pathlib import Path

from ssr.core.context import EndContext, StartContext, UpdateContext


def test_start_context():
    macro = {"foo": 1}
    ctx = StartContext(macro)

    assert ctx.macro_config == macro

    ctx.macro_config["bar"] = 2
    assert macro["bar"] == 2


def test_update_context():
    # mock
    class DataFile:
        called = 0

        def write(self, *data):
            self.called += 1

    datafile = DataFile()
    macro = {"foo": 1}
    ctx = UpdateContext(datafile, macro)

    assert ctx.macro_config == macro
    assert ctx._finish == False

    ctx.write("")
    assert datafile.called == 1

    ctx.finish()
    assert ctx._finish == True


def test_end_context():
    path = Path("./end")
    macro = {"foo": 1}
    ctx = EndContext(path, macro)

    assert ctx.filepath == path
    assert ctx.macro_config == macro
