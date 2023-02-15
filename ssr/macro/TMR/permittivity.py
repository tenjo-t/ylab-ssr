import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ssr.core.context import EndContext, StartContext, UpdateContext

# 真空の誘電率
e = 8.8541878128 * 10 ** (-12)


def start(ctx: StartContext):
    global lcr, keithley, area, depth, start_time, count

    lcr = ctx.get_gpib_instrument(7)
    keithley = ctx.get_gpib_instrument(11)

    ctx.filename = ctx.macro_config.filename
    area = ctx.macro_config.area
    depth = ctx.macro_config.depth
    # volt = ctx.macro_config.volt
    volt = lcr.query("VOLT?").replace(" ", "")

    ctx.write(f"# s = {area}[mm2]")
    ctx.write(f"# d = {depth}[mm]")
    ctx.write(f"# V = {volt}[V]")
    ctx.write(
        "time[s]",
        "frequency[Hz]",
        "temperature[K]",
        "capacitance[C]",
        "permittivity_real",
        "permittivity_image",
        "tan_delta",
        "resistance_Pt[Ohm]",
    )

    ctx.set_calibration("Pt", ctx.resolv_path(ctx.macro_config.calibration))
    # ctx.set_plot_info()
    start_time = time.time()
    count = 0


def update(ctx: UpdateContext):
    global e, lcr, keithley, area, depth, start_time, count

    elapsed_time = time.time() - start_time
    # 周波数は10の3乗から6乗まで
    frequency = pow(10, 3 + count * 0.2)

    # 周波数設定
    lcr.write(f"FREQ {frequency}")
    time.sleep(0.5)

    # LCRのデータ読み取り(コンマ区切りの文字列)
    lcr_ans = lcr.query("FETC?").split(",")

    capacitance = float(lcr_ans[0])
    tan_delta = float(lcr_ans[1])
    permittivity_real = capacitance * depth / (area * e) * 1000  # (1000は単位合わせ)
    permittivity_image = permittivity_real * tan_delta

    # プラチナ抵抗温度計の抵抗を取得
    resistance = float(keithley.query("FETCH?"))
    temperature = ctx.calibration("Pt", resistance)

    ctx.write(
        elapsed_time,
        frequency,
        temperature,
        capacitance,
        permittivity_real,
        permittivity_image,
        tan_delta,
        resistance,
    )

    ctx.plot(temperature, permittivity_real)

    # 5時間経ったら勝手に終了するように
    if elapsed_time > 5 * 60 * 60:
        ctx.finish()
    else:
        count = (count + 1) % 16


def end(ctx: EndContext):
    global lcr, keithley

    if ctx.error is not None:
        # エラー処理
        pass
