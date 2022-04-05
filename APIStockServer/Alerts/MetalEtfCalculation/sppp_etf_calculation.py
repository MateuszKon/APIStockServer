from APIStockServer.Alerts.MetalEtfCalculation import SprottEtfCalculation


class SpppEtfCalculation(SprottEtfCalculation):

    def handled_etf(self) -> str:
        return "SPPP"

    def get_metal_symbols(self) -> list:
        return ["XPT", "XPD"]

    def current_spot_price(self):
        return [self.spot_data.current_spot_price(metal) for metal in self.get_metal_symbols()]
