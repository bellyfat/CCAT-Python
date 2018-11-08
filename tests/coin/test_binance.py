# -*- coding: utf-8 -*-

import hashlib
import json
import unittest

from src.core.coin.lib.binance import Binance
from src.core.config import Config
from src.core.util.log import Logger

logger = Logger()


class TestBinance(unittest.TestCase):

    def test_getConfig(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getConfig()
        self.assertEqual(res["exchange"], binanceConf["exchange"])
        self.assertEqual(res["api_key"], binanceConf["api_key"])
        self.assertEqual(res["api_secret"], binanceConf["api_secret"])
        self.assertEqual(res["proxies"], proxies["url"])

    def test_setProxy(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        binance.setProxy(proxies["url"])
        res = binance.getConfig()
        self.assertEqual(res["proxies"], proxies["url"])

    def test_getServerTime(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerTime()
        self.assertNotEqual(res["serverTime"], "0")

    def test_getServerLimits(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerLimits()
        exp = [{'rateLimitType': 'REQUEST_WEIGHT', 'interval': 'MINUTE', 'limit': 1200},
               {'rateLimitType': 'ORDERS', 'interval': 'SECOND', 'limit': 10},
               {'rateLimitType': 'ORDERS', 'interval': 'DAY', 'limit': 100000}]
        self.assertEqual(json.dumps(res), json.dumps(exp))

    def test_getServerSymbols(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerSymbols()
        exp = b'{"symbol": "ETHBTC", "status": "TRADING", "baseAsset": "ETH", "baseAssetPrecision": 8, "quoteAsset": "BTC", "quotePrecision": 8, "orderTypes": ["LIMIT", "LIMIT_MAKER", "MARKET", "STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"], "icebergAllowed": true, "filters": [{"filterType": "PRICE_FILTER", "minPrice": "0.00334300", "maxPrice": "0.33426500", "tickSize": "0.00000100"}, {"filterType": "LOT_SIZE", "minQty": "0.00100000", "maxQty": "100000.00000000", "stepSize": "0.00100000"}, {"filterType": "MIN_NOTIONAL", "minNotional": "0.00100000"}, {"filterType": "ICEBERG_PARTS", "limit": 10}, {"filterType": "MAX_NUM_ALGO_ORDERS", "maxNumAlgoOrders": 5}]}'
        logger.debug(json.dumps(res[0]).encode())
        self.assertEqual(hashlib.md5(json.dumps(res[0]).encode()).hexdigest(), hashlib.md5(exp).hexdigest())


if __name__ == "__main__":
    print("Error: Should  be called form tests/test_coin.py")
