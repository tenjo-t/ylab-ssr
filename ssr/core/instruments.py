import pyvisa

import ssr.util


class InstrumentError(ssr.util.SSRError):
    pass


class InstrumentManager:
    def __init__(self) -> None:
        self._rm = pyvisa.ResourceManager()

    def list_resources(self) -> tuple[str]:
        return self._rm.list_reources()

    def open_resource(self, address: str):
        instr = self._rm.open_resource(address)

        # IDNコマンドで機器と通信. GPIB番号に機器がないとここでエラー
        try:
            instr.query("*IDN?")
        except pyvisa.VisaIOError as e:
            raise InstrumentError(
                f"{address}が`IDN?`コマンドに応答しません. 設定されているGPIBの番号が間違っている可能性があります"
            ) from e

        return instr

    def open_gpib_resource(self, address: int):
        return self.open_resource(f"GPIB0::{address}::INSTR")

    def close(self) -> None:
        self._rm.close()
