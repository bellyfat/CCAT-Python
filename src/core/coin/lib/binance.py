# -*- coding: utf-8 -*-

# Binance class
# URL https://python-binance.readthedocs.io/en/latest/overview.html

import json
import logging
import math

import requests
from binance.client import Client
from binance.exceptions import (BinanceAPIException, BinanceOrderException,
                                BinanceRequestException,
                                BinanceWithdrawException)

from src.core.coin.coin import Coin
from src.core.util.exceptions import BinanceException


class Binance(Coin):

    def __init__(self, exchange, api_key, api_secret, proxies=None):
        super(Binance, self).__init__(exchange, api_key, api_secret, proxies)
        self._client = Client(api_key, api_secret, {
                              "proxies": proxies, "verify": False, "timeout": 20})
        self._client.session.close()

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._client = Client(self._api_key, self._api_secret, {
                              "proxies": self._proxies, "verify": False, "timeout": 20})
        self._client.session.close()

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._client.get_server_time()  # UTC Zone UnixStamp
            self._client.session.close()
            return res["serverTime"]
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
    def getSymbolsLimits(self, fSymbol, tSymbol, **kwargs):
        try:
            base = self._client.get_symbol_info(fSymbol + tSymbol)
            self._client.session.close()
            tSymbol_price_precision = math.pow(10, -int(base["baseAssetPrecision"]))
            fSymbol_size_precision = math.pow(10, -int(base["quotePrecision"]))
            for b in base["filters"]:
                if b["filterType"] == "PRICE_FILTER":
                    tSymbol_price_max = float(b["maxPrice"])
                    tSymbol_price_min = float(b["minPrice"])
                    tSymbol_price_step = float(b["tickSize"])
                if b["filterType"] == "LOT_SIZE":
                    fSymbol_size_max = float(b["maxQty"])
                    fSymbol_size_min = float(b["minQty"])
                    fSymbol_size_step = float(b["stepSize"])
            res={
                "tSymbol_price": {
                "precision": tSymbol_price_precision,
                "max": tSymbol_price_max,
                "min": tSymbol_price_min,
                "step": tSymbol_price_step
                },
                "fSymbol_size": {
                "precision": fSymbol_size_precision,
                "max": fSymbol_size_max,
                "min": fSymbol_size_min,
                "step": fSymbol_size_step
                }
            }
            return res
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            raise BinanceException

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, **kwargs):
        try:
            symbol = fSymbol+tSymbol
            timeStamp = self._client.get_server_time()
            ticker = self._client.get_orderbook_ticker(symbol=symbol)
            self._client.session.close()
            res = {
                "timeStamp" : timeStamp["serverTime"],
                "fSymbol" : fSymbol,
                "tSymbol" : tSymbol,
                "bid_one_price" : ticker["bidPrice"],
                "bid_one_pize" : ticker["bidQty"],
                "ask_one_price" : ticker["askPrice"],
                "ask_one_pize" : ticker["askQty"]
            }
            return res
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            raise BinanceException

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit=100, **kwargs):
        try:
            symbol = fSymbol+tSymbol
            res = self._client.get_order_book(symbol=symbol, limit=limit)
            self._client.session.close()
            return res
        except (BinanceAPIException, BinanceRequestException, BinanceOrderException, BinanceWithdrawException):
            raise BinanceException

    # a specific symbols kline/candlesticks
    def getMarketKline(self, fSymbol, tSymbol, **kwargs):
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
    def createOrder(self, fSymbol, tSymbol, quantity, price, type="limit", **kwargs):
        pass

    # check orders done or undone
    def checkOrder(self, fSymbol, tSymbol, orderID, **kwargs):
        pass

    # cancle the specific orders
    def cancleOrder(self, fSymbol, tSymbol, orderID, **kwargs):
        pass
