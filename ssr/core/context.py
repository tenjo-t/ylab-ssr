import typing as t
from datetime import datetime
from pathlib import Path

from .datafile import DataFile


class StartContext:
    """マクロのstart関数として引数に渡されるメインのプログラムとやり取りをするクラス

    Attributes
    ----------
    filename: str
        保存するファイルの名前。
    header: list[str]
        保存するファイルのヘッダー。
    delimiter: str | None
        保存するファイルのデータを区切る文字。
    macro_config: dict[str,Any]
        設定ファイルに書かれたマクロ用の設定。読み取り専用。

    Methods
    -------
    set_calibration(key, path)
        キャリブレーション用のファイルを用いて補間関数を作る。keyに異なる文字列を渡すことで複数作れる。
    """

    def __init__(self, macro_config: dict[str, t.Any]) -> None:
        self.filename = datetime.now().isoformat() + ".csv"
        self.header: list[str] = []
        self.delimiter: str | None = None
        self._macro_config = macro_config

    @property
    def macro_config(self) -> dict[str, t.Any]:
        return self._macro_config

    def set_calibration(self, key: str, path: str | Path) -> None:
        pass


class UpdateContext:
    """マクロのupdate関数として引数に渡されるメインのプログラムとやり取りをするクラス

    Attributes
    ----------
    macro_config: dict[str,Any]
        設定ファイルに書かれたマクロ用の設定。読み取り専用。

    Methods
    -------
    calibration(key, path)
        keyで紐付けられた補間関数で補完する。
    plot(x, y, label)
        データをプロットする。同じラベルのデータは一連のデータとなる。
    write(*data)
        データをファイルに書き込む。複数の引数や配列などを渡すと自動で区切られて書き込まれる。
    finish()
        測定が終了したことを知らせる。この関数が呼ばれないと測定が永遠に終わらない。
    """

    def __init__(
        self,
        datafile: DataFile,
        macro_config: dict[str, t.Any],
    ) -> None:
        self._datafile = datafile
        self._macro_config = macro_config
        self._finish = False

    @property
    def macro_config(self) -> dict[str, t.Any]:
        return self._macro_config

    def calibration(self, key: str, value: float) -> float:
        pass

    def plot(self, x: float, y: float, label: str = "default"):
        pass

    def write(self, *data: tuple[t.Any]) -> None:
        self._datafile.write(*data)

    def finish(self) -> None:
        self._finish = True


class EndContext:
    """マクロのend関数として引数に渡されるメインのプログラムとやり取りをするクラス

    Attributes
    ----------
    filepath: Path
        測定したデータファイルが存在するパス。
    macro_config: dict[str,Any]
        設定ファイルに書かれたマクロ用の設定。読み取り専用。
    """

    def __init__(self, path, macro_config: dict[str, t.Any]) -> None:
        self.filepath = path
        self._macro_config = macro_config

    @property
    def macro_config(self) -> dict[str, t.Any]:
        return self._macro_config
