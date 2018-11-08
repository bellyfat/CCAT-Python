# -*- coding: utf-8 -*-

# Okex Class

import logging
import json
from src.core.coin.coin import Coin
from src.core.coin.lib.okex_v3_api.client import Client
from src.core.coin.lib.okex_v3_api.account_api import AccountAPI
from src.core.coin.lib.okex_v3_api.spot_api import SpotAPI
from src.core.util.exceptions import OkexException

class Okex(Coin):

    def __init__(self, exchange, api_key, api_secret, passphrase, proxies=None):
        super(Okex, self).__init__(exchange, api_key, api_secret, proxies)
        self._restClientAPI = OkexClient(self._api_key, self._api_secret, self.proxies)
        self.AccountAPI = OkexTradeClient(self._api_key, self._api_secret, self.proxies)
        SpotAPI(api_key, seceret_key, passphrase, True)

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        pass

    # perseconds qurry and orders rate limits
    def getServerLimits(self):
        try:
            res = self._restAPI.get_exchange_info()
            self._restAPI.session.close()
            return res["rateLimits"]
        except (OkexAPIException, OkexRequestException, OkexOrderException, OkexWithdrawException):
            raise OkexException

    # all symbols in pairs list baseSymbol quoteSymbol
    def getServerSymbols(self):
        try:
            res = self._restAPI.get_exchange_info()
            self._restAPI.session.close()
            return res["symbols"]
        except (OkexAPIException, OkexRequestException, OkexOrderException, OkexWithdrawException):
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
