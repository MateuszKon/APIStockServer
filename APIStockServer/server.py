import time
import os

from APIStockServer.Alerts import MetalEtfAlerts, AlertsScheduler
from APIStockServer.Alerts.MetalEtfCalculation import PhysEtfCalculation, PslvEtfCalculation, SpppEtfCalculation
from APIStockServer.DataAcquisition import MetalEtfScraping
from APIStockServer.modules.config_file import ConfigFile
from APIStockServer.initialize import initialize_api_objects, initialize_email_sender,\
    initialize_sprott_etf_calculators, initialize_receivers_obj


if __name__ == "__main__":
    # Initialize object handling config file
    config_obj = ConfigFile(os.path.join(os.path.dirname(__file__), "config.ini"))

    # Initialize API objects (Finnhub, GoldAPI)
    finnhub_apis, goldapi_apis = initialize_api_objects(config_obj)

    # Initialize Email Sender object
    email_sender = initialize_email_sender(config_obj)

    # Initialize receivers object
    receivers = initialize_receivers_obj(config_obj)

    # Initialize Sprott Etfs discount calculators
    list_of_sprott_etfs = [PhysEtfCalculation, PslvEtfCalculation, SpppEtfCalculation]
    sprott_etfs_calculators = initialize_sprott_etf_calculators(list_of_sprott_etfs,
                                                                goldapi_apis[0],
                                                                finnhub_apis[0],
                                                                MetalEtfScraping())

    metal_etf_alerts = MetalEtfAlerts(email_sender, sprott_etfs_calculators, receivers)
    AlertsScheduler(metal_etf_alerts.check_metal_alerts, print_log=True,
                    start_hour=10, start_minute=30,
                    stop_hour=1, stop_minute=50,
                    )
    while True:
        AlertsScheduler.run_waiting_alert()
        time.sleep(60)
