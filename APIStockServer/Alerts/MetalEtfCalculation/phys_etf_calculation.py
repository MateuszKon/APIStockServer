from APIStockServer.Alerts.MetalEtfCalculation import SprottEtfCalculation


class PhysEtfCalculation(SprottEtfCalculation):

    def handled_etf(self) -> str:
        return "PHYS"

    def get_metal_symbols(self) -> list:
        return ["XAU"]
