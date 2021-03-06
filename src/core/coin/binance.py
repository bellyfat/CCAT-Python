# -*- coding: utf-8 -*-

# Binance class
# URL https://python-binance.readthedocs.io/en/latest/overview.html

import json
import math
from decimal import ROUND_DOWN, ROUND_HALF_UP, ROUND_UP, Decimal

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
from src.core.util.helper import num_to_precision

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Binance(Coin):

    __STATUS = {
        "PENDING_CANCEL": CCAT_ORDER_STATUS_CANCELING,
        "NEW": CCAT_ORDER_STATUS_OPEN,
        "PARTIALLY_FILLED": CCAT_ORDER_STATUS_PART_FILLED,
        "FILLED": CCAT_ORDER_STATUS_FILLED,
        "CANCELED": CCAT_ORDER_STATUS_CANCELED
    }

    __TYPE = {"LIMIT": CCAT_ORDER_TYPE_LIMIT, "MARKET": CCAT_ORDER_TYPE_MARKET}

    __SIDE = {"BUY": CCAT_ORDER_SIDE_BUY, "SELL": CCAT_ORDER_SIDE_SELL}

    def __init__(self, exchange, api_key, api_secret, proxies=None):
        super(Binance, self).__init__(exchange, api_key, api_secret, proxies)
        self._client = Client(api_key, api_secret, {
            "proxies": proxies,
            "verify": False,
            "timeout": 5
        })

    def __del__(self):
        self._client.session.close()

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._client = Client(self._api_key, self._api_secret, {
            "proxies": proxies,
            "verify": False,
            "timeout": 5
        })

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._client.get_server_time()  # UTC Zone UnixStamp
            return res["serverTime"]
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.getServerTime: exception err=%s" % err
            raise BinanceException(errStr)

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
                "info_second": 5,
                "market_second": requests_second,
                "orders_second": orders_second,
                "webSockets_second": ''
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.getServerLimits: exception err=%s" % err
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getServerSymbols: exception err=%s" % err
            raise BinanceException(errStr)

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
                # tSymbol_price_precision = math.pow(10, -int(base["baseAssetPrecision"]))
                # fSymbol_size_precision = math.pow(10, -int(base["quotePrecision"]))
                for b in base["filters"]:
                    if b["filterType"] == "PRICE_FILTER":
                        tSymbol_price_precision = float(b["tickSize"])
                        tSymbol_price_max = float(b["maxPrice"])
                        tSymbol_price_min = float(b["minPrice"])
                        tSymbol_price_step = float(b["tickSize"])
                    if b["filterType"] == "LOT_SIZE":
                        fSymbol_size_precision = float(b["stepSize"])
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
            errStr = "src.core.coin.binance.Binance.getSymbolsLimits: exception err=%s" % err
            raise BinanceException(errStr)

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, aggDepth=0):
        try:
            symbol = fSymbol + tSymbol
            timeStamp = self._client.get_server_time()["serverTime"]
            base = self._client.get_order_book(symbol=symbol, limit=100)
            if not 'lastUpdateId' in base.keys() or not len(
                    base["bids"]) > 0 or not len(base["asks"]) > 0:
                err = "{fSymbol=%s, tSymbol=%s, base=%s}" % (fSymbol, tSymbol,
                                                             base)
                raise BinanceException(err)
            if aggDepth == 0:
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
                aggPrice = num_to_precision(float(base["bids"][0][0]), float(aggDepth), rounding=ROUND_DOWN)
                bid_one_price = float(aggPrice)
                bid_one_size = 0.0
                for bid in base["bids"]:
                    if float(bid[0]) < float(aggPrice):
                        break
                    bid_one_size = bid_one_size + float(bid[1])
                # calc asks
                aggPrice =  num_to_precision(float(base["asks"][0][0]), float(aggDepth), rounding=ROUND_UP)
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
            errStr = "src.core.coin.binance.Binance.getMarketOrderbookTicker: { fSymbol=%s, tSymbol=%s, aggDepth=%s }, exception err=%s" % (
                fSymbol, tSymbol, aggDepth, err)
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getMarketOrderbookDepth: { fSymbol=%s, tSymbol=%s, limit=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, err)
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getMarketKline: { fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s }, exception err=%s" % (
                fSymbol, tSymbol, interval, start, end, err)
            raise BinanceException(errStr)

    # get symbol trade fees
    def getTradeFees(self):
        try:
            res = self._client.get_trade_fee()
            return res["tradeFee"]
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.getTradeFees: exception err=%s" % err
            raise BinanceException(errStr)

    # get current trade
    def getTradeOpen(self, fSymbol='', tSymbol='', limit='100', ratio=''):
        try:
            symbol = ''
            if fSymbol != '' and tSymbol != '':
                symbol = fSymbol + tSymbol
                orders = self._client.get_open_orders(symbol=symbol)
            else:
                orders = self._client.get_open_orders()
            if ratio == '' and symbol != '':
                ratio = self._client.get_trade_fee(
                    symbol=symbol)["tradeFee"][0]["taker"]
            else:
                ratio = 0
            res = []
            for item in orders:
                filled_price = 0.0 if float(
                    item["executedQty"]) == 0 else float(
                        item["cummulativeQuoteQty"]) / float(
                            item["executedQty"])
                if symbol == '':
                    if item['symbol'][-4:] != 'USDT':
                        fSymbol = item['symbol'][:-3]
                        tSymbol = item['symbol'][-3:]
                    else:
                        fSymbol = item['symbol'][:-4]
                        tSymbol = item['symbol'][-4:]
                res.append({
                    "timeStamp":
                    item["time"],
                    "order_id":
                    item["orderId"],
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
            errStr = "src.core.coin.binance.Binance.getTradeOpen: { fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getTradeHistory: { fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getTradeSucceed: { fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s }, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getAccountBalances: exception err=%s" % err
            raise BinanceException(errStr)

    # get account all asset deposit and withdraw history
    def getAccountDetail(self):
        try:
            deposit = self._client.get_deposit_history()
            withdraw = self._client.get_withdraw_history()
            assets = []
            for de in deposit["depositList"]:
                if not de["asset"] in assets:
                    assets.append(de["asset"])
            for wi in withdraw["withdrawList"]:
                if not wi["asset"] in assets:
                    assets.append(wi["asset"])
            res = []
            for a in assets:
                deRes = []
                wiRes = []
                for de in deposit["depositList"]:
                    if de["asset"] == a:
                        deRes.append(de)
                for wi in withdraw["withdrawList"]:
                    if wi["asset"] == a:
                        wiRes.append(wi)
                res.append({"asset": a, "deposit": deRes, "withdraw": wiRes})
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.getAccountDetail: exception err=%s" % (
                asset, err)
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getAccountLimits: exception err=%s" % err
            raise BinanceException(errStr)

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
            errStr = "src.core.coin.binance.Binance.getAccountAssetBalance: { asset=%s }, exception err=%s" % (
                asset, err)
            raise BinanceException(errStr)

    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset=''):
        try:
            deposit = self._client.get_deposit_history(asset=asset)
            withdraw = self._client.get_withdraw_history(asset=asset)

            res = {}
            if deposit["depositList"] != [] or withdraw["withdrawList"] != []:
                res = {
                    "deposit": deposit["depositList"],
                    "withdraw": withdraw["withdrawList"]
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.getAccountAssetDetail: { asset=%s }, exception err=%s" % (
                asset, err)
            raise BinanceException(errStr)

    # create orders default limit
    def createOrder(self,
                    fSymbol,
                    tSymbol,
                    ask_or_bid,
                    price,
                    quantity,
                    ratio='',
                    type=CCAT_ORDER_TYPE_LIMIT):
        # for speed up, lib not check, check from local db.data
        try:
            symbol = fSymbol + tSymbol
            params = {
                "symbol":
                symbol,
                "side":
                SIDE_BUY if ask_or_bid == CCAT_ORDER_SIDE_BUY else SIDE_SELL,
                "type":
                type,
                "timeInForce":
                TIME_IN_FORCE_GTC,
                "quantity":
                quantity,
                "price":
                price
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
            errStr = "src.core.coin.binance.Binance.createOrder: { fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, quantity=%s, ratio=%s, type=%s }, exception err=%s" % (
                fSymbol, tSymbol, ask_or_bid, price, quantity, ratio, type,
                err)
            raise BinanceException(errStr)

    # check orders done or undone
    def checkOrder(self, orderID, fSymbol, tSymbol, ratio=''):
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
            errStr = "src.core.coin.binance.Binance.checkOrder: { orderID=%s, fSymbol=%s, tSymbol=%s, ratio=%s }, exception err=%s" % (
                orderID, fSymbol, tSymbol, ratio, err)
            raise BinanceException(errStr)

    # cancel the specific order
    def cancelOrder(self, orderID, fSymbol, tSymbol):
        try:
            symbol = fSymbol + tSymbol
            params = {"symbol": symbol, "orderId": orderID}
            info = self._client.get_order(**params)
            if info["status"] == "NEW" or info["status"] == "PARTIALLY_FILLED":
                base = self._client.cancel_order(**params)
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
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.cancelOrder: { orderID=%s, fSymbol=%s, tSymbol=%s }, exception err=%s" % (
                orderID, fSymbol, tSymbol, err)
            raise BinanceException(errStr)

    # cancel the batch orders
    def cancelBatchOrder(self, orderIDs, fSymbol, tSymbol):
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
                        "status": CCAT_ORDER_STATUS_CANCELED
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
            errStr = "src.core.coin.binance.Binance.cancelBatchOrder: { orderIDs=%s, fSymbol=%s, tSymbol=%s }, exception err=%s" % (
                orderIDs, fSymbol, tSymbol, err)
            raise BinanceException(errStr)

    # one click cancle all orders
    def oneClickCancleOrders(self):
        try:
            res = self.getTradeOpen()
            for r in res:
                b = self.cancelOrder(r['order_id'], r['fSymbol'], r['tSymbol'])
                if b['status'] != CCAT_ORDER_STATUS_CANCELED:
                    return False
            return True
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.oneClickCancleOrders: exception err=%s" % err
            raise BinanceException(errStr)

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
        except (ReadTimeout, ConnectionError, KeyError, BinanceAPIException,
                BinanceRequestException, BinanceOrderException,
                BinanceWithdrawException, Exception) as err:
            errStr = "src.core.coin.binance.Binance.oneClickTransToBaseCoin: exception err=%s" % err
            raise BinanceException(errStr)

    # deposit asset balance
    def depositAsset(self, asset):
        pass

    # withdraw asset balance
    def withdrawAsset(self, asset):
        pass
