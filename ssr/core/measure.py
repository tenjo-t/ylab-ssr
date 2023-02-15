import enum
from pathlib import Path

from .config import Config
from .context import EndContext, StartContext, UpdateContext
from .datafile import DataFile
from .instruments import InstrumentManager
from .macro import Macro


class State(enum.Flag):
    READY = enum.auto()
    START = enum.auto()
    UPDATE = enum.auto()
    END = enum.auto()
    FINISH = enum.auto()


class Measure:
    def __init__(self, config: Path) -> None:
        self.root = config.parent
        self._config = Config.from_toml(config)
        self._state = State.READY
        self._macro = Macro.from_file(config.macropath)

    @property
    def state(self) -> State:
        return self._state

    def run(self):
        # Ready
        instr_manager = InstrumentManager()
        self._state = State.START
        error = None

        # Start
        start_ctx = StartContext(self.root, instr_manager, self._config.macro)
        if self._macro.start is not None:
            try:
                self._macro.start(start_ctx)
            except Exception as e:
                error = e
        self._state = State.UPDATE

        # Update
        datafile = self._config.datadir / start_ctx.filename
        with DataFile.create(datafile, start_ctx.delimiter, False) as f:
            start_ctx._write_text(f)
            delimiter = f.delimiter
            update_ctx = UpdateContext(f, self._config.macro)
            try:
                while update_ctx._finish:
                    self._macro.update(update_ctx)
                error = None
            except Exception as e:
                error = e
        self._state = State.END

        # End
        end_ctx = EndContext(self.root, datafile, delimiter, self._config.macro)
        if self._macro.end is not None:
            self._macro.end(end_ctx)
        instr_manager.close()
        self._state = State.FINISH

    def abort(self):
        pass
