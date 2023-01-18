from pathlib import Path

import pytest

from ssr.core.config import Config, ConfigError


def test_config():
    config = Config(
        Path("./datadir"),
        Path("./tmpdir"),
        Path("./macro.py"),
        {"int": 123, "float": 1.23, "str": "123"},
    )

    assert config.datadir == Path("./datadir")
    assert config.tmpdir == Path("./tmpdir")
    assert config.macropath == Path("./macro.py")
    assert config.macro == {"int": 123, "float": 1.23, "str": "123"}


def test_config_from_toml(tmpdir):
    toml = Path(tmpdir) / "test.toml"
    toml.write_text(
        """DATADIR = "./datadir"
TMPDIR = "./tmpdir"
MACROPATH = "./macro.py"

[MACRO]
int = 123
float = 1.23
str = "123"
"""
    )

    config = Config.from_toml(toml)

    assert config.datadir == Path("./datadir")
    assert config.tmpdir == Path("./tmpdir")
    assert config.macropath == Path("./macro.py")
    assert config.macro == {"int": 123, "float": 1.23, "str": "123"}


def test_config_no_macro(tmpdir):
    toml = Path(tmpdir) / "test.toml"
    toml.write_text(
        """DATADIR = "./datadir"
TMPDIR = "./tmpdir"
MACROPATH = "./macro.py"
"""
    )

    config = Config.from_toml(toml)

    assert config.macro == {}


def test_config_invalid(tmpdir):
    toml = Path(tmpdir) / "test.toml"
    toml.write_text(
        """# DATADIR = "./datadir"
TMPDIR = "./tmpdir"
MACROPATH = "./macro.py"

[MACRO]
int = 123
float = 1.23
str = "123"
"""
    )

    with pytest.raises(ConfigError) as e:
        config = Config.from_toml(toml)

    assert str(e.value) == "DATADIRは必須です"
