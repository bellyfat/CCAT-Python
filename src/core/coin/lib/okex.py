# -*- coding: utf-8 -*-

# Okex Class

import json

import requests

from src.core.coin.coin import Coin
from src.core.coin.lib.okex_v3_api.account_api import AccountAPI
from src.core.coin.lib.okex_v3_api.client import Client
from src.core.coin.lib.okex_v3_api.exceptions import (OkexAPIException,
                                                      OkexParamsException,
                                                      OkexRequestException)
from src.core.coin.lib.okex_v3_api.spot_api import SpotAPI
from src.core.util.exceptions import OkexException
from src.core.util.helper import date_to_milliseconds, interval_to_milliseconds


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
    def getServerTime(self):
        try:
            res = self._client._get_timestamp(self._proxies)
            return date_to_milliseconds(res)
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
    def getSymbolsLimits(self, fSymbol, tSymbol, **kwargs):
        try:
            base = self._spotAPI.get_coin_info(self._proxies)
            for b in base:
                if b["base_currency"] == fSymbol and b["quote_currency"] == tSymbol:
                    tSymbol_price_precision = float(b["quote_increment"])
                    tSymbol_price_max = None
                    tSymbol_price_min = None
                    tSymbol_price_step = float(b["quote_increment"])
                    fSymbol_size_precision = float(b["base_increment"])
                    fSymbol_size_max = None
                    fSymbol_size_min = float(b["base_min_size"])
                    fSymbol_size_step = float(b["base_increment"])
                    res = {
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
            raise OkexException
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, **kwargs):
        try:
            ticker = self._spotAPI.get_depth(
                fSymbol + "-" + tSymbol, '1',  '', self._proxies)
            res = {
                "timeStamp": date_to_milliseconds(ticker["timestamp"]),
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_one_price": ticker["bids"][0][0],
                "bid_one_pize": ticker["bids"][0][1],
                "ask_one_price": ticker["asks"][0][0],
                "ask_one_pize": ticker["asks"][0][1]
            }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit='', **kwargs):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            ticker = self._spotAPI.get_depth(
                instrument_id, limit,  '', self._proxies)
            res = {
                "timeStamp": date_to_milliseconds(ticker["timestamp"]),
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_price_size": ticker["bids"],
                "ask_price_size": ticker["asks"]
            }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # a specific symbols kline/candlesticks
    def getMarketKline(self, fSymbol, tSymbol, interval, start, end, **kwargs):
        '''
        [
            {
            "close":7071.1913,
            "high":7072.7999,
            "low":7061.7,
            "open":7067.9008,
            "time":"2018-08-05T10:00:00Z",
            "volume":68.4532745
            }
        ]
        '''
        try:
            instrument_id = fSymbol + "-" + tSymbol
            granularity = int(interval_to_milliseconds(interval)/1000)
            kline = self._spotAPI.get_kline(
                instrument_id, start, end, granularity, self._proxies)
            return kline
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

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
