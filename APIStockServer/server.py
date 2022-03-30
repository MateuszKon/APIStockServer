from flask import Flask
import time

from alerts import MetalEtfAlerts, AlertsScheduler
from APIRequests import Finnhub, GoldApi
from modules.config_file import ConfigFile
from modules.email_sender import EmailSender

app = Flask(__name__)


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
    config_obj = ConfigFile("config.ini")
    finnhub_apis, goldapi_apis = initialize_api_objects(config_obj)
    email_sender = initialize_email_sender(config_obj)
    receivers_emails = config_obj.read_file_defined_by_key("Email Sender", "receiver_emails_path")
    metal_etf_alerts = MetalEtfAlerts(email_sender, goldapi_apis[0], finnhub_apis[0], receivers_emails)
    AlertsScheduler("11:52", "01:50", metal_etf_alerts.check_metal_alerts, {'self': metal_etf_alerts, 'print_log': True})
    while True:
        AlertsScheduler.run_waiting_alert()
        time.sleep(1)
