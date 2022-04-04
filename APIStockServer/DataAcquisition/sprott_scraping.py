from enum import Enum

from bs4 import BeautifulSoup
import requests

from APIStockServer.DataAcquisition import IPreciousMetalEtfInformation


class MetalEtf(Enum):
    PHYS = 1
    PLSV = 2
    SPPP = 3


class SprottScraping(IPreciousMetalEtfInformation):

    _URLS = {MetalEtf.PHYS: "https://sprott.com/investment-strategies/physical-bullion-trusts/gold/",
             MetalEtf.PLSV: "https://sprott.com/investment-strategies/physical-bullion-trusts/silver/",
             MetalEtf.SPPP: "https://sprott.com/investment-strategies/physical-bullion-trusts/platinum-and-palladium/",
             }

    def etf_allocation(self, etf_name: str):
        """
        Scraping information from https://sprott.com/ about inputed etf - scraped info is amount of shares in etf and
        amount of precious metals holding by this etf
        :param etf_name: MetalEtf enumerate value
        :return: Tuple of etf shares amount and total weight of metal holding. If selected etf if SPPP, then second
        element of the tuple is a list of weights' of platinium and palladium (as SPPP holds two types of precious
        metal)
        """
        try:
            etf = MetalEtf[etf_name]
        except KeyError:
            raise ValueError(f"'{etf_name}' is not handled etf by SprottScraping class!")
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(self._URLS[etf]).text

        # Parse the html content - shares of etf (units of etf)
        soup = BeautifulSoup(html_content, "lxml")
        units_tag = soup.find("td", attrs={"headers": "previousClose_outstanding"})
        units_outstanding = int(units_tag.text.replace(",", ""))

        # Parse the html content - amount of metal holding
        ounces_tag = units_tag.parent.next_sibling.next_sibling.td
        total_ounces = int(ounces_tag.text.replace(",", ""))

        # If Etf is SPPP, there is two types of metals in holding - platinum and palladium
        if etf is MetalEtf.SPPP:
            palladium_ounces_tag = ounces_tag.parent.next_sibling.next_sibling.td
            palladium_total_ounces = int(palladium_ounces_tag.text.replace(",", ""))
            platinum_total_ounces = total_ounces
            total_ounces = [platinum_total_ounces, palladium_total_ounces]

        return units_outstanding, total_ounces


if __name__ == "__main__":
    metal_list = ["PHYS", "PLSV", "SPPP"]
    for metal_etf in metal_list:
        print(metal_etf)
        print(SprottScraping().etf_allocation(metal_etf))
        print()
