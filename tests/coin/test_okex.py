# -*- coding: utf-8 -*-

import hashlib
import json
import os
import sys
import unittest

sys.path.append(os.getcwd())

from src.core.coin.lib.okex import Okex
from src.core.config import Config
from src.core.util.log import Logger


logger = Logger()


class TestOkex(unittest.TestCase):

    def test_getConfig(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getConfig()
        logger.debug(res)
        self.assertEqual(res["exchange"], okexConf["exchange"])
        self.assertEqual(res["api_key"], okexConf["api_key"])
        self.assertEqual(res["api_secret"], okexConf["api_secret"])
        self.assertEqual(res["proxies"], proxies["url"])

    def test_setProxy(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"])
        okex.setProxy(proxies["url"])
        res = okex.getConfig()
        logger.debug(res)
        self.assertEqual(res["proxies"], proxies["url"])

    def test_getServerTime(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getServerTime()
        logger.debug(res)
        self.assertIsInstance(res, int)

    def test_getServerLimits(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getServerLimits()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getServerSymbols(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getServerSymbols()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getSymbolsLimits(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getSymbolsLimits("TRX", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookTicker(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getMarketOrderbookTicker("STC", "BTC")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getMarketOrderbookDepth("STC", "BTC", 5)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getMarketKline(
            "STC", "BTC", "1h", "2018-11-01T00:00:00.000Z", "2018-11-02T00:00:00.000Z")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeFees(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])

        res = okex.getTradeFees()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOpen(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getTradeOpen("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeHistory(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getTradeHistory("TRX", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeSucceed(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getTradeSucceed("TRX", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountBalances(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getAccountBalances()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountLimits(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getAccountLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountAssetBalance(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getAccountAssetBalance("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getAccountAssetDetail(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getAccountAssetDetail("USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_createOrder(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.createOrder("ETH", "USDT", "ask", 200, 0.001)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_checkOrder(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.checkOrder("TRX", "USDT", "1774314142386176")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancleOrder(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.cancleOrder("TRX", "USDT", "1774314142386176")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancleBatchOrder(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.cancleBatchOrder(
            "TRX", "USDT", ["1774314142386176", "1771669234011136"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_depositeAsset(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        pass

    def test_withdrawAsset(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        pass


if __name__ == "__main__":
    unittest.main()
