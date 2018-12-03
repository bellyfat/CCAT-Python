# -*- coding: utf-8 -*-

import os
import sys
import unittest

from src.core.coin.okex import Okex
from src.core.config import Config
from src.core.util.log import Logger

sys.path.append(os.getcwd())

# proxies
_proxies = Config()._Proxies_url if Config()._Proxies_proxies else None
# Okex
_Okex_exchange = Config()._Okex_exchange
_Okex_api_key = Config()._Okex_api_key
_Okex_api_secret = Config()._Okex_api_secret
_Okex_passphrase = Config()._Okex_passphrase

okex = Okex(_Okex_exchange, _Okex_api_key, _Okex_api_secret, _Okex_passphrase,
            _proxies)
logger = Logger()


class TestOkex(unittest.TestCase):
    def test_getConfig(self):
        res = okex.getConfig()
        logger.debug(res)
        self.assertEqual(res["exchange"], _Okex_exchange)

    def test_setProxy(self):
        okex.setProxy(_proxies)
        res = okex.getConfig()
        logger.debug(res)
        self.assertEqual(res["proxies"], _proxies)

    def test_getServerTime(self):
        res = okex.getServerTime()
        logger.debug(res)
        self.assertIsInstance(res, int)

    def test_getServerLimits(self):
        res = okex.getServerLimits()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getServerSymbols(self):
        res = okex.getServerSymbols()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getSymbolsLimits(self):
        res = okex.getSymbolsLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getMarketOrderbookTicker(self):
        res = okex.getMarketOrderbookTicker("ETH", "USDT", 0.1)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        res = okex.getMarketOrderbookDepth("ETH", "USDT", 5)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        res = okex.getMarketKline("ETH", "USDT", "1h",
                                  "2018-12-02T00:00:00.000Z",
                                  "2018-12-03T00:00:00.000Z")
        logger.debug(len(res))
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeFees(self):
        res = okex.getTradeFees()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOpen(self):
        # res = okex.getTradeOpen("", "")
        res = okex.getTradeOpen("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeHistory(self):
        res = okex.getTradeHistory("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeSucceed(self):
        res = okex.getTradeSucceed("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountBalances(self):
        res = okex.getAccountBalances()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountLimits(self):
        res = okex.getAccountLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountAssetBalance(self):
        res = okex.getAccountAssetBalance("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getAccountAssetDetail(self):
        res = okex.getAccountAssetDetail("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_createOrder(self):
        res = okex.createOrder("ETH", "USDT", "bid", 10, 0.001)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_checkOrder(self):
        res = okex.checkOrder("1771669234011136", "TRX", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancelOrder(self):
        res = okex.cancelOrder("1771669234011136", "TRX", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancelBatchOrder(self):
        res = okex.cancelBatchOrder(["1771669234011136", "1771614029560832"], "TRX", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_depositeAsset(self):
        pass

    def test_withdrawAsset(self):
        pass


if __name__ == "__main__":
    unittest.main()
