from abc import abstractmethod

from bs4 import BeautifulSoup
import requests

from APIStockServer.DataAcquisition.sprott_etf import AbstractMetalEtf


class AbstractSprottEtf(AbstractMetalEtf):

    @classmethod
    @abstractmethod
    def get_etf_url(cls):
        pass

    @classmethod
    def get_etf_allocation(cls, etf_name):
        """
        Scraping information from https://sprott.com/ about inputed etf - scraped info is amount of shares in etf and
        amount of precious metals holding by this etf
        :param etf_name: etf string name
        :return: Tuple of etf shares amount and total weight of metal holding. If selected etf if SPPP, then second
        element of the tuple is a list of weights' of platinium and palladium (as SPPP holds two types of precious
        metal)
        """
        if etf_name != cls.handled_etf():
            raise ValueError(f"'{etf_name}' is not handled etf by {__class__} class!")

        html_content = requests.get(cls.get_etf_url()).text

        # Parse the html content - shares of etf (units of etf)
        soup = BeautifulSoup(html_content, "lxml")
        units_tag = soup.find("td", attrs={"headers": "previousClose_outstanding"})
        units_outstanding = int(units_tag.text.replace(",", ""))

        # Parse the html content - amount of metal holding
        ounces_tag = units_tag.parent.next_sibling.next_sibling.td
        total_ounces = int(ounces_tag.text.replace(",", ""))

        return units_outstanding, total_ounces
