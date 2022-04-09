from APIStockServer.DataAcquisition import IPreciousMetalEtfInformation
from APIStockServer.DataAcquisition.sprott_etf import AbstractMetalEtf


class MetalEtfScraping(IPreciousMetalEtfInformation):

    def __init__(self, register_default=True, additional_etf_registration_list=list()):
        """
        MetalEtfScraping object handles scraping information about etfs. At default (register_default=True) object can
        handle etfs: PHYS, PLSV, SPPP. Each etf is registered as subclass of AbstractMetalEtf
        :param register_default: True - register default etfs subclasses: SprottPhys, SprottPlsv, SprottSppp
        :param additional_etf_registration_list: list of AbstractMetalEtf subclasses for registering handled etfs
        """
        self.registered_etfs = dict()
        if register_default:
            from APIStockServer.DataAcquisition.sprott_etf import SprottPhys, SprottPslv, SprottSppp
            self.register_metal_etf(SprottPhys)
            for SprottEtf in [SprottPhys, SprottPslv, SprottSppp]:
                self.register_metal_etf(SprottEtf)
        for AdditionalEtf in additional_etf_registration_list:
            self.register_metal_etf(AdditionalEtf)

    def register_metal_etf(self, metal_etf: type(AbstractMetalEtf)):
        self.registered_etfs[metal_etf.handled_etf()] = metal_etf

    def etf_allocation(self, etf_name: str):
        """
        Currently scraping information from https://sprott.com/ about inputed etf - scraped info is amount of shares in etf and
        amount of precious metals holding by this etf. Might be expanded to other etfs / other sites.
        :param etf_name: etf string name
        :return: Tuple of etf shares amount and total weight of metal holding. If selected etf if SPPP, then second
        element of the tuple is a list of weights' of platinium and palladium (as SPPP holds two types of precious
        metal)
        """
        if etf_name not in self.registered_etfs:
            raise ValueError(f"'{etf_name}' is not handled etf by MetalEtfScraping class!")
        metal_etf: AbstractMetalEtf = self.registered_etfs[etf_name]
        return metal_etf.get_etf_allocation(etf_name)


if __name__ == "__main__":
    etf_metal_list = ["PHYS", "PSLV", "SPPP"]
    for metal_etf in etf_metal_list:
        print(metal_etf)
        print(MetalEtfScraping().etf_allocation(metal_etf))
        print()
