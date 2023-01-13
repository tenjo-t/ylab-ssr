import typing as t
from pathlib import Path

import tomllib

import ssr


class ConfigError(ssr.SSRError):
    pass


class Config:
    macro: dict[str, t.Any]

    def __init__(self, path: Path) -> None:
        with path.open(encoding="utf-8") as f:
            config = tomllib.load(f)

        datadir = config["DATADIR"]
        if datadir is None:
            raise ConfigError("DATADIRは必須です")
        self.datadir = Path(datadir)

        tmpdir = config["TMPDIR"]
        if tmpdir is None:
            raise ConfigError("TEMPDIRは必須です")
        self.tmpdir = Path(tmpdir)

        macrodir = config["MACRODIR"]
        if macrodir is None:
            raise ConfigError("MACRODIRは必須です")
        self.macrodir = Path(macrodir)

        if (macro := config["MACRO"]) is not None:
            self.macro = macro
