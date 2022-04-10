from typing import List

from APIStockServer.Alerts.AlertSender import EmailSender
from APIStockServer.Alerts.AlertSender.Receivers import ReceiversSimpleList
from APIStockServer.Alerts.MetalEtfCalculation import SprottEtfCalculation
from APIStockServer.DataAcquisition import IPreciousMetalSpotData, IPreciousMetalEtfData, IPreciousMetalEtfInformation
from APIStockServer.DataAcquisition import Finnhub, GoldApi
from APIStockServer.modules.config_file import ConfigFile


def initialize_api_objects(config: ConfigFile):
    finnhub_keys = config.read_file_defined_by_key("API Keys", "finnhub")
    finnhub_apis = list(Finnhub(key) for key in finnhub_keys)
    goldapi_keys = config.read_file_defined_by_key("API Keys", "goldapi")
    goldapi_apis = list(GoldApi(key) for key in goldapi_keys)
    return finnhub_apis, goldapi_apis


def initialize_email_sender(config: ConfigFile):
    config_email = config['Email Sender']
    email_sender = EmailSender(config_email['smtp_server'], config_email['sender_email'], config_email['password'])
    return email_sender


def initialize_sprott_etf_calculators(metal_etfs_classes: List[SprottEtfCalculation],
                                      spot_data: IPreciousMetalSpotData,
                                      etf_data: IPreciousMetalEtfData,
                                      etf_info: IPreciousMetalEtfInformation,
                                      ):
    calculators = list()
    for C in metal_etfs_classes:
        calculators.append(C(spot_data=spot_data,
                             etf_data=etf_data,
                             etf_info=etf_info
                             )
                           )
    return calculators


def initialize_receivers_obj(config: ConfigFile):
    receivers_emails = config.read_file_defined_by_key("Email Sender", "receiver_emails_path")
    return ReceiversSimpleList(receivers_emails)
