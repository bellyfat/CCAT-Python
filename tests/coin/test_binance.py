# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

import unittest
from src.core.coin.lib.binance import Binance
from src.core.config import Config


class TestBinance(unittest.TestCase):

    def test_getConfig(self):
        conf = Config()
        print(conf)
        # binance = Binance(binanceStr.exchange,
        #                   binanceStr.api_key, binanceStr.api_secret)
        # res = binance.getConfig()
        # print(type(res))
        # self.assertEqual(res, binanceStr)

if __name__ == "__main__":
    test = TestBinance()
    test.test_getConfig()
