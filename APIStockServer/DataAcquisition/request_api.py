import requests


class ApiRequest:

    def __init__(self, auth_key, headers):
        self._auth_key = auth_key
        self._headers = headers

    def _init_req(self) -> requests.Session:
        s = requests.Session()
        s.headers.update(self._headers)
        return s
