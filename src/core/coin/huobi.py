# -*- coding: utf-8 -*-

# Huobi Class

import math
from decimal import ROUND_DOWN, ROUND_UP, Decimal

import requests
from requests.exceptions import ConnectionError, ReadTimeout

from src.core.coin.coin import Coin
from src.core.coin.lib.huobipro_api.HuobiService import Huobi as HuobiAPI
from src.core.util.exceptions import HuobiException
from src.core.util.helper import date_to_milliseconds, interval_to_milliseconds


class Huobi(Coin):
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
                fSymbol = b["base-currency"]
                tSymbol = b["quote-currency"]
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
            for b in base['data']:
                # if not b["symbol-partition"]="main":
                #     continue
                fSymbol = b["base-currency"]
                tSymbol = b["quote-currency"]
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
                err = "{fSymbol=%s, tSymbol=%s} response base=%s" % (fSymbol, tSymbol,
                                                             base)
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
                err = "{fSymbol=%s, tSymbol=%s} response base=%s" % (fSymbol, tSymbol,
                                                             base)
                raise Exception(err)
            if limit != '':
                limit = min((int(limit), len(base['tick']["bids"]),
                                  len(base['tick']["asks"])))
            else:
                limit = min((len(base['tick']["bids"]),
                                  len(base['tick']["asks"])))
            print(limit)
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
                "1m":"1min",
                "5m": "5min",
                "15m": "15min",
                "30m": "30min",
                "60m": "60min",
                "1d": "1day",
                "1m": "1mon",
                "1w": "1week",
                "1y": "1year"
                }
            granularity = interval_to_milliseconds(interval)
            size = int((date_to_milliseconds(end)-date_to_milliseconds(start))/granularity)
            if size < 1 or size > 2000:
                err = "{fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s} calc size=%s error" % (fSymbol, tSymbol, interval, start, end, size)
                raise Exception(err)
            base = self._huobiAPI.get_kline(symbol,period[interval],size)
            if not base['status'] == 'ok':
                err = "{fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s} response base=%s" % (fSymbol, tSymbol, interval, start, end, base)
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
