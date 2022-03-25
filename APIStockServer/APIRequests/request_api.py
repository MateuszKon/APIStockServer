import os

from APIStockServer.modules.util import get_environ_file_path


class ApiRequest:

    def __init__(self, auth_key):
        self._auth_key = auth_key

    def current_price(self, asset_name):
        pass

    # @classmethod
    # def _is_auth_key(cls):
    #     """
    #     Checks if authentication key is already read into application
    #     :return: True or False
    #     """
    #     return True if cls._AUTH_KEY else False
    #
    # @classmethod
    # def _auth_key_file(cls):
    #     """
    #     Gets authentication key from file defined by environment variable 'APISTOCK_KEY_FILE'
    #     """
    #     try:
    #         # root_path is parent folder of folder containing finhub_api.py
    #         root_path = os.path.dirname(os.path.realpath(__file__))
    #         root_path = os.path.dirname(root_path)
    #         file_path = get_environ_file_path("APISTOCK_KEY_FILE",
    #                                           root_path=root_path)
    #         with open(file_path) as f_r:
    #             key = f_r.readline()
    #             if key:
    #                 cls._AUTH_KEY = key
    #             else:
    #                 raise KeyError(f"File {file_path} does not contain valid authentication key!")
    #     except KeyError as e:
    #         raise Exception('Check README.md file for more information.').with_traceback(e.__traceback__)