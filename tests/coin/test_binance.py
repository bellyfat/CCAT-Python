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
        # logger.debug(res)
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
        # logger.debug(res)
        self.assertEqual(res["proxies"], proxies["url"])

    def test_getServerTime(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerTime()
        # logger.debug(res)
        self.assertIsInstance(res, int)

    def test_getServerLimits(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerLimits()
        # logger.debug(type(res))
        self.assertIsInstance(res, list)

    def test_getServerSymbols(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerSymbols()
        # logger.debug(type(res))
        self.assertIsInstance(res, dict)

    def test_getSymbolsLimits(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getSymbolsLimits("IOST","BTC")
        # logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookTicker(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getMarketOrderbookTicker("IOST","BTC")
        # logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getMarketOrderbookDepth("IOST","BTC",5)
        # logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getMarketKline("IOST","BTC","6h","2018-11-01T00:00:00.000Z","2018-11-02T00:00:00.000Z")
        logger.debug(res)
        self.assertIsInstance(res, list)




if __name__ == "__main__":
    print("Error: Should  be called form tests/test_coin.py")
