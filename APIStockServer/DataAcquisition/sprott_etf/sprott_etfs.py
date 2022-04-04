from bs4 import BeautifulSoup
import requests

from APIStockServer.DataAcquisition.sprott_etf import AbstractSprottEtf


class SprottPlsv(AbstractSprottEtf):

    @classmethod
    def handled_etf(cls):
        return "PLSV"

    @classmethod
    def get_etf_url(cls):
        return "https://sprott.com/investment-strategies/physical-bullion-trusts/silver/"


class SprottPhys(AbstractSprottEtf):

    @classmethod
    def handled_etf(cls):
        return "PHYS"

    @classmethod
    def get_etf_url(cls):
        return "https://sprott.com/investment-strategies/physical-bullion-trusts/gold/"


class SprottSppp(AbstractSprottEtf):

    @classmethod
    def handled_etf(cls):
        return "SPPP"

    @classmethod
    def get_etf_url(cls):
        return "https://sprott.com/investment-strategies/physical-bullion-trusts/platinum-and-palladium/"

    @classmethod
    def get_etf_allocation(cls, etf_name):
        if etf_name != cls.handled_etf():
            raise ValueError(f"'{etf_name}' is not handled etf by {__class__} class!")

        html_content = requests.get(cls.get_etf_url()).text

        # Parse the html content - shares of etf (units of etf)
        soup = BeautifulSoup(html_content, "lxml")
        units_tag = soup.find("td", attrs={"headers": "previousClose_outstanding"})
        units_outstanding = int(units_tag.text.replace(",", ""))

        # Parse the html content - amount of metal holding
        ounces_tag = units_tag.parent.next_sibling.next_sibling.td
        platinum_total_ounces = int(ounces_tag.text.replace(",", ""))

        # Etf is SPPP, there is two types of metals in holding - platinum and palladium
        palladium_ounces_tag = ounces_tag.parent.next_sibling.next_sibling.td
        palladium_total_ounces = int(palladium_ounces_tag.text.replace(",", ""))
        total_ounces = [platinum_total_ounces, palladium_total_ounces]

        return units_outstanding, total_ounces