import time
import threading

from APIStockServer.modules.api_handler import ApiHandler as Api
from APIStockServer.modules.email_sender import EmailSender as Email


class MetalEtfAlerts:

    def __init__(self, email_sender: Email):
        self.email = email_sender

    def start_periodic_thread(self, funct_calculate, period, *args, **kwargs):
        threading.Thread(target=funct_calculate, args=(period, *args), kwargs=kwargs, daemon=True).start()
