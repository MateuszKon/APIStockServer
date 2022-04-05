from APIStockServer.Alerts.MetalEtfCalculation import SprottEtfCalculation


class PslvEtfCalculation(SprottEtfCalculation):

    def handled_etf(self) -> str:
        return "PSLV"

    def get_metal_symbols(self) -> list:
        return ["XAG"]
