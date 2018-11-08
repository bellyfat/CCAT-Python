# -*- coding: utf-8 -*-

# Binance class
# URL https://python-binance.readthedocs.io/en/latest/overview.html

import logging
import json
import requests
from src.core.coin.coin import Coin
from src.core.util.exceptions import BinanceException
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException

class Binance(Coin):

    def __init__(self, exchange, api_key, api_secret, proxies=None):
        super(Binance, self).__init__(exchange, api_key, api_secret, proxies)
        self._client = Client(api_key, api_secret, {"proxies": proxies, "verify": False, "timeout": 20})
        self._client.session.close()

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._client = Client(self._api_key, self._api_secret, {"proxies": self._proxies, "verify": False, "timeout": 20})
        self._client.session.close()

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._client.get_server_time() # UTC Zone UnixStamp
            self._client.session.close()
            return res
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            raise BinanceException

    # perseconds qurry and orders rate limits
    def getServerLimits(self):
        try:
            res = self._client.get_exchange_info()
            self._client.session.close()
            return res["rateLimits"]
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            raise BinanceException

    # all symbols in pairs list baseSymbol quoteSymbol
    # def getServerSymbols(self):
    #     try:
    #         res = self._client.get_exchange_info()
    #         self._client.session.close()
    #         return res["symbols"]
    #     except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
    #         raise BinanceException
    def getServerSymbols(self):
        # not all api defined, get form cryptoCompare
        try:
            querry = "https://min-api.cryptocompare.com/data/all/exchanges"
            res = requests.request("GET", querry)
            if res.status_code == requests.codes.ok:
                return res.json()["Binance"]
            else:
                raise BinanceException
        except requests.exceptions.RequestException:
            raise BinanceException



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
