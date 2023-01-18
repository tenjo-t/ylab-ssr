import typing as t
from pathlib import Path

import tomllib

import ssr.util


class ConfigError(ssr.util.SSRError):
    pass


class Config(t.NamedTuple):
    """SSRの基本設定

    Attributes
    ----------
    datadir: Path
        データファイルを保存するフォルダへのパス
    tmpdir: Path
        一時ファイルを保存するフォルダへのパス
    macropath: Path
        マクロファイルへのパス
    macro: dict[str, t.Any]
        マクロが自由に設定できる設定

    Examples
    -------
    ```toml
    DATADIR = "path/to/datadir"
    TMPDIR  = "path/to/tmpdir"
    MACROPATH = "path/to/macropath"

    # マクロが自由に設定できる設定
    [MACRO]
    filename = "foo.csv"
    ```

    """

    datadir: Path
    tmpdir: Path
    macropath: Path
    macro: dict[str, t.Any]

    @staticmethod
    def from_toml(path: Path):
        with path.open("rb") as f:
            config = tomllib.load(f)

        if not "DATADIR" in config:
            raise ConfigError("DATADIRは必須です")
        datadir = Path(config["DATADIR"])

        if not "TMPDIR" in config:
            raise ConfigError("TEMPDIRは必須です")
        tmpdir = Path(config["TMPDIR"])

        if not "MACROPATH" in config:
            raise ConfigError("MACRODIRは必須です")
        macropath = Path(config["MACROPATH"])

        macro = config["MACRO"] if "MACRO" in config else {}

        return Config(datadir, tmpdir, macropath, macro)
