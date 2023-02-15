# TMR

SSR用のTMRマクロ

## Permittivity

```toml
DATADIR = "path/to/datadir"
TMPDIR  = "path/to/tmpdir"
MACROPATH = "path/to/permittivity.py"

# マクロが自由に設定できる設定
[MACRO]

# データファイルの名前
filename = "foo.csv"
# 電極面積 (mm2)
area = 1.23
# 厚さ (mm)
depth = 1.23
# volt = 10
# キャリブレーションファイルへのパス
calibration = "path/to/calibration/file"
```
