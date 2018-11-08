# -*- coding: utf-8 -*-

# Okex Class

import json
import logging

from src.core.coin.coin import Coin
from src.core.coin.lib.okex_v3_api.account_api import AccountAPI
from src.core.coin.lib.okex_v3_api.client import Client
from src.core.coin.lib.okex_v3_api.exceptions import (OkexAPIException,
                                                      OkexParamsException,
                                                      OkexRequestException)
from src.core.coin.lib.okex_v3_api.spot_api import SpotAPI
from src.core.util.exceptions import OkexException


class Okex(Coin):

    def __init__(self, exchange, api_key, api_secret, passphrase, proxies=None):
        super(Okex, self).__init__(exchange, api_key, api_secret, proxies)
        self._passphrase = passphrase
        self._client = Client(api_key, api_secret, passphrase, True)
        self._accountAPI = AccountAPI(api_key, api_secret, passphrase, True)
        self._spotAPI = SpotAPI(api_key, api_secret, passphrase, True)

    # get config
    def getConfig(self):
        return {"exchange": self._exchange, "api_key": self._api_key, "api_secret": self._api_secret, "passphrase": self._passphrase, "proxies": self._proxies}

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self, proxies=None):
        try:
            res = self._client._get_timestamp(proxies)
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # perseconds qurry and orders rate limits
    def getServerLimits(self):
        '''
        REST API
            如果传入有效的API key 用user id限速；如果没有则拿公网IP限速。
            限速规则：一般接口限速6次/秒。其中币币API包含accounts的接口，所有接口的总访问频率不能超过10次/秒；币币API包含orders的接口，所有接口的总访问频率不能超过10次/秒。
        WebSocket
            WebSocket将每个命令类型限制为每秒50条命令。
        '''
        res = [{"RestAPI": {"user": "6 times per second", "all": "10 times per second"}},
               {"WebSocketAPI": "50 times per second"}]
        return res

    # all symbols in pairs list baseSymbol quoteSymbol
    def getServerSymbols(self):
        # not all api defined, get form cryptoCompare
        try:
            querry = "https://min-api.cryptocompare.com/data/all/exchanges"
            res = requests.request("GET", querry)
            if res.status_code == requests.codes.ok:
                return res.json()["OKEX"]
            else:
                raise OkexException
        except requests.exceptions.RequestException:
            raise OkexException

    # buy or sell a specific symbol's rate limits
    def getSymbolLimits(self, symbol, **kwargs):
        pass

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, symbol, **kwargs):
        pass

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, symbol, **kwargs):
        pass

    # a specific symbols kline/candlesticks
    def getMarketKline(self, symbol, **kwargs):
        pass

    # get current trade
    def getTradeOpen(self, **kwargs):
        pass

        # get history trade
    def getTradeHistory(self, **kwargs):
        pass

        # get succeed trade
    def getTradeSucceed(self, **kwargs):
        pass

    # get account all asset balance
    def getAccountBalances(self, **kwargs):
        pass

    # get account asset balance
    def getAccountAssetBalance(self, asset, **kwargs):
        pass

    # get account asset deposit and withdraw detail
    def getAccountAssetDetail(self, asset, **kwargs):
        pass

    # create orders default limit
    def createOrder(self, symbol, quantity, price, type="limit", **kwargs):
        pass

    # check orders done or undone
    def checkOrder(self, symbol, orderID, **kwargs):
        pass

    # cancle the specific orders
    def cancleOrder(self, symbol, orderID, **kwargs):
        pass
