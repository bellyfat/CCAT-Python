# -*- coding: utf-8 -*-

# Huobi Class

import math
from decimal import ROUND_DOWN, ROUND_UP, Decimal

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from src.core.coin.coin import Coin
from src.core.coin.enums import *
from src.core.coin.lib.huobipro_api.HuobiService import Huobi as HuobiAPI
from src.core.util.exceptions import HuobiException
from src.core.util.helper import (date_to_milliseconds,
                                  interval_to_milliseconds, utcnow_timestamp)


class Huobi(Coin):

    __STATUS = {
        "submitting": ORDER_STATUS_ORDERING,
        "submitted": ORDER_STATUS_OPEN,
        "partial-filled": ORDER_STATUS_PART_FILLED,
        "partial-canceled": ORDER_STATUS_CANCELING,
        "filled": ORDER_STATUS_FILLED,
        "canceled": ORDER_STATUS_CANCELED
    }

    __TYPE = {
        "buy-market": ORDER_TYPE_MARKET,
        "sell-market": ORDER_TYPE_MARKET,
        "buy-limit": ORDER_TYPE_LIMIT,
        "sell-limit": ORDER_TYPE_LIMIT
    }

    __SIDE = {
        "buy-market": ORDER_SIDE_BUY,
        "sell-market": ORDER_SIDE_SELL,
        "buy-limit": ORDER_SIDE_BUY,
        "sell-limit": ORDER_SIDE_SELL
    }

    def __init__(self,
                 exchange,
                 api_key,
                 api_secret,
                 acct_id=None,
                 proxies=None):
        super(Huobi, self).__init__(exchange, api_key, api_secret, proxies)
        self._acct_id = acct_id
        self._huobiAPI = HuobiAPI(self._api_key, self._api_secret,
                                  self._acct_id, self._proxies)

    # get config
    def getConfig(self):
        return {
            "exchange": self._exchange,
            "api_key": self._api_key,
            "api_secret": self._api_secret,
            "acct_id": self._acct_id,
            "proxies": self._proxies
        }

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._huobiAPI = HuobiAPI(self._api_key, self._api_secret,
                                  self._acct_id, self._proxies)

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            res = self._huobiAPI.get_timestamp()
            if not res['status'] == 'ok':
                raise Exception(res)
            return int(res['data'])
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # per seconds qurry and orders rate limits
    def getServerLimits(self):
        '''
        REST API
        限制频率（每个接口，只针对交易api，行情api不限制）为10秒100次。
        '''
        res = {
            "info_second": 60,
            "market_second": 60,
            "orders_second": 10,
            "webSockets_second": ''
        }
        return res

    # all symbols in pairs list baseSymbol quoteSymbol
    def getServerSymbols(self):
        try:
            base = self._huobiAPI.get_symbols()
            if not base['status'] == 'ok':
                raise Exception(base)
            fSymbol = ''
            tSymbol = ''
            res = []
            for b in base['data']:
                fSymbol = b["base-currency"].upper()
                tSymbol = b["quote-currency"].upper()
                res.append({"fSymbol": fSymbol, "tSymbol": tSymbol})
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # def getServerSymbols(self):
    #     # not all api defined, get form cryptoCompare
    #     try:
    #         querry = "https://min-api.cryptocompare.com/data/all/exchanges"
    #         res = requests.request("GET", querry)
    #         if res.status_code == requests.codes.ok:
    #             return res.json()["Huobipro"]
    #         else:
    #             raise HuobiException(err)
    #     except requests.exceptions.RequestException:
    #         raise HuobiException(err)

    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self):
        try:
            base = self._huobiAPI.get_symbols()
            if not base['status'] == 'ok':
                raise Exception(base)
            res = []
            for b in base['data']:
                # if not b["symbol-partition"]="main":
                #     continue
                fSymbol = b["base-currency"].upper()
                tSymbol = b["quote-currency"].upper()
                tSymbol_price_precision = math.pow(10,
                                                   -int(b["price-precision"]))
                tSymbol_price_max = ''
                tSymbol_price_min = math.pow(10, -int(b["price-precision"]))
                tSymbol_price_step = math.pow(10, -int(b["price-precision"]))
                fSymbol_size_precision = math.pow(10,
                                                  -int(b["amount-precision"]))
                fSymbol_size_max = ''
                fSymbol_size_min = math.pow(10, -int(b["amount-precision"]))
                fSymbol_size_step = math.pow(10, -int(b["amount-precision"]))
                min_notional = fSymbol_size_min * tSymbol_price_min
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
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, aggDepth=''):
        try:
            if aggDepth != '':
                if float(aggDepth) > 1:
                    raise Exception("aggDepth must < 1.0")
            symbol = (fSymbol + tSymbol).lower()
            base = self._huobiAPI.get_depth(symbol, 'step0')
            if not base['status'] == 'ok' or not len(
                    base['tick']["bids"]) > 0 or not len(
                        base['tick']["asks"]) > 0:
                err = "{fSymbol=%s, tSymbol=%s} response base=%s" % (
                    fSymbol, tSymbol, base)
                raise Exception(err)
            if aggDepth == '':
                res = {
                    "timeStamp": base["ts"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": float(base['tick']["bids"][0][0]),
                    "bid_one_size": float(base['tick']["bids"][0][1]),
                    "ask_one_price": float(base['tick']["asks"][0][0]),
                    "ask_one_size": float(base['tick']["asks"][0][1])
                }
            else:
                # calc bids
                aggPrice = Decimal(base['tick']["bids"][0][0]).quantize(
                    Decimal(str(aggDepth)), rounding=ROUND_DOWN)
                bid_one_price = float(aggPrice)
                bid_one_size = 0.0
                for bid in base['tick']["bids"]:
                    if float(bid[0]) < float(aggPrice):
                        break
                    bid_one_size = bid_one_size + float(bid[1])
                # calc asks
                aggPrice = Decimal(base['tick']["asks"][0][0]).quantize(
                    Decimal(str(aggDepth)), rounding=ROUND_UP)
                ask_one_price = float(aggPrice)
                ask_one_size = 0.0
                for ask in base['tick']["asks"]:
                    if float(ask[0]) > float(aggPrice):
                        break
                    ask_one_size = ask_one_size + float(ask[1])
                res = {
                    "timeStamp": base["ts"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": bid_one_price,
                    "bid_one_size": bid_one_size,
                    "ask_one_price": ask_one_price,
                    "ask_one_size": ask_one_size
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit=''):
        '''
        "tick": {
            "id": 消息id,
            "ts": 消息生成时间，单位：毫秒,
            "bids": 买盘,[price(成交价), amount(成交量)], 按price降序,
            "asks": 卖盘,[price(成交价), amount(成交量)], 按price升序
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            base = self._huobiAPI.get_depth(symbol, 'step0')
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s} response base=%s" % (
                    fSymbol, tSymbol, base)
                raise Exception(err)
            if limit != '':
                limit = min((int(limit), len(base['tick']["bids"]),
                             len(base['tick']["asks"])))
            else:
                limit = min((len(base['tick']["bids"]),
                             len(base['tick']["asks"])))
            res = {
                "timeStamp": base["ts"],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_price_size": base['tick']["bids"][0:limit:1],
                "ask_price_size": base['tick']["asks"][0:limit:1]
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # a specific symbols kline/candlesticks
    def getMarketKline(self, fSymbol, tSymbol, interval, start, end):
        '''
        "data": [
            {
                "id": K线id（时间戳）,
                "amount": 成交量,
                "count": 成交笔数,
                "open": 开盘价,
                "close": 收盘价,当K线为最晚的一根时，是最新成交价
                "low": 最低价,
                "high": 最高价,
                "vol": 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
            }

        ]
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            period = {
                "1m": "1min",
                "5m": "5min",
                "15m": "15min",
                "30m": "30min",
                "1h": "60min",
                "1d": "1day",
                "1m": "1mon",
                "1w": "1week",
                "1y": "1year"
            }
            granularity = interval_to_milliseconds(interval)
            size = int(
                (date_to_milliseconds(end) - date_to_milliseconds(start)) /
                granularity)
            if size < 1 or size > 2000:
                err = "{fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s} calc size=%s error" % (
                    fSymbol, tSymbol, interval, start, end, size)
                raise Exception(err)
            base = self._huobiAPI.get_kline(symbol, period[interval], size)
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s} response base=%s" % (
                    fSymbol, tSymbol, interval, start, end, base)
                raise Exception(err)
            res = []
            for b in base['data']:
                res.append({
                    "timeStamp": base['ts'],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "open": b["open"],
                    "high": b["high"],
                    "low": b["low"],
                    "close": b["close"],
                    "volume": b["amount"]
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get symbol trade fees
    def getTradeFees(self):
        '''
        币币手续费： 挂单成交0.1%， 吃单成交0.15%
        '''
        res = [{"symbol": "all", "maker": 0.002, "taker": 0.002}]
        return res

    # get current trade
    def getTradeOpen(self, fSymbol, tSymbol, limit='100', ratio=''):
        '''
        /* GET /v1/orders/openOrders */
        {
          "status": "ok",
          "data": [
            {
              "id": 5454937,
              "symbol": "ethusdt",
              "account-id": 30925,
              "amount": "1.000000000000000000",
              "price": "0.453000000000000000",
              "created-at": 1530604762277,
              "type": "sell-limit",
              "filled-amount": "0.0",
              "filled-cash-amount": "0.0",
              "filled-fees": "0.0",
              "source": "web",
              "state": "submitted"
            }
          ]
        }
        '''
        try:
            symbol = ''
            account_id = ''
            if fSymbol and tSymbol:
                symbol = (fSymbol + tSymbol).lower()
                account_id = self._acct_id if self._acct_id else self._huobiAPI.get_accounts(
                )['data'][0]['id']
            side = ''
            size = limit
            base = self._huobiAPI.open_orders(account_id, symbol, side, size)
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s} response base=%s" % (
                    fSymbol, tSymbol, limit, ratio, base)
                raise Exception(err)
            res = []
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            for b in base['data']:
                filled_price = 0.0 if float(
                    b["filled-amount"]) == 0 else float(
                        b["filled-cash-amount"]) / float(b["filled-amount"])
                res.append({
                    "timeStamp": b["created-at"],
                    "order_id": b["id"],
                    "status": ORDER_STATUS_OPEN,
                    "type": self.__TYPE[b["type"]],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": self.__SIDE[b["type"]],
                    "ask_bid_price": float(b["price"]),
                    "ask_bid_size": float(b["amount"]),
                    "filled_price": filled_price,
                    "filled_size": float(b["filled-amount"]),
                    "fee": float(b["filled-fees"])
                    # "fee": float(b["filled-cash-amount"]) * ratio
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get history trade
    def getTradeHistory(self, fSymbol, tSymbol, limit='100', ratio=''):
        '''
        /* GET /v1/order/orders */
        {
          "status": "ok",
          "data": [
            {
              "id": 59378,
              "symbol": "ethusdt",
              "account-id": 100009,
              "amount": "10.1000000000",
              "price": "100.1000000000",
              "created-at": 1494901162595,
              "type": "buy-limit",
              "field-amount": "10.1000000000",
              "field-cash-amount": "1011.0100000000",
              "field-fees": "0.0202000000",
              "finished-at": 1494901400468,
              "user-id": 1000,
              "source": "api",
              "state": "filled",
              "canceled-at": 0,
              "exchange": "huobi",
              "batch": ""
            }
          ]
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            states = "submitting,submitted,partial-filled,partial-canceled,filled,canceled"
            types = "buy-market,sell-market,buy-limit,sell-limit"
            size = limit
            base = self._huobiAPI.orders_list(symbol, states, types, '', '',
                                              '', '', size)
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s} response base=%s" % (
                    fSymbol, tSymbol, limit, ratio, base)
                raise Exception(err)
            res = []
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            for b in base['data']:
                filled_price = 0.0 if float(b["field-amount"]) == 0 else float(
                    b["field-cash-amount"]) / float(b["field-amount"])
                res.append({
                    "timeStamp": b["created-at"],
                    "order_id": b["id"],
                    "status": self.__STATUS[b["state"]],
                    "type": self.__TYPE[b["type"]],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": self.__SIDE[b["type"]],
                    "ask_bid_price": float(b["price"]),
                    "ask_bid_size": float(b["amount"]),
                    "filled_price": filled_price,
                    "filled_size": float(b["field-amount"]),
                    "fee": float(b["field-fees"])
                    # "fee": float(b["field-cash-amount"]) * ratio
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get succeed trade
    def getTradeSucceed(self, fSymbol, tSymbol, limit='100', ratio=''):
        '''
        /* GET /v1/order/orders */
        {
          "status": "ok",
          "data": [
            {
              "id": 59378,
              "symbol": "ethusdt",
              "account-id": 100009,
              "amount": "10.1000000000",
              "price": "100.1000000000",
              "created-at": 1494901162595,
              "type": "buy-limit",
              "field-amount": "10.1000000000",
              "field-cash-amount": "1011.0100000000",
              "field-fees": "0.0202000000",
              "finished-at": 1494901400468,
              "user-id": 1000,
              "source": "api",
              "state": "filled",
              "canceled-at": 0,
              "exchange": "huobi",
              "batch": ""
            }
          ]
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            states = "filled"
            types = "buy-market,sell-market,buy-limit,sell-limit"
            size = limit
            base = self._huobiAPI.orders_list(symbol, states, types, '', '',
                                              '', '', size)
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s} response base=%s" % (
                    fSymbol, tSymbol, limit, ratio, base)
                raise Exception(err)
            res = []
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            for b in base['data']:
                filled_price = 0.0 if float(b["field-amount"]) == 0 else float(
                    b["field-cash-amount"]) / float(b["field-amount"])
                res.append({
                    "timeStamp": b["created-at"],
                    "order_id": b["id"],
                    "status": self.__STATUS[b["state"]],
                    "type": self.__TYPE[b["type"]],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": self.__SIDE[b["type"]],
                    "ask_bid_price": float(b["price"]),
                    "ask_bid_size": float(b["amount"]),
                    "filled_price": filled_price,
                    "filled_size": float(b["field-amount"]),
                    "fee": float(b["field-fees"])
                    # "fee": float(b["field-cash-amount"]) * ratio
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get account all asset balance
    def getAccountBalances(self):
        '''
        /* GET /v1/account/accounts/'account-id'/balance */
        {
          "status": "ok",
          "data": {
            "id": 100009,
            "type": "spot",
            "state": "working",
            "list": [
              {
                "currency": "usdt",
                "type": "trade",
                "balance": "500009195917.4362872650"
              },
              {
                "currency": "usdt",
                "type": "frozen",
                "balance": "328048.1199920000"
              },
             {
                "currency": "etc",
                "type": "trade",
                "balance": "499999894616.1302471000"
              },
              {
                "currency": "etc",
                "type": "frozen",
                "balance": "9786.6783000000"
              }
             {
                "currency": "eth",
                "type": "trade",
                "balance": "499999894616.1302471000"
              },
              {
                "currency": "eth",
                "type": "frozen",
                "balance": "9786.6783000000"
              }
            ],
            "user-id": 1000
          }
        }
        '''
        try:
            base = self._huobiAPI.get_balance()
            if not base['status'] == 'ok':
                err = "response base=%s" % base
                raise Exception(err)
            currencies = []
            res = []
            for b in base['data']['list']:
                if b["currency"] not in currencies:
                    currencies.append(b["currency"])
                    res.append({
                        "asset": b["currency"],
                        "balance": 0.0,
                        "free": 0.0,
                        "locked": 0.0
                    })
            for i in range(len(res)):
                for b in base['data']['list']:
                    if res[i]["asset"] == b["currency"] and b[
                            "type"] == "trade":
                        res[i]["free"] = float(b["balance"])
                    if res[i]["asset"] == b["currency"] and b[
                            "type"] == "frozen":
                        res[i]["locked"] = float(b["balance"])
            for i in range(len(res)):
                res[i]["asset"] = res[i]["asset"].upper()
                res[i]["balance"] = res[i]["free"] + res[i]["locked"]
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get account asset deposit and withdraw limits
    def getAccountLimits(self):
        '''
        /* GET /v1/common/currencys */
        {
          "status": "ok",
          "data": [
            "usdt",
            "eth",
            "etc"
          ]
        }
        '''
        try:
            base = self._huobiAPI.get_currencies()
            if not base['status'] == 'ok':
                err = "response base=%s" % base
                raise Exception(err)
            res = []
            for b in base['data']:
                res.append({
                    "asset": b.upper(),
                    "can_deposit": '',
                    "can_withdraw": '',
                    "min_withdraw": ''
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get account asset balance
    def getAccountAssetBalance(self, asset):
        try:
            base = self._huobiAPI.get_balance()
            if not base['status'] == 'ok':
                err = "{asset=%s} response base=%s" % (asset, base)
                raise Exception(err)
            res = {}
            for b in base['data']['list']:
                if b["currency"] == asset.lower():
                    res = {
                        "asset": b["currency"],
                        "balance": 0.0,
                        "free": 0.0,
                        "locked": 0.0
                    }
            if res != {}:
                for b in base['data']['list']:
                    if res["asset"] == b["currency"] and b["type"] == "trade":
                        res["free"] = float(b["balance"])
                    if res["asset"] == b["currency"] and b["type"] == "frozen":
                        res["locked"] = float(b["balance"])
            if res != {}:
                res["asset"] = res["asset"].upper()
                res["balance"] = res["free"] + res["locked"]
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset):
        try:
            deRes = self._huobiAPI.get_deposit_withdraw(
                asset.lower(), type='deposit', froms='0', size='100')
            wiRes = self._huobiAPI.get_deposit_withdraw(
                asset.lower(), type='withdraw', froms='0', size='100')
            if not deRes['status'] == 'ok' or not wiRes['status'] == 'ok':
                err = "{asset=%s} response deRes=%s, wiRes=%s" % (asset, deRes,
                                                                  wiRes)
                raise Exception(err)
            deposit = []
            for de in deRes['data']:
                deposit.append(de)
            withdraw = []
            for wi in wiRes['data']:
                withdraw.appen(wi)
            res = {"deposit": deposit, "withdraw": withdraw}
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

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
            symbol = (fSymbol + tSymbol).lower()
            source = 'api'
            if ask_or_bid == ORDER_SIDE_BUY and type == ORDER_TYPE_LIMIT:
                _type = 'buy-limit'
            if ask_or_bid == ORDER_SIDE_BUY and type == ORDER_TYPE_MARKET:
                _type = 'buy-market'
            if ask_or_bid == ORDER_SIDE_SELL and type == ORDER_TYPE_LIMIT:
                _type = 'sell-limit'
            if ask_or_bid == ORDER_SIDE_SELL and type == ORDER_TYPE_MARKET:
                _type = 'sell-market'
            timeStamp = utcnow_timestamp()
            base = self._huobiAPI.send_order(quantity, source, symbol, _type,
                                             price)
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, quantity=%s, ratio=%s, type=%s} response base=%s" % (
                    fSymbol, tSymbol, ask_or_bid, price, quantity, ratio, type,
                    base)
                raise Exception(err)
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            res = {
                "timeStamp": timeStamp,
                "order_id": base["data"],
                "status": ORDER_STATUS_ORDERING,
                "type": self.__TYPE[_type],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": ask_or_bid,
                "ask_bid_price": float(price),
                "ask_bid_size": float(quantity),
                "filled_price": 0.0,
                "filled_size": 0.0,
                "fee": 0.0
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # check orders done or undone
    def checkOrder(self, orderID, fSymbol='', tSymbol='', ratio=''):
        try:
            base = self._huobiAPI.order_info(orderID)
            if not base['status'] == 'ok':
                err = "{orderID=%s, fSymbol=%s, tSymbol=%s, ratio=%s} response base=%s" % (
                    orderID, fSymbol, tSymbol, ratio, base)
                raise Exception(err)
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            b = base['data']
            filled_price = 0.0 if float(b["field-amount"]) == 0 else float(
                b["field-cash-amount"]) / float(b["field-amount"])
            res = {
                "timeStamp": b["created-at"],
                "order_id": b["id"],
                "status": self.__STATUS[b["state"]],
                "type": self.__TYPE[b["type"]],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": self.__SIDE[b["type"]],
                "ask_bid_price": float(b["price"]),
                "ask_bid_size": float(b["amount"]),
                "filled_price": filled_price,
                "filled_size": float(b["field-amount"]),
                "fee": float(b["field-fees"])
                # "fee": float(b["field-cash-amount"]) * ratio
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # cancel orders done or undone
    def cancelOrder(self, orderID, fSymbol='', tSymbol=''):
        try:
            ba = self._huobiAPI.order_info(orderID)
            if not ba['status'] == 'ok':
                err = "{orderID=%s, fSymbol=%s, tSymbol=%s} response ba=%s" % (
                    orderID, fSymbol, tSymbol, ba)
                raise Exception(err)
            if self.__STATUS[
                    ba['data']["state"]] == ORDER_STATUS_OPEN or self.__STATUS[
                        ba['data']["state"]] == ORDER_STATUS_PART_FILLED:
                base = self._huobiAPI.cancel_order(orderID)
                rebase = self._huobiAPI.order_info(orderID)
                if not base['status'] == 'ok' or not rebase['status'] == 'ok':
                    err = "{orderID=%s, fSymbol=%s, tSymbol=%s} response base=%s" % (
                        orderID, fSymbol, tSymbol, base)
                    raise Exception(err)
                res = {
                    "order_id": orderID,
                    "status": self.__STATUS[rebase['data']["state"]]
                }
            else:
                res = {
                    "order_id": orderID,
                    "status": self.__STATUS[ba['data']["state"]]
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # cancel the bathch orders
    def cancelBatchOrder(self, orderIDs, fSymbol='', tSymbol=''):
        try:
            res = []
            for orderID in orderIDs:
                ba = self._huobiAPI.order_info(orderID)
                if not ba['status'] == 'ok':
                    err = "{orderID=%s, fSymbol=%s, tSymbol=%s} response ba=%s" % (
                        orderID, fSymbol, tSymbol, ba)
                    raise Exception(err)
                if self.__STATUS[ba['data'][
                        "state"]] == ORDER_STATUS_OPEN or self.__STATUS[
                            ba['data']["state"]] == ORDER_STATUS_PART_FILLED:
                    base = self._huobiAPI.cancel_order(orderID)
                    rebase = self._huobiAPI.order_info(orderID)
                    if not base['status'] == 'ok' or not base[
                            'status'] == 'ok' or not rebase['status'] == 'ok':
                        err = "{orderID=%s, fSymbol=%s, tSymbol=%s} response base=%s, rebase" % (
                            orderID, fSymbol, tSymbol, base, rebase)
                        raise Exception(err)
                    res.append({
                        "order_id": orderID,
                        "status": self.__STATUS[rebase['data']["state"]]
                    })
                else:
                    res.append({
                        "order_id": orderID,
                        "status": self.__STATUS[ba['data']["state"]]
                    })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            raise HuobiException(err)

    # deposit asset balance
    def depositAsset(self, asset):
        pass

    # withdraw asset balance
    def withdrawAsset(self, asset):
        pass
