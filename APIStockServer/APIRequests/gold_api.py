import requests


class GoldApi:

    @classmethod
    def metals_get_current_price(cls, metal_name):
        header = {"x-access-token": "goldapi-1sj718l0f5hae6-io", "Content-Type": "application/json"}
        response = requests.get(f'https://www.goldapi.io/api/{metal_name}/USD', headers=header)
        # {'timestamp': 1646564733, 'metal': 'XAG', 'currency': 'USD', 'exchange': 'FOREXCOM',
        # 'symbol': 'FOREXCOM:XAGUSD', 'prev_close_price': 25.184, 'open_price': 25.184, 'low_price': 25.046,
        # 'high_price': 25.745, 'open_time': 1646352000, 'price': 25.711, 'ch': 0.527, 'chp': 2.09, 'ask': 25.74,
        # 'bid': 25.682}
        return response.json()


if __name__ == "__main__":
    # Gold price
    print("Gold:")
    spot_price = GoldApi.metals_get_current_price("XAU")['price']
    print(spot_price)