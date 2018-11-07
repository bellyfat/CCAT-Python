# -*- coding: utf-8 -*-

import unittest

from src.core.coin.lib.binance import Binance
from src.core.config import Config


class TestBinance(unittest.TestCase):
    proxies = Config()._proxies
    binanceConf = Config()._binance

    binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                      binanceConf["api_secret"], proxies["url"])

    def test_getConfig(self):
        res = self.binance.getConfig()
        self.assertEqual(res["exchange"], self.binanceConf["exchange"])
        self.assertEqual(res["api_key"], self.binanceConf["api_key"])
        self.assertEqual(res["api_secret"], self.binanceConf["api_secret"])
        self.assertEqual(res["proxies"], self.proxies["url"])


if __name__ == "__main__":
    print("Error: Should  be called form tests/test_coin.py")
