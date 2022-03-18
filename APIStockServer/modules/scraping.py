from bs4 import BeautifulSoup
import requests

from enum import Enum


class MetalEtf(Enum):
    PHYS = 1
    PLSV = 2
    SPPP = 3
    UU = 4


class SprottScraping:

    _URLS = {MetalEtf.PHYS: "https://sprott.com/investment-strategies/physical-bullion-trusts/gold/",
             MetalEtf.PLSV: "https://sprott.com/investment-strategies/physical-bullion-trusts/silver/",
             MetalEtf.SPPP: "https://sprott.com/investment-strategies/physical-bullion-trusts/platinum-and-palladium/",
             MetalEtf.UU: "https://sprott.com/investment-strategies/physical-commodity-funds/uranium/",
             }

    @classmethod
    def get_etf_allocation(cls, etf: MetalEtf):
        """
        Scraping information from https://sprott.com/ about inputed etf - scraped info is amount of shares in etf and
        amount of precious metals holding by this etf
        :param etf: MetalEtf enumerate value
        :return: Tuple of etf shares amount and total weight of metal holding. If selected etf if SPPP, then second
        element of the tuple is a tuple of weights' of platinium and palladium (as SPPP holds two types of precious
        metal)
        """
        if not isinstance(etf, MetalEtf):
            raise ValueError(f"'{etf}' is not MetalEtf enum type!")
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(cls._URLS[etf]).text

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
            total_ounces = (platinum_total_ounces, palladium_total_ounces)

        return units_outstanding, total_ounces


if __name__ == "__main__":
    for etf in MetalEtf:
        print(etf)
        print(SprottScraping.get_etf_allocation(etf))
        print()
