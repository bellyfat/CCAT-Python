# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.getcwd())

from src.core.coin.huobi import Huobi
from src.core.config import Config
from src.core.util.log import Logger


# proxies
_proxies = Config()._Proxies_url if Config()._Proxies_proxies else None
# Huobi
_Huobi_exchange = Config()._Huobi_exchange
_Huobi_api_key = Config()._Huobi_api_key
_Huobi_api_secret = Config()._Huobi_api_secret
_Huobi_acct_id = Config()._Huobi_acct_id

huobi = Huobi(_Huobi_exchange, _Huobi_api_key, _Huobi_api_secret, _Huobi_acct_id,
            _proxies)
logger = Logger()


class TestHuobi(unittest.TestCase):
    def test_getConfig(self):
        res = huobi.getConfig()
        logger.debug(res)
        self.assertEqual(res["exchange"], _Huobi_exchange)

    def test_setProxy(self):
        huobi.setProxy(_proxies)
        res = huobi.getConfig()
        logger.debug(res)
        self.assertEqual(res["proxies"], _proxies)

    def test_getServerTime(self):
        res = huobi.getServerTime()
        logger.debug(res)
        self.assertIsInstance(res, int)

    def test_getServerLimits(self):
        res = huobi.getServerLimits()
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getServerSymbols(self):
        res = huobi.getServerSymbols()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getSymbolsLimits(self):
        res = huobi.getSymbolsLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getMarketOrderbookTicker(self):
        res = huobi.getMarketOrderbookTicker("ETH", "USDT", 0.1)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketOrderbookDepth(self):
        res = huobi.getMarketOrderbookDepth("ETH", "USDT", 100)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getMarketKline(self):
        res = huobi.getMarketKline("ETH", "USDT", "1h",
                                  "2018-12-02T00:00:00.000Z",
                                  "2018-12-03T00:00:00.000Z")
        logger.debug(len(res))
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeFees(self):
        res = huobi.getTradeFees()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOpen(self):
        # res = huobi.getTradeOpen("", "")
        res = huobi.getTradeOpen("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeHistory(self):
        res = huobi.getTradeHistory("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeSucceed(self):
        res = huobi.getTradeSucceed("ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountBalances(self):
        res = huobi.getAccountBalances()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountDetail(self):
        res = huobi.getAccountDetail()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountLimits(self):
        res = huobi.getAccountLimits()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountAssetBalance(self):
        res = huobi.getAccountAssetBalance("USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_getAccountAssetDetail(self):
        res = huobi.getAccountAssetDetail("ETH")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_createOrder(self):
        res = huobi.createOrder("ETH", "USDT", "bid", 10, 0.05)
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_checkOrder(self):
        res = huobi.checkOrder("18252501002", "ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancelOrder(self):
        res = huobi.cancelOrder("18252501002", "ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, dict)

    def test_cancelBatchOrder(self):
        res = huobi.cancelBatchOrder(["18252501002", "18253191905"],"ETH", "USDT")
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_oneClickCancleOrders(self):
        res = huobi.oneClickCancleOrders()
        logger.debug(res)
        self.assertIsInstance(res, bool)

    def test_oneClickTransToBaseCoin(self):
        res = huobi.oneClickTransToBaseCoin("USDT")
        logger.debug(res)
        self.assertIsInstance(res, bool)

    def test_depositeAsset(self):
        pass

    def test_withdrawAsset(self):
        pass

if __name__ == "__main__":
    unittest.main()
