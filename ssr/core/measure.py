import enum

from .config import Config
from .context import EndContext, StartContext, UpdateContext
from .datafile import DataFile
from .macro import Macro


class State(enum.Flag):
    READY = enum.auto()
    START = enum.auto()
    UPDATE = enum.auto()
    END = enum.auto()
    FINISH = enum.auto()


class Measure:
    def __init__(self, config: Config) -> None:
        self._state = State.READY
        self._macro = Macro.from_file(config.macropath)
        self._config = config

    @property
    def state(self) -> State:
        return self._state

    def run(self):
        # Ready
        self._state = State.START

        # Start
        start_ctx = StartContext(self._config.macro)
        if self._macro.start is not None:
            self._macro.start(start_ctx)
        self._state = State.UPDATE

        # Update
        datafile = self._config.datadir / start_ctx.filename
        with DataFile.create(datafile, start_ctx.delimiter, False) as f:
            update_ctx = UpdateContext(f, self._config.macro)
            while update_ctx._finish:
                self._macro.update(update_ctx)
        self._state = State.END

        # End
        end_ctx = EndContext(datafile, self._config.macro)
        if self._macro.end is not None:
            self._macro.end(end_ctx)
        self._state = State.FINISH

    def abort():
        pass
