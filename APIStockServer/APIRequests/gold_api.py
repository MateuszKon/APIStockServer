import requests

from request_api import ApiRequest


class GoldApi(ApiRequest):

    def __init__(self, auth_key):
        super().__init__(auth_key)
        self._headers = {"x-access-token": "goldapi-1sj718l0f5hae6-io", "Content-Type": "application/json"}

    def current_price(self, asset_name):
        response = requests.get(f'https://www.goldapi.io/api/{asset_name}/USD', headers=self._headers)
        # {'timestamp': 1646564733, 'metal': 'XAG', 'currency': 'USD', 'exchange': 'FOREXCOM',
        # 'symbol': 'FOREXCOM:XAGUSD', 'prev_close_price': 25.184, 'open_price': 25.184, 'low_price': 25.046,
        # 'high_price': 25.745, 'open_time': 1646352000, 'price': 25.711, 'ch': 0.527, 'chp': 2.09, 'ask': 25.74,
        # 'bid': 25.682}
        return response.json()


if __name__ == "__main__":
    # Gold price
    print("Gold:")
    spot_price = GoldApi.current_price("XAU")['price']
    print(spot_price)
