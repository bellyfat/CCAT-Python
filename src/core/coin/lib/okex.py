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
        res = {
            "requests_second": 10,
            "orders_second": 10,
            "orders_day": 10 * 3600 * 24,
            "webSockets_second": 50
        }
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
    def getSymbolsLimits(self, fSymbol, tSymbol):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            base = self._spotAPI.get_coin_info(self._proxies)
            for b in base:
                if b["base_currency"] == fSymbol and b["quote_currency"] == tSymbol:
                    tSymbol_price_precision = float(b["tick_size"])
                    tSymbol_price_max = ''
                    tSymbol_price_min = float(b["tick_size"])
                    tSymbol_price_step = float(b["tick_size"])
                    fSymbol_size_precision = float(b["size_increment"])
                    fSymbol_size_max = ''
                    fSymbol_size_min = float(b["min_size"])
                    fSymbol_size_step = float(b["size_increment"])
                    min_notional = fSymbol_size_min * tSymbol_price_min
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
                        },
                        "min_notional": min_notional
                    }
                    return res
            raise OkexException
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol):
        try:
            ticker = self._spotAPI.get_depth(
                fSymbol + "-" + tSymbol, '1',  '', self._proxies)
            res = {
                "timeStamp": date_to_milliseconds(ticker["timestamp"]),
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_one_price": float(ticker["bids"][0][0]),
                "bid_one_size": float(ticker["bids"][0][1]),
                "ask_one_price": float(ticker["asks"][0][0]),
                "ask_one_size": float(ticker["asks"][0][1])
            }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit=''):
        '''
        {
            "timestamp": "2016-12-08T20:09:05.508883Z",

            "bids": [
                [ price, size, num_orders ],
                [ "295.96", "4.39088265", 2 ],
                ...
            ],
            "asks": [
                [ price, size, num_orders ],
                [ "295.97", "25.23542881", 12 ],
                ...
            ]
        }
        '''
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
    def getMarketKline(self, fSymbol, tSymbol, interval, start, end):
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
            granularity = int(interval_to_milliseconds(interval) / 1000)
            kline = self._spotAPI.get_kline(
                instrument_id, start, end, granularity, self._proxies)
            return kline
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get symbol trade fees
    def getTradeFees(self):
        '''
        币币手续费： 挂单成交0.1%， 吃单成交0.15%
        '''
        res = [{
            "symbol": "all",
            "maker": 0.001,
            "taker": 0.0015
        }]
        return res

    # get current trade
    def getTradeOpen(self, fSymbol='', tSymbol='', ratio='', froms='', to='', limit='100'):
        try:
            instrument_id = ''
            if fSymbol and tSymbol:
                instrument_id = fSymbol + "-" + tSymbol
            orders = self._spotAPI.get_orders_pending(
                instrument_id, froms, to, limit, self._proxies)
            res = []
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            for item in orders[0]:
                ask_or_bid = "ask" if item["side"] == "buy" else "bid"
                filled_price = float(item["filled_size"]) if float(item["filled_size"]) == 0 else float(
                    item["filled_notional"]) / float(item["filled_size"])
                res.append({
                    "timeStamp": date_to_milliseconds(item["timestamp"]),
                    "order_id": item["order_id"],
                    "status": "open",
                    "type": item["type"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": ask_or_bid,
                    "ask_bid_price": float(item["price"]),
                    "ask_bid_size": float(item["size"]),
                    "filled_price": filled_price,
                    "filled_size": float(item["filled_size"]),
                    "fee": float(ratio) * float(item["filled_notional"])
                })
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get history trade
    def getTradeHistory(self, fSymbol, tSymbol, ratio='', froms='', to='', limit='100'):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            orders = self._spotAPI.get_orders_list(
                "all", instrument_id, froms, to, limit, self._proxies)
            res = []
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            for item in orders[0]:
                ask_or_bid = "ask" if item["side"] == "buy" else "bid"
                filled_price = float(item["filled_size"]) if float(item["filled_size"]) == 0 else float(
                    item["filled_notional"]) / float(item["filled_size"])
                res.append({
                    "timeStamp": date_to_milliseconds(item["timestamp"]),
                    "order_id": item["order_id"],
                    "status": item["status"],
                    "type": item["type"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": ask_or_bid,
                    "ask_bid_price": float(item["price"]),
                    "ask_bid_size": float(item["size"]),
                    "filled_price": filled_price,
                    "filled_size": float(item["filled_size"]),
                    "fee": float(ratio) * float(item["filled_notional"])
                })
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get succeed trade
    def getTradeSucceed(self, fSymbol, tSymbol, ratio='', froms='', to='', limit='100'):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            orders = self._spotAPI.get_orders_list(
                "filled", instrument_id, froms, to, limit, self._proxies)
            res = []
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            for item in orders[0]:
                ask_or_bid = "ask" if item["side"] == "buy" else "bid"
                filled_price = float(item["filled_size"]) if float(item["filled_size"]) == 0 else float(
                    item["filled_notional"]) / float(item["filled_size"])
                res.append({
                    "timeStamp": date_to_milliseconds(item["timestamp"]),
                    "order_id": item["order_id"],
                    "status": item["status"],
                    "type": item["type"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": ask_or_bid,
                    "ask_bid_price": float(item["price"]),
                    "ask_bid_size": float(item["size"]),
                    "filled_price": filled_price,
                    "filled_size": float(item["filled_size"]),
                    "fee": float(ratio) * float(item["filled_notional"])
                })
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get account all asset balance
    def getAccountBalances(self, **kwargs):
        try:
            base = self._spotAPI.get_account_info(self._proxies)
            res = []
            for b in base:
                res.append({
                    "asset": b["currency"],
                    "balance": float(b["balance"]),
                    "free": float(b["available"]),
                    "locked": float(b["frozen"])
                })
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get account asset deposit and withdraw limits
    def getAccountLimits(self, **kwargs):
        try:
            base = self._accountAPI.get_currencies(self._proxies)
            res = []
            for b in base:
                if "min_withdrawal" in b.keys():
                    res.append({
                        "asset": b["currency"],
                        "can_deposite": str(b["can_deposit"]) in ["true", "True", "1"],
                        "can_withdraw": str(b["can_withdraw"]) in ["true", "True", "1"],
                        "min_withdraw": float(b["min_withdrawal"])
                    })
                else:
                    res.append({
                        "asset": b["currency"],
                        "can_deposite": str(b["can_deposit"]) in ["true", "True", "1"],
                        "can_withdraw": str(b["can_withdraw"]) in ["true", "True", "1"],
                        "min_withdraw": 0.0
                    })
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get account asset balance
    def getAccountAssetBalance(self, asset, **kwargs):
        try:
            base = self._spotAPI.get_coin_account_info(asset, self._proxies)
            res = {
                "asset": base["currency"],
                "balance": float(base["balance"]),
                "free": float(base["available"]),
                "locked": float(base["frozen"])
            }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset, **kwargs):
        try:
            res = self._spotAPI.get_ledger_record(asset, '', self._proxies)
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # create orders default limit
    def createOrder(self, fSymbol, tSymbol, ask_or_bid, price, quantity, ratio='', type="limit"):
        #  for speed up, lib not check, check from local db.data
        try:
            instrument_id = fSymbol + "-" + tSymbol
            side = 'buy' if ask_or_bid == "ask" else 'sell'
            base = self._spotAPI.take_order(
                type, side, instrument_id, quantity, 1, '', price, '', self._proxies)
            order_id = base["order_id"]
            info = self._spotAPI.get_order_info(
                order_id, instrument_id, self._proxies)
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            ask_or_bid = "ask" if info["side"] == "buy" else "bid"
            filled_price = float(info["filled_size"]) if float(info["filled_size"]) == 0 else float(
                info["filled_notional"]) / float(info["filled_size"])
            res = {
                "timeStamp": date_to_milliseconds(info["timestamp"]),
                "order_id": info["order_id"],
                "status": info["status"],
                "type": info["type"],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": ask_or_bid,
                "ask_bid_price": float(info["price"]),
                "ask_bid_size": float(info["size"]),
                "filled_price": filled_price,
                "filled_size": float(info["filled_size"]),
                "fee": float(ratio) * float(info["filled_notional"])
            }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # check orders done or undone
    def checkOrder(self, fSymbol, tSymbol, orderID, ratio='', **kwargs):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            info = self._spotAPI.get_order_info(
                orderID, instrument_id, self._proxies)
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            ask_or_bid = "ask" if info["side"] == "buy" else "bid"
            filled_price = float(info["filled_size"]) if float(info["filled_size"]) == 0 else float(
                info["filled_notional"]) / float(info["filled_size"])
            res = {
                "timeStamp": date_to_milliseconds(info["timestamp"]),
                "order_id": info["order_id"],
                "status": info["status"],
                "type": info["type"],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": ask_or_bid,
                "ask_bid_price": float(info["price"]),
                "ask_bid_size": float(info["size"]),
                "filled_price": filled_price,
                "filled_size": float(info["filled_size"]),
                "fee": float(ratio) * float(info["filled_notional"])
            }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # cancle the specific order
    def cancleOrder(self, fSymbol, tSymbol, orderID, **kwargs):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            info = self._spotAPI.get_order_info(
                orderID, instrument_id, self._proxies)
            if info["status"] == "open" or info["status"] == "part_filled":
                base = self._spotAPI.revoke_order(
                    orderID, instrument_id, self._proxies)
                if base["result"] == True:
                    res = {
                        "order_id": orderID,
                        "status": "cancled"
                    }
            else:
                res = {
                    "order_id": orderID,
                    "status": info["status"]
                }
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # cancle the bathch orders
    def cancleBatchOrder(self, fSymbol, tSymbol, orderIDs, **kwargs):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            res = []
            for orderID in orderIDs:
                info = self._spotAPI.get_order_info(
                    orderID, instrument_id, self._proxies)
                if info["status"] == "open" or info["status"] == "part_filled":
                    base = self._spotAPI.revoke_order(
                        orderID, instrument_id, self._proxies)
                    if base["result"] == True:
                        res.append({
                            "order_id": orderID,
                            "status": "cancled"
                        })
                else:
                    res.append({
                        "order_id": orderID,
                        "status": info["status"]
                    })
            return res
        except (OkexAPIException, OkexRequestException, OkexParamsException):
            raise OkexException

    # deposite asset balance
    def depositeAsset(self, asset, **kwargs):
        pass

    # withdraw asset balance
    def withdrawAsset(self, asset, **kwargs):
        pass
