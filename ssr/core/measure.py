import enum
import itertools
import typing as t
from datetime import datetime
from pathlib import Path

import ssr


class State(enum.Flag):
    READY = enum.auto()
    START = enum.auto()
    UPDATE = enum.auto()
    FINISH = enum.auto()
    END = enum.auto()
    AFTER = enum.auto()

    @classmethod
    def finished(state) -> bool:
        return bool(state & (State.FINISH | State.END | State.AFTER))

    @classmethod
    def measuring(state) -> bool:
        return bool(state & State.UPDATE)


class DataFileInfo:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._header = []

    @property
    def name(self) -> str:
        return self._path.name

    @property.setter
    def name(self, name: str) -> None:
        self._path = self._path.parent / name

    @property
    def delimiter(self) -> str:
        if self._delimiter is None:
            return self._delimiter
        else:
            self._calc_delimiter()

    @property.setter
    def delimiter(self, delimiter: str) -> None:
        self._delimiter = delimiter

    @property
    def header(self) -> list[str]:
        return self._header

    @property.setter
    def header(self, header: list[str]) -> None:
        self._header = header

    def add_header(self, txt: str) -> None:
        self._header.append(txt)

    def _calc_delimiter(self):
        match self._path.suffix:
            case ".csv":
                return ","
            case ".tsv":
                return "\t"
            case ".dat":
                return "\t"
            case _:
                return "\t"


class DataFile:
    def __init__(self, path: Path, delimiter: str | None) -> None:
        self._path = path

        if delimiter is not None:
            self._delimiter = delimiter
        else:
            match path.suffix:
                case ".csv":
                    self._delimiter = ","
                case ".tsv":
                    self._delimiter = "\t"
                case ".dat":
                    self._delimiter = "\t"
                case _:
                    self._delimiter = "\t"

    def create(self, override: bool) -> None:
        if not override and self._path.exists():
            raise FileExistsError()

        self._file = self._path.open(encoding="utf-8")

    def write(self, *data: t.Iterable | str) -> None:
        text = self._delimiter.join(str, itertools.chain.from_iterable(data)) + "\n"
        self._file.write(text)

    def close(self) -> None:
        if not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


class MeasureContext:
    _calibration = {}

    def __init__(self, config: ssr.core.Config) -> None:
        self._datafile = DataFileInfo(
            config.datadir / datetime.now().isoformat() + ".csv"
        )
        self._macro_config = config.macro

    @property
    def datafile(self) -> DataFileInfo:
        return self._datafile

    @property
    def macro_config(self) -> dict[str, t.Any]:
        return self._macro_config

    def calibration(self, path, value) -> float:
        pass

    def set_label():
        pass

    def write_file():
        pass

    def set_plot_info():
        pass

    def save_data():
        pass

    def save():
        pass

    def plot_data():
        pass

    def plot():
        pass

    def no_plot():
        pass


class Measure:
    def __init__(self, config: ssr.core.Config) -> None:
        self.data = DataFile()

    def run(self):
        pass

    def finish():
        pass
