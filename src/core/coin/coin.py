# -*- coding: utf-8 -*-

# coin class
# super class of all coins

from abc import ABCMeta, abstractmethod


class Coin(object):
    __metaclass__ = ABCMeta

    def __init__(self, exchange, api_key, api_secret, proxies):
        self._exchange = exchange
        self._api_key = api_key
        self._api_secret = api_secret
        self._proxies = proxies

    # get config
    def getConfig(self):
        return {
            "exchange": self._exchange,
            "api_key": self._api_key,
            "api_secret": self._api_secret,
            "proxies": self._proxies
        }

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
    def getServerSymbols(self):
        pass

    @abstractmethod
    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self):
        pass

    @abstractmethod
    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, aggDepth):
        pass

    @abstractmethod
    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit):
        pass

    @abstractmethod
    # a specific symbols kline/candlesticks
    def getMarketKline(self, fSymbol, tSymbol, interval, start, end):
        pass

    @abstractmethod
    # get symbol trade fees
    def getTradeFees(self):
        pass

    @abstractmethod
    # get current trade
    def getTradeOpen(self, fSymbol, tSymbol, limit, ratio):
        pass

    @abstractmethod
    # get history trade
    def getTradeHistory(self, fSymbol, tSymbol, froms, to, limit, ratio):
        pass

    @abstractmethod
    # get succeed trade
    def getTradeSucceed(self, fSymbol, tSymbol, froms, to, limit, ratio):
        pass

    @abstractmethod
    # get account all asset balance
    def getAccountBalances(self):
        pass

    @abstractmethod
    # get account asset deposit and withdraw limis
    def getAccountLimits(self):
        pass

    @abstractmethod
    # get account asset balance
    def getAccountAssetBalance(self, asset):
        pass

    @abstractmethod
    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset):
        pass

    @abstractmethod
    # create orders default limit
    def createOrder(self, fSymbol, tSymbol, ask_or_bid, price, quantity, ratio,
                    type):
        pass

    @abstractmethod
    # check orders done or undone
    def checkOrder(self, fSymbol, tSymbol, orderID, ratio):
        pass

    @abstractmethod
    # cancle the specific order
    def cancleOrder(self, fSymbol, tSymbol, orderID):
        pass

    @abstractmethod
    # cancle the batch orders
    def cancleBatchOrder(self, fSymbol, tSymbol, orderIDs):
        pass

    @abstractmethod
    # deposite asset balance
    def depositeAsset(self, asset):
        pass

    @abstractmethod
    # withdraw asset balance
    def withdrawAsset(self, asset):
        pass
