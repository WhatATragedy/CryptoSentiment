import requests
from typing import Dict, List

class CoinMarketCap():
    def __init__(self, api_key, url="https://pro-api.coinmarketcap.com/"):
        self._url = url
        if api_key is None:
            raise ValueError("API Key must be set..")
        self._api_key = api_key
        self._headers = {
            'Accept': 'application/json',
            'X-CMC_PRO_API_KEY': self._api_key
        }

    @staticmethod
    def _did_error(r):
        if data := r.json().get("status"):
            if data.get("error_message"):
                raise SystemError(data.get("error_message"))
            else:
                return False


    def get_listings(self, return_limit=50, direction="back", api_limit=100) -> List:
        domain = f"{self._url}v1/cryptocurrency/listings/latest?limit={api_limit}"
        r = requests.get(domain, headers=self._headers)
        if self._did_error(r):
            return []
        self.data = r.json().get("data")
        if direction == "back":
            return self.data[-return_limit:]
        else:
            return self.data[:return_limit]

    def get_symbols_and_rank(self, r=None, limit=20) -> Dict:
        symbols = dict()
        if r:
            if isinstance(r, list):
                self.data = r
            else:   
                if r.get("data"):
                    self.data = r.get("data")
        for asset in self.data[:limit]:
            symbols[asset.get("symbol")] = asset.get("cmc_rank")
        return symbols



if __name__ == "__main__":
    cmc = CoinMarketCap(api_key="")
    data = cmc.get_listings()
    print(cmc.get_symbols(data))