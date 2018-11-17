# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.getcwd())

from src.core.util.log import Logger
from src.core.config import Config
from src.core.coin.binance import Binance

proxies = Config()._proxies
binanceConf = Config()._binance
binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                  binanceConf["api_secret"], proxies["url"])
logger = Logger()


class TestBinance(unittest.TestCase):
    def test_getConfig(self):
        res = binance.getConfig()
        logger.debug(res)
        self.assertEqual(res["exchange"], binanceConf["exchange"])
        self.assertEqual(res["api_key"], binanceConf["api_key"])
        self.assertEqual(res["api_secret"], binanceConf["api_secret"])
        self.assertEqual(res["proxies"], proxies["url"])

    def test_setProxy(self):
        binance.setProxy(proxies["url"])
        res = binance.getConfig()
        logger.debug(res)
        self.assertEqual(res["proxies"], proxies["url"])

    def test_getServerTime(self):
        res = binance.getServerTime()
        logger.debug(res)
        self.assertIsInstance(res, int)

    def test_getServerLimits(self):
        res = binance.getServerLimits()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getServerSymbols(self):
        res = binance.getServerSymbols()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getSymbolsLimits(self):
        res = binance.getSymbolsLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getMarketOrderbookTicker(self):
        res = binance.getMarketOrderbookTicker("IOST", "BTC")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        res = binance.getMarketOrderbookDepth("IOST", "BTC", 5)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        res = binance.getMarketKline(
            "IOST", "BTC", "1m", "2018-11-11T00:00:00.000Z", "2018-11-11T01:00:00.000Z")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeFees(self):
        res = binance.getTradeFees()
        # res = binance.getTradeFees(symbol="ETHUSDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOpen(self):
        res = binance.getTradeOpen("ETH", "USDT", 0.0015)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeHistory(self):
        res = binance.getTradeHistory("ETH", "USDT", 0.0015)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeSucceed(self):
        res = binance.getTradeSucceed("ETH", "USDT", 0.0015)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountBalances(self):
        res = binance.getAccountBalances()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountLimits(self):
        res = binance.getAccountLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountAssetBalance(self):
        res = binance.getAccountAssetBalance("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getAccountAssetDetail(self):
        res = binance.getAccountAssetDetail("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    # def test_createOrder(self):
    #     res = binance.createOrder("ETH", "USDT", "ask", 150, 0.05)
    #     logger.debug(res)
    #     self.assertIsInstance(res, dict)

    def test_checkOrder(self):
        res = binance.checkOrder("ETH", "USDT", "102624667")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancleOrder(self):
        res = binance.cancleOrder("ETH", "USDT", "135080289")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancleBatchOrder(self):
        res = binance.cancleBatchOrder("ETH", "USDT", ["134809076", "134809137"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_depositeAsset(self):
        pass

    def test_withdrawAsset(self):
        pass


if __name__ == "__main__":
    unittest.main()
