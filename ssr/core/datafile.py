import typing as t
from io import TextIOWrapper
from pathlib import Path

import ssr.util


class DataFile:
    def __init__(self, file: TextIOWrapper, delimiter: str) -> None:
        self.delimiter = delimiter
        self._file = file

    def write(self, *data: tuple) -> None:
        text = self.delimiter.join(map(str, ssr.util.flatten(data))) + "\n"
        self._file.write(text)
        # 事故でプログラムが強制終了しても途中までのデータを残すために毎回ファイルに書き込む
        self._file.flush()

    def close(self) -> None:
        if not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @staticmethod
    def create(path: Path, delimiter: str | None = None, override=False):
        mode = "w" if override else "x"
        file = path.open(mode, encoding="utf-8")
        if delimiter is None:
            match path.suffix:
                case ".csv":
                    delimiter = ","
                case ".tsv":
                    delimiter = "\t"
                case ".dat":
                    delimiter = "\t"
                case _:
                    delimiter = "\t"

        return DataFile(file, delimiter)
