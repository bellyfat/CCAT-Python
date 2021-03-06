# -*- coding: utf-8 -*-

# Okex Class

import json
from decimal import ROUND_DOWN, ROUND_HALF_UP, ROUND_UP, Decimal

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from src.core.coin.coin import Coin
from src.core.coin.enums import *
from src.core.coin.lib.okex_v3_api.account_api import AccountAPI
from src.core.coin.lib.okex_v3_api.client import Client
from src.core.coin.lib.okex_v3_api.exceptions import (OkexAPIException,
                                                      OkexParamsException,
                                                      OkexRequestException)
from src.core.coin.lib.okex_v3_api.spot_api import SpotAPI
from src.core.util.exceptions import OkexException
from src.core.util.helper import (date_to_milliseconds,
                                  interval_to_milliseconds, num_to_precision)


class Okex(Coin):

    __STATUS = {
        "ordering": CCAT_ORDER_STATUS_ORDERING,
        "canceling": CCAT_ORDER_STATUS_CANCELING,
        "open": CCAT_ORDER_STATUS_OPEN,
        "part_filled": CCAT_ORDER_STATUS_PART_FILLED,
        "filled": CCAT_ORDER_STATUS_FILLED,
        "cancelled": CCAT_ORDER_STATUS_CANCELED
    }

    __TYPE = {"limit": CCAT_ORDER_TYPE_LIMIT, "market": CCAT_ORDER_TYPE_MARKET}

    __SIDE = {"buy": CCAT_ORDER_SIDE_BUY, "sell": CCAT_ORDER_SIDE_SELL}

    def __init__(self, exchange, api_key, api_secret, passphrase,
                 proxies=None):
        super(Okex, self).__init__(exchange, api_key, api_secret, proxies)
        self._passphrase = passphrase
        self._client = Client(api_key, api_secret, passphrase, False)
        self._accountAPI = AccountAPI(api_key, api_secret, passphrase, False)
        self._spotAPI = SpotAPI(api_key, api_secret, passphrase, False)

    # get config
    def getConfig(self):
        return {
            "exchange": self._exchange,
            "api_key": self._api_key,
            "api_secret": self._api_secret,
            "passphrase": self._passphrase,
            "proxies": self._proxies
        }

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._client._get_timestamp(self._proxies)
            return date_to_milliseconds(res)
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getServerTime: exception err=%s" % err
            raise OkexException(errStr)

    # per seconds qurry and orders rate limits
    def getServerLimits(self):
        '''
        REST API
            如果传入有效的API key 用user id限速；如果没有则拿公网IP限速。
            限速规则：一般接口限速6次/秒。其中币币API包含accounts的接口，所有接口的总访问频率不能超过10次/秒；币币API包含orders的接口，所有接口的总访问频率不能超过10次/秒。
        WebSocket
            WebSocket将每个命令类型限制为每秒50条命令。
        '''
        res = {
            "info_second": 5,
            "market_second": 10,
            "orders_second": 10,
            "webSockets_second": ''
        }
        return res

    # all symbols in pairs list baseSymbol quoteSymbol
    def getServerSymbols(self):
        try:
            base = self._spotAPI.get_coin_info(self._proxies)
            fSymbol = ''
            tSymbol = ''
            res = []
            for b in base:
                fSymbol = b["base_currency"]
                tSymbol = b["quote_currency"]
                res.append({"fSymbol": fSymbol, "tSymbol": tSymbol})
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getServerSymbols: exception err=%s" % err
            raise OkexException(errStr)

    # def getServerSymbols(self):
    #     # not all api defined, get form cryptoCompare
    #     try:
    #         querry = "https://min-api.cryptocompare.com/data/all/exchanges"
    #         res = requests.request("GET", querry)
    #         if res.status_code == requests.codes.ok:
    #             return res.json()["OKEX"]
    #         else:
    #             raise OkexException(err)
    #     except requests.exceptions.RequestException:
    #         raise OkexException(err)

    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self):
        try:
            base = self._spotAPI.get_coin_info(self._proxies)
            fSymbol = ''
            tSymbol = ''
            tSymbol_price_precision = ''
            tSymbol_price_max = ''
            tSymbol_price_min = ''
            tSymbol_price_step = ''
            fSymbol_size_precision = ''
            fSymbol_size_max = ''
            fSymbol_size_min = ''
            fSymbol_size_step = ''
            min_notional = ''
            res = []
            for b in base:
                fSymbol = b["base_currency"]
                tSymbol = b["quote_currency"]
                tSymbol_price_precision = float(b["tick_size"])
                tSymbol_price_max = ''
                tSymbol_price_min = float(b["tick_size"])
                tSymbol_price_step = float(b["tick_size"])
                fSymbol_size_precision = float(b["size_increment"])
                fSymbol_size_max = ''
                fSymbol_size_min = float(b["min_size"])
                fSymbol_size_step = float(b["size_increment"])
                min_notional = tSymbol_price_min * fSymbol_size_min
                res.append({
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
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
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getSymbolsLimits: exception err=%s" % err
            raise OkexException(errStr)

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, aggDepth=0):
        try:
            base = self._spotAPI.get_depth(fSymbol + "-" + tSymbol, '200', '',
                                           self._proxies)
            if not len(base["bids"]) > 0 or not len(base["asks"]) > 0:
                raise Exception(base)
            if aggDepth == 0:
                res = {
                    "timeStamp": date_to_milliseconds(base["timestamp"]),
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": float(base["bids"][0][0]),
                    "bid_one_size": float(base["bids"][0][1]),
                    "ask_one_price": float(base["asks"][0][0]),
                    "ask_one_size": float(base["asks"][0][1])
                }
            else:
                # calc bids
                aggPrice = num_to_precision(
                    float(base["bids"][0][0]),
                    float(aggDepth),
                    rounding=ROUND_DOWN)
                bid_one_price = float(aggPrice)
                bid_one_size = 0.0
                for bid in base["bids"]:
                    if float(bid[0]) < float(aggPrice):
                        break
                    bid_one_size = bid_one_size + float(bid[1])
                # calc asks
                aggPrice = num_to_precision(
                    float(base["asks"][0][0]),
                    float(aggDepth),
                    rounding=ROUND_UP)
                ask_one_price = float(aggPrice)
                ask_one_size = 0.0
                for ask in base["asks"]:
                    if float(ask[0]) > float(aggPrice):
                        break
                    ask_one_size = ask_one_size + float(ask[1])
                res = {
                    "timeStamp": date_to_milliseconds(base["timestamp"]),
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": bid_one_price,
                    "bid_one_size": bid_one_size,
                    "ask_one_price": ask_one_price,
                    "ask_one_size": ask_one_size
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getMarketOrderbookTicker: { fSymbol=%s, tSymbol=%s, aggDepth=%s }, exception err=%s" % (
                fSymbol, tSymbol, aggDepth, err)
            raise OkexException(errStr)

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
            ticker = self._spotAPI.get_depth(instrument_id, limit, '',
                                             self._proxies)
            res = {
                "timeStamp": date_to_milliseconds(ticker["timestamp"]),
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_price_size": ticker["bids"],
                "ask_price_size": ticker["asks"]
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getMarketOrderbookDepth: { fSymbol=%s, tSymbol=%s, limit=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, err)
            raise OkexException(errStr)

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
            kline = self._spotAPI.get_kline(instrument_id, start, end,
                                            granularity, self._proxies)
            res = []
            for k in kline:
                res.append({
                    "timeStamp": date_to_milliseconds(k["time"]),
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "open": k["open"],
                    "high": k["high"],
                    "low": k["low"],
                    "close": k["close"],
                    "volume": k["volume"]
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getMarketKline: { fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s }, exception err=%s" % (
                fSymbol, tSymbol, interval, start, end, err)
            raise OkexException(errStr)

    # get symbol trade fees
    def getTradeFees(self):
        '''
        币币手续费： 挂单成交0.1%， 吃单成交0.15%
        '''
        res = [{"symbol": "all", "maker": 0.001, "taker": 0.0015}]
        return res

    # get current trade
    def getTradeOpen(self, fSymbol='', tSymbol='', limit='100', ratio=''):
        try:
            instrument_id = ''
            if fSymbol != '' and tSymbol != '':
                instrument_id = fSymbol + "-" + tSymbol
            orders = self._spotAPI.get_orders_pending(instrument_id, '', '',
                                                      limit, self._proxies)
            res = []
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            for item in orders[0]:
                filled_price = float(item["filled_size"]) if float(
                    item["filled_size"]) == 0 else float(
                        item["filled_notional"]) / float(item["filled_size"])
                if not instrument_id:
                    fSymbol = item["instrument_id"].split('-')[0].upper()
                    tSymbol = item["instrument_id"].split('-')[1].upper()
                res.append({
                    "timeStamp":
                    date_to_milliseconds(item["timestamp"]),
                    "order_id":
                    item["order_id"],
                    "status":
                    CCAT_ORDER_STATUS_OPEN,
                    "type":
                    self.__TYPE[item["type"]],
                    "fSymbol":
                    fSymbol,
                    "tSymbol":
                    tSymbol,
                    "ask_or_bid":
                    self.__SIDE[item["side"]],
                    "ask_bid_price":
                    float(item["price"]),
                    "ask_bid_size":
                    float(item["size"]),
                    "filled_price":
                    filled_price,
                    "filled_size":
                    float(item["filled_size"]),
                    "fee":
                    float(ratio) * float(item["filled_notional"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getTradeOpen: { fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise OkexException(errStr)

    # get history trade
    def getTradeHistory(self, fSymbol, tSymbol, limit='100', ratio=''):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            orders = self._spotAPI.get_orders_list("all", instrument_id, '',
                                                   '', limit, self._proxies)
            res = []
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            for item in orders[0]:
                filled_price = float(item["filled_size"]) if float(
                    item["filled_size"]) == 0 else float(
                        item["filled_notional"]) / float(item["filled_size"])
                res.append({
                    "timeStamp":
                    date_to_milliseconds(item["timestamp"]),
                    "order_id":
                    item["order_id"],
                    "status":
                    self.__STATUS[item["status"]],
                    "type":
                    self.__TYPE[item["type"]],
                    "fSymbol":
                    fSymbol,
                    "tSymbol":
                    tSymbol,
                    "ask_or_bid":
                    self.__SIDE[item["side"]],
                    "ask_bid_price":
                    float(item["price"]),
                    "ask_bid_size":
                    float(item["size"]),
                    "filled_price":
                    filled_price,
                    "filled_size":
                    float(item["filled_size"]),
                    "fee":
                    float(ratio) * float(item["filled_notional"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getTradeHistory: { fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise OkexException(errStr)

    # get succeed trade
    def getTradeSucceed(self, fSymbol, tSymbol, limit='100', ratio=''):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            orders = self._spotAPI.get_orders_list("filled", instrument_id, '',
                                                   '', limit, self._proxies)
            res = []
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            for item in orders[0]:
                filled_price = float(item["filled_size"]) if float(
                    item["filled_size"]) == 0 else float(
                        item["filled_notional"]) / float(item["filled_size"])
                res.append({
                    "timeStamp":
                    date_to_milliseconds(item["timestamp"]),
                    "order_id":
                    item["order_id"],
                    "status":
                    self.__STATUS[item["status"]],
                    "type":
                    self.__TYPE[item["type"]],
                    "fSymbol":
                    fSymbol,
                    "tSymbol":
                    tSymbol,
                    "ask_or_bid":
                    self.__SIDE[item["side"]],
                    "ask_bid_price":
                    float(item["price"]),
                    "ask_bid_size":
                    float(item["size"]),
                    "filled_price":
                    filled_price,
                    "filled_size":
                    float(item["filled_size"]),
                    "fee":
                    float(ratio) * float(item["filled_notional"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getTradeSucceed: { fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise OkexException(errStr)

    # get account all asset balance
    def getAccountBalances(self):
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
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getAccountBalances: exception err=%s" % err
            raise OkexException(errStr)

    # get account all asset deposit and withdraw history
    def getAccountDetail(self):
        try:
            base = self._accountAPI.get_ledger_record(0, 10, 100, '', '',
                                                      self._proxies)
            assets = []
            for b in base[0]:
                if b["typename"] == 'deposit' or b["typename"] == 'withdrawal':
                    if b["currency"] not in assets:
                        assets.append(b["currency"])
            res = []
            for a in assets:
                deposit = []
                withdraw = []
                for b in base[0]:
                    if b['typename'] == 'deposit' and b["currency"] == a:
                        deposit.append(b)
                    if b['typename'] == 'withdrawal' and b["currency"] == a:
                        withdraw.append(b)
                res.append({
                    "asset": a,
                    "deposit": deposit,
                    "withdraw": withdraw
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getAccountDetail: exception err=%s" % err
            raise OkexException(errStr)

    # get account asset deposit and withdraw limits
    def getAccountLimits(self):
        try:
            base = self._accountAPI.get_currencies(self._proxies)
            res = []
            for b in base:
                if "min_withdrawal" in b.keys():
                    res.append({
                        "asset":
                        b["currency"],
                        "can_deposit":
                        str(b["can_deposit"]) in ["true", "True", "1"],
                        "can_withdraw":
                        str(b["can_withdraw"]) in ["true", "True", "1"],
                        "min_withdraw":
                        float(b["min_withdrawal"])
                    })
                else:
                    res.append({
                        "asset":
                        b["currency"],
                        "can_deposit":
                        str(b["can_deposit"]) in ["true", "True", "1"],
                        "can_withdraw":
                        str(b["can_withdraw"]) in ["true", "True", "1"],
                        "min_withdraw":
                        0.0
                    })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getAccountLimits: exception err=%s" % err
            raise OkexException(errStr)

    # get account asset balance
    def getAccountAssetBalance(self, asset):
        try:
            base = self._spotAPI.get_coin_account_info(asset, self._proxies)
            res = {
                "asset": base["currency"],
                "balance": float(base["balance"]),
                "free": float(base["available"]),
                "locked": float(base["frozen"])
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getAccountAssetBalance: { asset=%s }, exception err=%s" % (
                asset, err)
            raise OkexException(errStr)

    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset):
        try:
            asset = asset.lower()
            base = self._accountAPI.get_ledger_record(0, 10, 100, asset, '',
                                                      self._proxies)
            deposit = []
            withdraw = []
            for b in base[0]:
                if b['typename'] == 'deposit':
                    deposit.append(b)
                if b['typename'] == 'withdrawal':
                    withdraw.append(b)
            res = {}
            if deposit != [] or withdraw != []:
                res = {"deposit": deposit, "withdraw": withdraw}
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.getAccountAssetDetail: { asset=%s }, exception err=%s" % (
                asset, err)
            raise OkexException(errStr)

    # create orders default limit
    def createOrder(self,
                    fSymbol,
                    tSymbol,
                    ask_or_bid,
                    price,
                    quantity,
                    ratio='',
                    type="limit"):
        #  for speed up, lib not check, check from local db.data
        try:
            instrument_id = fSymbol + "-" + tSymbol
            side = 'buy' if ask_or_bid == CCAT_ORDER_SIDE_BUY else 'sell'
            base = self._spotAPI.take_order(type, side, instrument_id,
                                            quantity, 1, '', price, '',
                                            self._proxies)
            order_id = base["order_id"]
            info = self._spotAPI.get_order_info(order_id, instrument_id,
                                                self._proxies)
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            filled_price = float(info["filled_size"]) if float(
                info["filled_size"]) == 0 else float(
                    info["filled_notional"]) / float(info["filled_size"])
            res = {
                "timeStamp": date_to_milliseconds(info["timestamp"]),
                "order_id": info["order_id"],
                "status": self.__STATUS[info["status"]],
                "type": self.__TYPE[info["type"]],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": self.__SIDE[info["side"]],
                "ask_bid_price": float(info["price"]),
                "ask_bid_size": float(info["size"]),
                "filled_price": filled_price,
                "filled_size": float(info["filled_size"]),
                "fee": float(ratio) * float(info["filled_notional"])
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.createOrder: { fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, quantity=%s, ratio=%s, type=%s }, exception err=%s" % (
                fSymbol, tSymbol, ask_or_bid, price, quantity, ratio, type,
                err)
            raise OkexException(errStr)

    # check orders done or undone
    def checkOrder(self, orderID, fSymbol, tSymbol, ratio=''):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            info = self._spotAPI.get_order_info(orderID, instrument_id,
                                                self._proxies)
            if ratio == '':
                ratio = self.getTradeFees()[0]["taker"]
            filled_price = float(info["filled_size"]) if float(
                info["filled_size"]) == 0 else float(
                    info["filled_notional"]) / float(info["filled_size"])
            res = {
                "timeStamp": date_to_milliseconds(info["timestamp"]),
                "order_id": info["order_id"],
                "status": self.__STATUS[info["status"]],
                "type": self.__TYPE[info["type"]],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": self.__SIDE[info["side"]],
                "ask_bid_price": float(info["price"]),
                "ask_bid_size": float(info["size"]),
                "filled_price": filled_price,
                "filled_size": float(info["filled_size"]),
                "fee": float(ratio) * float(info["filled_notional"])
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.checkOrder: { orderID=%s, fSymbol=%s, tSymbol=%s, ratio=%s }, exception err=%s" % (
                orderID, fSymbol, tSymbol, ratio, err)
            raise OkexException(errStr)

    # cancel the specific order
    def cancelOrder(self, orderID, fSymbol, tSymbol):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            info = self._spotAPI.get_order_info(orderID, instrument_id,
                                                self._proxies)
            if info["status"] == "open" or info["status"] == "part_filled":
                base = self._spotAPI.revoke_order(orderID, instrument_id,
                                                  self._proxies)
                if base["result"] == True:
                    res = {
                        "order_id": orderID,
                        "status": CCAT_ORDER_STATUS_CANCELED
                    }
            else:
                res = {
                    "order_id": orderID,
                    "status": self.__STATUS[info["status"]]
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.cancelOrder: { orderID=%s, fSymbol=%s, tSymbol=%s }, exception err=%s" % (
                orderID, fSymbol, tSymbol, err)
            raise OkexException(errStr)

    # cancel the bathch orders
    def cancelBatchOrder(self, orderIDs, fSymbol, tSymbol):
        try:
            instrument_id = fSymbol + "-" + tSymbol
            res = []
            for orderID in orderIDs:
                info = self._spotAPI.get_order_info(orderID, instrument_id,
                                                    self._proxies)
                if info["status"] == "open" or info["status"] == "part_filled":
                    base = self._spotAPI.revoke_order(orderID, instrument_id,
                                                      self._proxies)
                    if base["result"] == True:
                        res.append({
                            "order_id": orderID,
                            "status": CCAT_ORDER_STATUS_CANCELED
                        })
                else:
                    res.append({
                        "order_id": orderID,
                        "status": self.__STATUS[info["status"]]
                    })
            return res
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.cancelBatchOrder: { orderIDs=%s, fSymbol=%s, tSymbol=%s }, exception err=%s" % (
                orderIDs, fSymbol, tSymbol, err)
            raise OkexException(errStr)

    # one click cancle all orders
    def oneClickCancleOrders(self):
        try:
            res = self.getTradeOpen()
            for r in res:
                b = self.cancelOrder(r['order_id'], r['fSymbol'], r['tSymbol'])
                if b['status'] != CCAT_ORDER_STATUS_CANCELED:
                    return False
            return True
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.oneClickCancleOrders: exception err=%s" % err
            raise OkexException(errStr)

    # one click trans all to baseCoin
    def oneClickTransToBaseCoin(self, baseCoin='USDT'):
        try:
            exceptionStr = []
            balance = self.getAccountBalances()
            symbol = self.getSymbolsLimits()
            deSet = []
            trSet = []
            # trSet -> deSet
            for b in balance:
                isIn = False
                if b['asset'] != baseCoin and b['free'] > 0:
                    for s in symbol:
                        if (baseCoin.upper(), b['asset']) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                        if (b['asset'], baseCoin.upper()) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                    if isIn == False:
                        for s in symbol:
                            if b['asset'] == s['fSymbol'] and isIn == False:
                                for sy in symbol:
                                    if (baseCoin.upper(), s['tSymbol']) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_SELL,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
                                    if (s['tSymbol'], baseCoin.upper()) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_SELL,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
                            if b['asset'] == s['tSymbol'] and isIn == False:
                                for sy in symbol:
                                    if (baseCoin.upper(), s['tSymbol']) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_BUY,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
                                    if (s['tSymbol'], baseCoin.upper()) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_BUY,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
            for tr in trSet:
                res = self.getMarketOrderbookDepth(tr['fSymbol'],
                                                   tr['tSymbol'], 100)
                sum = 0
                trTrade = []
                if tr['ask_or_bid'] == CCAT_ORDER_SIDE_BUY:
                    for r in res['ask_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        trBalanceSize = tr['balance'] / rprice
                        if sum < trBalanceSize:
                            trSize = min(trBalanceSize - sum, rSize)
                            if not trSize > 0:
                                continue
                            if not tr['limit_size_min'] == 'NULL':
                                if trSize < tr['limit_size_min']:
                                    continue
                            if not tr['limit_min_notional'] == 'NULL':
                                if rprice * trSize < tr['limit_min_notional']:
                                    continue
                            sum = sum + trSize
                            trTrade.append({'price': rprice, 'size': trSize})
                if tr['ask_or_bid'] == CCAT_ORDER_SIDE_SELL:
                    for r in res['bid_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        trBalanceSize = tr['balance']
                        if sum < trBalanceSize:
                            trSize = min(trBalanceSize - sum, rSize)
                            if not trSize > 0:
                                continue
                            if not tr['limit_size_min'] == 'NULL':
                                if trSize < tr['limit_size_min']:
                                    continue
                            if not tr['limit_min_notional'] == 'NULL':
                                if rprice * trSize < tr['limit_min_notional']:
                                    continue
                            sum = sum + trSize
                            trTrade.append({'price': rprice, 'size': trSize})
                for trade in trTrade:
                    price = num_to_precision(
                        trade['price'],
                        tr['limit_price_precision'],
                        rounding=ROUND_HALF_UP)
                    size = num_to_precision(
                        trade['size'],
                        tr['limit_size_precision'],
                        rounding=ROUND_DOWN)
                    if not float(size) > 0:
                        continue
                    if not tr['limit_size_min'] == 'NULL':
                        if float(size) < tr['limit_size_min']:
                            continue
                    if not tr['limit_min_notional'] == 'NULL':
                        if float(price) * float(
                                size) < tr['limit_min_notional']:
                            continue
                    try:
                        base = self.createOrder(
                            tr['fSymbol'], tr['tSymbol'], tr['ask_or_bid'],
                            str(price), str(size), 0, CCAT_ORDER_TYPE_LIMIT)
                    except Exception as err:
                        exceptionStr.append(err)
            # deSet -> baseCoin
            balance = self.getAccountBalances()
            for b in balance:
                isIn = False
                if b['asset'] != baseCoin and b['free'] > 0:
                    for s in symbol:
                        if (baseCoin.upper(), b['asset']) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                            deSet.append({
                                'fSymbol':
                                s['fSymbol'],
                                'tSymbol':
                                s['tSymbol'],
                                'balance':
                                float(b['free']),
                                'ask_or_bid':
                                CCAT_ORDER_SIDE_BUY,
                                'limit_price_precision':
                                "NULL" if s["tSymbol_price"]["precision"] == ''
                                else float(s["tSymbol_price"]["precision"]),
                                'limit_size_precision':
                                "NULL" if s["fSymbol_size"]["precision"] == ''
                                else float(s["fSymbol_size"]["precision"]),
                                'limit_size_min':
                                "NULL" if s["fSymbol_size"]["min"] == '' else
                                float(s["fSymbol_size"]["min"]),
                                'limit_min_notional':
                                "NULL" if s["min_notional"] == '' else float(
                                    s["min_notional"])
                            })
                        if (b['asset'], baseCoin.upper()) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                            deSet.append({
                                'fSymbol':
                                s['fSymbol'],
                                'tSymbol':
                                s['tSymbol'],
                                'balance':
                                float(b['free']),
                                'ask_or_bid':
                                CCAT_ORDER_SIDE_SELL,
                                'limit_price_precision':
                                "NULL" if s["tSymbol_price"]["precision"] == ''
                                else float(s["tSymbol_price"]["precision"]),
                                'limit_size_precision':
                                "NULL" if s["fSymbol_size"]["precision"] == ''
                                else float(s["fSymbol_size"]["precision"]),
                                'limit_size_min':
                                "NULL" if s["fSymbol_size"]["min"] == '' else
                                float(s["fSymbol_size"]["min"]),
                                'limit_min_notional':
                                "NULL" if s["min_notional"] == '' else float(
                                    s["min_notional"])
                            })
            for de in deSet:
                res = self.getMarketOrderbookDepth(de['fSymbol'],
                                                   de['tSymbol'], 100)
                sum = 0
                deTrade = []
                if de['ask_or_bid'] == CCAT_ORDER_SIDE_BUY:
                    for r in res['ask_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        deBalanceSize = de['balance'] / rprice
                        if sum < deBalanceSize:
                            deSize = min(deBalanceSize - sum, rSize)
                            if not deSize > 0:
                                continue
                            if not de['limit_size_min'] == 'NULL':
                                if deSize < de['limit_size_min']:
                                    continue
                            if not de['limit_min_notional'] == 'NULL':
                                if rprice * deSize < de['limit_min_notional']:
                                    continue
                            sum = sum + deSize
                            deTrade.append({'price': rprice, 'size': deSize})
                if de['ask_or_bid'] == CCAT_ORDER_SIDE_SELL:
                    for r in res['bid_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        deBalanceSize = de['balance']
                        if sum < deBalanceSize:
                            deSize = min(deBalanceSize - sum, rSize)
                            if not deSize > 0:
                                continue
                            if not de['limit_size_min'] == 'NULL':
                                if deSize < de['limit_size_min']:
                                    continue
                            if not de['limit_min_notional'] == 'NULL':
                                if rprice * deSize < de['limit_min_notional']:
                                    continue
                            sum = sum + deSize
                            deTrade.append({'price': rprice, 'size': deSize})
                for trade in deTrade:
                    price = num_to_precision(
                        trade['price'],
                        de['limit_price_precision'],
                        rounding=ROUND_HALF_UP)
                    size = num_to_precision(
                        trade['size'],
                        de['limit_size_precision'],
                        rounding=ROUND_DOWN)
                    if not float(size) > 0:
                        continue
                    if not de['limit_size_min'] == 'NULL':
                        if float(size) < de['limit_size_min']:
                            continue
                    if not de['limit_min_notional'] == 'NULL':
                        if float(price) * float(
                                size) < de['limit_min_notional']:
                            continue
                    try:
                        base = self.createOrder(
                            de['fSymbol'], de['tSymbol'], de['ask_or_bid'],
                            str(price), str(size), 0, CCAT_ORDER_TYPE_LIMIT)
                    except Exception as err:
                        exceptionStr.append(err)
            # check trans result
            if not exceptionStr == []:
                raise Exception(exceptionStr)
            balance = self.getAccountBalances()
            for b in balance:
                isIn = False
                if b['asset'] != baseCoin and b['free'] > 0:
                    for s in symbol:
                        if (b['asset'],
                                'USDT') == (s['fSymbol'],
                                            s['tSymbol']) and isIn == False:
                            isIn = True
                            res = self.getMarketOrderbookDepth(
                                s['fSymbol'], s['tSymbol'], 10)
                            if float(b['free']) * float(res['bid_price_size'][
                                    0][0]) > CCAT_BALANCE_SMALL_AMOUNT_USDT:
                                return False
                    if isIn == False:
                        for s in symbol:
                            if b['asset'] == s['fSymbol'] and isIn == False:
                                for sy in symbol:
                                    if (s['tSymbol'], 'USDT') == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        res = self.getMarketOrderbookDepth(
                                            s['fSymbol'], s['tSymbol'], 10)
                                        resy = self.getMarketOrderbookDepth(
                                            sy['fSymbol'], sy['tSymbol'], 10)
                                        if float(b['free']) * float(
                                                res['bid_price_size'][0]
                                            [0]) * float(
                                                resy['bid_price_size'][0][0]
                                            ) > CCAT_BALANCE_SMALL_AMOUNT_USDT:
                                            return False
            return True
        except (ReadTimeout, ConnectionError, KeyError, OkexAPIException,
                OkexRequestException, OkexParamsException, Exception) as err:
            errStr = "src.core.coin.okex.Okex.oneClickTransToBaseCoin: exception err=%s" % err
            raise OkexException(errStr)

    # deposit asset balance
    def depositAsset(self, asset):
        pass

    # withdraw asset balance
    def withdrawAsset(self, asset):
        pass
