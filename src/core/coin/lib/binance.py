# -*- coding: utf-8 -*-

# Binance class
# URL https://python-binance.readthedocs.io/en/latest/overview.html

import logging
import json
from src.core.coin.coin import Coin
from src.core.util.exceptions import BinanceException
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException

class Binance(Coin):

    def __init__(self, exchange, api_key, api_secret, proxies=''):
        super(Binance, self).__init__(exchange, api_key, api_secret, proxies)
        if self._proxies != '':
            self._restAPI = Client(self._api_key, self._api_secret, {
                                   "proxies": self._proxies, "verify": False, "timeout": 20})
        else:
            self._restAPI = Client(self._api_key, self._api_secret, {
                                   "verify": False, "timeout": 20})
        self._restAPI.session.close()

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._restAPI = Client(self._api_key, self._api_secret, {
                               "proxies": self._proxies, "verify": False, "timeout": 20})
        self._restAPI.session.close()

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._restAPI.get_server_time()
            self._restAPI.session.close()
            return res
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            # log BinanceException
            pass


    # perseconds qurry and orders rate limits
    def getServerLimits(self, **kwargs):
        try:
            return self._restAPI.getget_exchange_info()
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            # log BinanceException
            pass

    # all symbols in pairs list baseSymbol quoteSymbol
    def getSymbols(self, **kwargs):
        try:
            return self._restAPI.getget_exchange_info()
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            # log BinanceException
            pass

    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self, symbol, **kwargs):
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
