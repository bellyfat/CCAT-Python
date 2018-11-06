# -*- coding: utf-8 -*-

import unittest
from src.core.coin.lib.binance import Binance


class TestBinance(unittest.TestCase):

    def test_getConfig(self):
        binance = Binance()
        res = binance.getConfig()
        print(res)
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()
