# -*- coding: utf-8 -*-

# Huobi Class

from src.core.coin.coin import Coin
from src.core.coin.lib.huobipro_api.HuobiService import Huobi as HuobiAPI
from src.core.util.exceptions import HuobiException
from src.core.util.helper import date_to_milliseconds, interval_to_milliseconds


class Huobi(Coin):
    def __init__(self,
                 exchange,
                 api_key,
                 api_secret,
                 acct_id=None,
                 proxies=None):
        super(Huobi, self).__init__(exchange, api_key, api_secret, proxies)
        self._acct_id = acct_id
        self._huobiAPI = HuobiAPI(self._api_key, self._api_secret,
                                  self._acct_id, self._proxies)

    # get config
    def getConfig(self):
        return {
            "exchange": self._exchange,
            "api_key": self._api_key,
            "api_secret": self._api_secret,
            "acct_id": self._acct_id,
            "proxies": self._proxies
        }

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._huobiAPI = HuobiAPI(self._api_key, self._api_secret,
                                  self._acct_id, self._proxies)

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._huobiAPI.get_timestamp()
            if res['status'] == 'ok':
                return int(res['data'])
            raise Exception(res)
        except Exception as err:
            raise HuobiException(err)
