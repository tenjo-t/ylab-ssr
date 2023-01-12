import enum
import itertools
import typing as t
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

    def write(self, *data: t.Iterable | str) -> None:
        text = self._delimiter.join(str, itertools.chain.from_iterable(data)) + "\n"
        self._path.write_text(text)


class Measure:
    def __init__(self) -> None:
        pass

    def start_macro():
        pass

    def finish():
        pass

    def set_file_name():
        pass

    def set_calibration():
        pass

    def calibration():
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
