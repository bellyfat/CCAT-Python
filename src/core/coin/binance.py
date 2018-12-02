# -*- coding: utf-8 -*-

# Binance class
# URL https://python-binance.readthedocs.io/en/latest/overview.html

import json
import math
from decimal import ROUND_DOWN, ROUND_UP, Decimal

import requests
import urllib3
from requests.exceptions import ConnectionError, ReadTimeout

from src.core.coin.coin import Coin
from src.core.coin.enums import *
from src.core.coin.lib.binance_api.client import Client
from src.core.coin.lib.binance_api.enums import *
from src.core.coin.lib.binance_api.exceptions import (BinanceAPIException,
                                                      BinanceOrderException,
                                                      BinanceRequestException,
                                                      BinanceWithdrawException)
from src.core.coin.lib.binance_api.helpers import date_to_milliseconds
from src.core.util.exceptions import BinanceException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Binance(Coin):

    __STATUS = {
        "PENDING_CANCEL": ORDER_STATUS_CANCELING,
        "NEW": ORDER_STATUS_OPEN,
        "PARTIALLY_FILLED": ORDER_STATUS_PART_FILLED,
        "FILLED": ORDER_STATUS_FILLED,
        "CANCELED": ORDER_STATUS_CANCELED
    }

    __TYPE = {"LIMIT": ORDER_TYPE_LIMIT, "MARKET": ORDER_TYPE_MARKET}

    __SIDE = {"BUY": ORDER_SIDE_BUY, "SELL": ORDER_SIDE_SELL}

    def __init__(self, exchange, api_key, api_secret, proxies=None):
        super(Binance, self).__init__(exchange, api_key, api_secret, proxies)
        self._client = Client(api_key, api_secret, {
            "proxies": proxies,
            "verify": False,
            "timeout": 20
        })

    def __del__(self):
        self._client.session.close()

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._client = Client(self._api_key, self._api_secret, {
            "proxies": proxies,
            "verify": False,
            "timeout": 20
        })

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._client.get_server_time()  # UTC Zone UnixStamp
            return res["serverTime"]
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # perseconds qurry and orders rate limits
    def getServerLimits(self):
        try:
            base = self._client.get_exchange_info()
            for b in base["rateLimits"]:
                if b["rateLimitType"] == "REQUEST_WEIGHT" and b[
                        "interval"] == "MINUTE":
                    requests_second = float(b["limit"]) / 60
                if b["rateLimitType"] == "ORDERS" and b["interval"] == "SECOND":
                    orders_second = float(b["limit"])
                if b["rateLimitType"] == "ORDERS" and b["interval"] == "DAY":
                    orders_day = float(b["limit"])
            res = {
                "info_second": requests_second,
                "market_second": requests_second,
                "orders_second": orders_second,
                "webSockets_second": ''
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # all symbols in pairs list baseSymbol quoteSymbol
    def getServerSymbols(self):
        try:
            base = self._client.get_exchange_info()["symbols"]
            res = []
            for b in base:
                fSymbol = b["baseAsset"]
                tSymbol = b["quoteAsset"]
                res.append({"fSymbol": fSymbol, "tSymbol": tSymbol})
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # def getServerSymbols(self):
    #     # not all api defined, get form cryptoCompare
    #     try:
    #         querry = "https://min-api.cryptocompare.com/data/all/exchanges"
    #         res = requests.request("GET", querry)
    #         if res.status_code == requests.codes.ok:
    #             return res.json()["Binance"]
    #         else:
    #             raise BinanceException(err)
    #     except requests.exceptions.RequestException:
    #         raise BinanceException(err)

    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self):
        try:
            info = self._client.get_exchange_info()["symbols"]
            fSymbol = ''
            tSymbol = ''
            tSymbol_price_precision = ''
            fSymbol_size_precision = ''
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
            for base in info:
                fSymbol = base["baseAsset"]
                tSymbol = base["quoteAsset"]
                tSymbol_price_precision = math.pow(
                    10, -int(base["baseAssetPrecision"]))
                fSymbol_size_precision = math.pow(10,
                                                  -int(base["quotePrecision"]))
                for b in base["filters"]:
                    if b["filterType"] == "PRICE_FILTER":
                        tSymbol_price_max = float(b["maxPrice"])
                        tSymbol_price_min = float(b["minPrice"])
                        tSymbol_price_step = float(b["tickSize"])
                    if b["filterType"] == "LOT_SIZE":
                        fSymbol_size_max = float(b["maxQty"])
                        fSymbol_size_min = float(b["minQty"])
                        fSymbol_size_step = float(b["stepSize"])
                    if b["filterType"] == "MIN_NOTIONAL":
                        min_notional = float(b["minNotional"])
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
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, aggDepth=''):
        try:
            if aggDepth != '':
                if float(aggDepth) > 1:
                    raise Exception("aggDepth must < 1.0")
            symbol = fSymbol + tSymbol
            timeStamp = self._client.get_server_time()["serverTime"]
            base = self._client.get_order_book(symbol=symbol, limit=100)
            if not 'lastUpdateId' in base.keys() or not len(
                    base["bids"]) > 0 or not len(base["asks"]) > 0:
                err = "{fSymbol=%s, tSymbol=%s, base=%s}" % (fSymbol, tSymbol,
                                                             base)
                raise BinanceException(err)
            if aggDepth == '':
                res = {
                    "timeStamp": timeStamp,
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": float(base["bids"][0][0]),
                    "bid_one_size": float(base["bids"][0][1]),
                    "ask_one_price": float(base["asks"][0][0]),
                    "ask_one_size": float(base["asks"][0][1])
                }
            else:
                # calc bids
                aggPrice = Decimal(base["bids"][0][0]).quantize(
                    Decimal(str(aggDepth)), rounding=ROUND_DOWN)
                bid_one_price = float(aggPrice)
                bid_one_size = 0.0
                for bid in base["bids"]:
                    if float(bid[0]) < float(aggPrice):
                        break
                    bid_one_size = bid_one_size + float(bid[1])
                # calc asks
                aggPrice = Decimal(base["asks"][0][0]).quantize(
                    Decimal(str(aggDepth)), rounding=ROUND_UP)
                ask_one_price = float(aggPrice)
                ask_one_size = 0.0
                for ask in base["asks"]:
                    if float(ask[0]) > float(aggPrice):
                        break
                    ask_one_size = ask_one_size + float(ask[1])
                res = {
                    "timeStamp": timeStamp,
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": bid_one_price,
                    "bid_one_size": bid_one_size,
                    "ask_one_price": ask_one_price,
                    "ask_one_size": ask_one_size
                }

            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit=100):
        try:
            symbol = fSymbol + tSymbol
            timeStamp = self._client.get_server_time()
            ticker = self._client.get_order_book(symbol=symbol, limit=limit)
            res = {
                "timeStamp": timeStamp["serverTime"],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_price_size": ticker["bids"],
                "ask_price_size": ticker["asks"]
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # a specific symbols kline/candlesticks
    def getMarketKline(self, fSymbol, tSymbol, interval, start, end=''):
        '''
        Returns
        [
            [
                1499040000000,      # Open time
                "0.01634790",       # Open
                "0.80000000",       # High
                "0.01575800",       # Low
                "0.01577100",       # Close
                "148976.11427815",  # Volume
                1499644799999,      # Close time
                "2434.19055334",    # Quote asset volume
                308,                # Number of trades
                "1756.87402397",    # Taker buy base asset volume
                "28.46694368",      # Taker buy quote asset volume
                "17928899.62484339" # Can be ignored
            ]
        ]
        '''
        try:
            symbol = fSymbol + tSymbol
            kline = self._client.get_historical_klines(symbol, interval, start,
                                                       end)
            res = []
            for k in kline:
                res.append({
                    "timeStamp": k[0],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "open": k[1],
                    "high": k[2],
                    "low": k[3],
                    "close": k[4],
                    "volume": k[5]
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get symbol trade fees
    def getTradeFees(self):
        try:
            res = self._client.get_trade_fee()
            return res["tradeFee"]
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get current trade
    def getTradeOpen(self, fSymbol='', tSymbol='', limit='100', ratio=''):
        try:
            if fSymbol and tSymbol:
                symbol = fSymbol + tSymbol
                orders = self._client.get_open_orders(symbol=symbol)
            else:
                orders = self._client.get_open_orders()
            if ratio == '':
                ratio = self._client.get_trade_fee(
                    symbol=symbol)["tradeFee"][0]["taker"]
            res = []
            for item in orders:
                filled_price = 0.0 if float(
                    item["executedQty"]) == 0 else float(
                        item["cummulativeQuoteQty"]) / float(item["executedQty"])
                res.append({
                    "timeStamp":
                    item["time"],
                    "order_id":
                    item["orderId"],
                    "status":
                    ORDER_STATUS_OPEN,
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
                    float(item["origQty"]),
                    "filled_price":
                    filled_price,
                    "filled_size":
                    float(item["executedQty"]),
                    "fee":
                    float(ratio) * float(item["cummulativeQuoteQty"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get history trade
    def getTradeHistory(self, fSymbol, tSymbol, limit='100', ratio=''):
        try:
            symbol = fSymbol + tSymbol
            orders = self._client.get_all_orders(symbol=symbol)
            if ratio == '':
                ratio = self._client.get_trade_fee(
                    symbol=symbol)["tradeFee"][0]["taker"]
            res = []
            for item in orders:
                filled_price = 0.0 if float(
                    item["executedQty"]) == 0 else float(
                        item["cummulativeQuoteQty"]) / float(
                            item["executedQty"])
                res.append({
                    "timeStamp":
                    item["time"],
                    "order_id":
                    item["orderId"],
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
                    float(item["origQty"]),
                    "filled_price":
                    filled_price,
                    "filled_size":
                    float(item["executedQty"]),
                    "fee":
                    float(ratio) * float(item["cummulativeQuoteQty"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get succeed trade
    def getTradeSucceed(self, fSymbol, tSymbol, limit='100', ratio=''):
        try:
            symbol = fSymbol + tSymbol
            orders = self._client.get_all_orders(symbol=symbol)
            if ratio == '':
                ratio = self._client.get_trade_fee(
                    symbol=symbol)["tradeFee"][0]["taker"]
            res = []
            for item in orders:
                if item["status"] == "FILLED":
                    ask_or_bid = "ask" if item["side"] == "BUY" else "bid"
                    filled_price = 0.0 if float(
                        item["executedQty"]) == 0 else float(
                            item["cummulativeQuoteQty"]) / float(
                                item["executedQty"])
                    res.append({
                        "timeStamp":
                        item["time"],
                        "order_id":
                        item["orderId"],
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
                        float(item["origQty"]),
                        "filled_price":
                        filled_price,
                        "filled_size":
                        float(item["executedQty"]),
                        "fee":
                        float(ratio) * float(item["cummulativeQuoteQty"])
                    })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get account all asset balance
    def getAccountBalances(self):
        try:
            base = self._client.get_account()
            res = []
            for b in base["balances"]:
                res.append({
                    "asset": b["asset"],
                    "balance": float(b["free"]) + float(b["locked"]),
                    "free": float(b["free"]),
                    "locked": float(b["locked"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get account assets deposit and withdraw limit
    def getAccountLimits(self):
        try:
            base = self._client.get_asset_details()
            res = []
            for key, value in base["assetDetail"].items():
                res.append({
                    "asset": key,
                    "can_deposit": value["depositStatus"],
                    "can_withdraw": value["withdrawStatus"],
                    "min_withdraw": float(value["minWithdrawAmount"])
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get account asset balance
    def getAccountAssetBalance(self, asset):
        try:
            base = self._client.get_asset_balance(asset=asset)
            res = {
                "asset": base["asset"],
                "balance": float(base["free"]) + float(base["locked"]),
                "free": float(base["free"]),
                "locked": float(base["locked"])
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset=''):
        try:
            deposit = self._client.get_deposit_history(asset=asset)
            withdraw = self._client.get_withdraw_history(asset=asset)
            res = {
                "deposit": deposit["depositList"],
                "withdraw": withdraw["withdrawList"]
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # create orders default limit
    def createOrder(self,
                    fSymbol,
                    tSymbol,
                    ask_or_bid,
                    price,
                    quantity,
                    ratio='',
                    type=ORDER_TYPE_LIMIT):
        # for speed up, lib not check, check from local db.data
        try:
            symbol = fSymbol + tSymbol
            params = {
                "symbol": symbol,
                "side": SIDE_BUY if ask_or_bid == "ask" else SIDE_SELL,
                "type": type,
                "timeInForce": TIME_IN_FORCE_GTC,
                "quantity": quantity,
                "price": price
            }
            base = self._client.create_order(**params)
            if ratio == '':
                ratio = self._client.get_trade_fee(
                    symbol=symbol)["tradeFee"][0]["taker"]
            filled_price = 0.0 if float(base["executedQty"]) == 0 else float(
                base["cummulativeQuoteQty"]) / float(base["executedQty"])
            res = {
                "timeStamp": base["transactTime"],
                "order_id": base["orderId"],
                "status": self.__STATUS[base["status"]],
                "type": self.__TYPE[base["type"]],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": self.__SIDE[base["side"]],
                "ask_bid_price": float(base["price"]),
                "ask_bid_size": float(base["origQty"]),
                "filled_price": filled_price,
                "filled_size": float(base["executedQty"]),
                "fee": float(ratio) * float(base["cummulativeQuoteQty"])
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # check orders done or undone
    def checkOrder(self, fSymbol, tSymbol, orderID, ratio=''):
        try:
            symbol = fSymbol + tSymbol
            params = {"symbol": symbol, "orderId": orderID}
            base = self._client.get_order(**params)
            if ratio == '':
                ratio = self._client.get_trade_fee(
                    symbol=symbol)["tradeFee"][0]["taker"]
            filled_price = 0.0 if float(base["executedQty"]) == 0 else float(
                base["cummulativeQuoteQty"]) / float(base["executedQty"])
            res = {
                "timeStamp": base["time"],
                "order_id": base["orderId"],
                "status": self.__STATUS[base["status"]],
                "type": self.__TYPE[base["type"]],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": self.__SIDE[base["side"]],
                "ask_bid_price": float(base["price"]),
                "ask_bid_size": float(base["origQty"]),
                "filled_price": filled_price,
                "filled_size": float(base["executedQty"]),
                "fee": float(ratio) * float(base["cummulativeQuoteQty"])
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # cancle the specific order
    def cancleOrder(self, fSymbol, tSymbol, orderID):
        try:
            symbol = fSymbol + tSymbol
            params = {"symbol": symbol, "orderId": orderID}
            info = self._client.get_order(**params)
            if info["status"] == "NEW" or info["status"] == "PARTIALLY_FILLED":
                base = self._client.cancel_order(**params)
                res = {"order_id": orderID, "status": ORDER_STATUS_CANCELED}
            else:
                res = {
                    "order_id": orderID,
                    "status": self.__STATUS[info["status"]]
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # cancle the batch orders
    def cancleBatchOrder(self, fSymbol, tSymbol, orderIDs):
        try:
            symbol = fSymbol + tSymbol
            res = []
            for orderID in orderIDs:
                params = {"symbol": symbol, "orderId": orderID}
                info = self._client.get_order(**params)
                if info["status"] == "NEW" or info[
                        "status"] == "PARTIALLY_FILLED":
                    base = self._client.cancel_order(**params)
                    res.append({
                        "order_id": orderID,
                        "status": ORDER_STATUS_CANCELED
                    })
                else:
                    res.append({
                        "order_id": orderID,
                        "status": self.__STATUS[info["status"]]
                    })
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            raise BinanceException(err)

    # deposit asset balance
    def depositAsset(self, asset):
        pass

    # withdraw asset balance
    def withdrawAsset(self, asset):
        pass
