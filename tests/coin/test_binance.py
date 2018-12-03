# -*- coding: utf-8 -*-

import os
import sys
import unittest

from src.core.coin.binance import Binance
from src.core.config import Config
from src.core.util.log import Logger

sys.path.append(os.getcwd())

# proxies
_proxies = Config()._Proxies_url if Config()._Proxies_proxies else None
# Binance
_Binance_exchange = Config()._Binance_exchange
_Binance_api_key = Config()._Binance_api_key
_Binance_api_secret = Config()._Binance_api_secret

binance = Binance(_Binance_exchange, _Binance_api_key, _Binance_api_secret,
                  _proxies)
logger = Logger()


class TestBinance(unittest.TestCase):
    def test_getConfig(self):
        res = binance.getConfig()
        logger.debug(res)
        self.assertEqual(res["exchange"], _Binance_exchange)

    def test_setProxy(self):
        binance.setProxy(_proxies)
        res = binance.getConfig()
        logger.debug(res)
        self.assertEqual(res["proxies"], _proxies)

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
        res = binance.getMarketOrderbookTicker("ETH", "USDT", 0.1)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        res = binance.getMarketOrderbookDepth("ETH", "USDT", 5)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        res = binance.getMarketKline("ETH", "USDT", "1h",
                                     "2018-12-02T00:00:00.000Z",
                                     "2018-12-03T00:00:00.000Z")
        logger.debug(len(res))
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeFees(self):
        res = binance.getTradeFees()
        # res = binance.getTradeFees(symbol="ETHUSDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOpen(self):
        # res = binance.getTradeOpen("", "")
        res = binance.getTradeOpen("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeHistory(self):
        res = binance.getTradeHistory("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeSucceed(self):
        res = binance.getTradeSucceed("ETH", "USDT")
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

    def test_createOrder(self):
        res = binance.createOrder("ETH", "USDT", "bid", 10, 0.05)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_checkOrder(self):
        res = binance.checkOrder("102624667", "ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancelOrder(self):
        res = binance.cancelOrder("135080289", "ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancelBatchOrder(self):
        res = binance.cancelBatchOrder(["134809076", "134809137"], "ETH",
                                       "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_depositeAsset(self):
        pass

    def test_withdrawAsset(self):
        pass


if __name__ == "__main__":
    unittest.main()
