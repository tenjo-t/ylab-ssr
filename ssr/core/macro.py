import typing as t
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

from .context import EndContext, StartContext, UpdateContext


class Macro(t.NamedTuple):
    update: t.Callable[[UpdateContext], None]
    start: t.Callable[[StartContext], None] | None
    end: t.Callable[[EndContext], None] | None

    @staticmethod
    def from_file(path: Path):
        name = path.stem

        # importlibを使って動的にpythonファイルを読み込む
        spec = spec_from_loader(name, SourceFileLoader(name, str(path)))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        # start関数のチェック
        if hasattr(module, "start") and callable(module.start):
            if module.start.__code__.co_argcount == 1:
                start = module.start
            else:
                raise SyntaxError("関数の引数は一つです")
        else:
            start = None

        # update関数のチェック
        if hasattr(module, "update") and callable(module.update):
            if module.update.__code__.co_argcount == 1:
                update = module.update
            else:
                raise SyntaxError("関数の引数は一つです")
        else:
            raise SyntaxError("update関数は必須です")

        # end関数のチェック
        if hasattr(module, "end") and callable(module.end):
            if module.end.__code__.co_argcount == 1:
                end = module.end
            else:
                raise SyntaxError("関数の引数は一つです")
        else:
            end = None

        return Macro(update, start, end)
