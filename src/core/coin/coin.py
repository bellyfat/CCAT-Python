# -*- coding: utf-8 -*-

# coin class
# super class of all coins

from abc import ABCMeta, abstractmethod

class Coin(object):
    __metaclass__ = ABCMeta

    def __init__(self, exchange, api_key, api_secret, proxise=''):
        self._exchange = exchange
        self._api_key = api_keys
        self._api_secret = api_secret
        self._proxies = proxies

    # get config
    def getConfig(self):
        return {"exchange": self._exchange, "api_key": self._api_key, "api_secret": self._api_secret, "proxies": self._proxies}

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies

    @abstractmethod
    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        pass

    @abstractmethod
    # perseconds qurry and orders rate limits
    def getServerLimits(self):
        pass

    @abstractmethod
    # all symbols in pairs list baseSymbol quoteSymbol
    def getSymbols(self, **kwargs):
        pass

    @abstractmethod
    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self, symbol, **kwargs):
        pass

    @abstractmethod
    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, symbol, **kwargs):
        pass

    @abstractmethod
    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, symbol, **kwargs):
        pass

    @abstractmethod
    # a specific symbols kline/candlesticks
    def getMarketKline(self, symbol, **kwargs):
        pass

    @abstractmethod
    # get current trade
    def getTradeOpen(self, **kwargs):
        pass

    @abstractmethod
    # get history trade
    def getTradeHistory(self, **kwargs):
        pass

    @abstractmethod
    # get succeed trade
    def getTradeSucceed(self, **kwargs):
        pass

    @abstractmethod
    # get account all asset balance
    def getAccountBalances(self, **kwargs):
        pass

    @abstractmethod
    # get account asset balance
    def getAccountAssetBalance(self, asset, **kwargs):
        pass

    @abstractmethod
    # get account asset deposit and withdraw detail
    def getAccountAssetDetail(self, asset, **kwargs):
        pass

    # @abstractmethod
    # # withdraw account asset
    # def getAccountAssetWithDraw(self, asset, **kwargs):
    #     pass

    @abstractmethod
    # create orders default limit
    def createOrder(self, symbol, quantity, price, type="limit", **kwargs):
        pass

    @abstractmethod
    # check orders done or undone
    def checkOrder(self, symbol, orderID, **kwargs):
        pass

    @abstractmethod
    # cancle the specific orders
    def cancleOrder(self, symbol, orderID, **kwargs):
        pass
