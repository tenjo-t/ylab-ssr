from pathlib import Path

from ssr.core.datafile import DataFile


def test_datafile(tmpdir):
    data = Path(tmpdir) / "test.csv"
    with data.open("w", encoding="utf-8") as f:
        with DataFile(f, ",") as d:
            pass
        assert f.closed

    with data.open("w", encoding="utf-8") as f:
        try:
            with DataFile(f, ",") as d:
                raise Exception()
        except:
            assert f.closed


def test_datafile_create(tmpdir):
    tmpdir = Path(tmpdir)

    csv = tmpdir / "test.csv"
    with DataFile.create(csv) as f:
        assert f._delimiter == ","
        f.write("foo", ["bar", "baz"])
    assert csv.read_text() == "foo,bar,baz\n"

    tsv = tmpdir / "test.tsv"
    with DataFile.create(tsv) as f:
        assert f._delimiter == "\t"
        f.write("foo", ["bar", "baz"])
    assert tsv.read_text() == "foo\tbar\tbaz\n"

    dat = tmpdir / "test.dat"
    with DataFile.create(dat) as f:
        assert f._delimiter == "\t"
        f.write("foo", ["bar", "baz"])
    assert dat.read_text() == "foo\tbar\tbaz\n"

    default = tmpdir / "test"
    with DataFile.create(default) as f:
        assert f._delimiter == "\t"
        f.write("foo", ["bar", "baz"])
    assert default.read_text() == "foo\tbar\tbaz\n"
