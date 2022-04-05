import time
import os

from APIStockServer.Alerts import MetalEtfAlerts, AlertsScheduler
from APIStockServer.Alerts.AlertSender import EmailSender
from APIStockServer.Alerts.MetalEtfCalculation import SprottEtfCalculation
from APIStockServer.Alerts.MetalEtfCalculation import PhysEtfCalculation, PslvEtfCalculation, SpppEtfCalculation
from APIStockServer.DataAcquisition import Finnhub, GoldApi, MetalEtfScraping
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


if __name__ == "__main__":
    config_obj = ConfigFile(os.path.join(os.path.dirname(__file__), "config.ini"))

    finnhub_apis, goldapi_apis = initialize_api_objects(config_obj)

    email_sender = initialize_email_sender(config_obj)

    receivers_emails = config_obj.read_file_defined_by_key("Email Sender", "receiver_emails_path")

    list_of_sprott_etfs = [PhysEtfCalculation, PslvEtfCalculation, SpppEtfCalculation]
    calculators = list()
    for C in list_of_sprott_etfs:
        C: SprottEtfCalculation
        calculators.append(C(spot_data=goldapi_apis[0],
                             etf_data=finnhub_apis[0],
                             etf_info=MetalEtfScraping()
                             )
                           )

    metal_etf_alerts = MetalEtfAlerts(email_sender, calculators, receivers_emails)
    AlertsScheduler(metal_etf_alerts.check_metal_alerts, print_log=True,
                    start_hour=10, start_minute=30,
                    stop_hour=21, stop_minute=50,
                    )
    while True:
        AlertsScheduler.run_waiting_alert()
        time.sleep(60)
