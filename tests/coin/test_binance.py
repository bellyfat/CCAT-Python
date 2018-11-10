# -*- coding: utf-8 -*-

import hashlib
import json
import os
import sys
import unittest

sys.path.append(os.getcwd())

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
        logger.debug(res)
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
        logger.debug(res)
        self.assertEqual(res["proxies"], proxies["url"])

    def test_getServerTime(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerTime()
        logger.debug(res)
        self.assertIsInstance(res, int)

    def test_getServerLimits(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerLimits()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getServerSymbols(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getServerSymbols()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getSymbolsLimits(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getSymbolsLimits("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookTicker(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getMarketOrderbookTicker("IOST", "BTC")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getMarketOrderbookDepth("IOST", "BTC", 5)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getMarketKline(
            "IOST", "BTC", "6h", "2018-11-01T00:00:00.000Z", "2018-11-02T00:00:00.000Z")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeFees(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getTradeFees(symbol="ETHUSDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOpen(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getTradeOpen("ETH", "USDT", 0.0015)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeHistory(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getTradeHistory("ETH", "USDT", 0.0015)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeSucceed(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getTradeSucceed("ETH", "USDT", 0.0015)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountBalances(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getAccountBalances()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountLimits(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getAccountLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountAssetBalance(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getAccountAssetBalance("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getAccountAssetDetail(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.getAccountAssetDetail("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_createOrder(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.createOrder("ETH", "USDT", "ask", 200, 0.05)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_checkOrder(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.checkOrder("ETH", "USDT", "102624667")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancleOrder(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.cancleOrder("ETH", "USDT", "134790465")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancleBatchOrder(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        res = binance.cancleBatchOrder(
            "ETH", "USDT", ["134809076", "134809137"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_depositeAsset(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        pass

    def test_withdrawAsset(self):
        proxies = Config()._proxies
        binanceConf = Config()._binance
        binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                          binanceConf["api_secret"], proxies["url"])
        pass


if __name__ == "__main__":
    unittest.main()
