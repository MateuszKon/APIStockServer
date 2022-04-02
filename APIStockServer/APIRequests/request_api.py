import os

from APIStockServer.modules.util import get_environ_file_path


class ApiRequest:

    def __init__(self, auth_key):
        self._auth_key = auth_key

    def current_quote(self, asset_name):
        # abstract function
        pass

    def current_price(self, asset_name):
        # abstract function
        pass
