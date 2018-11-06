# -*- coding: utf-8 -*-

import unittest
from coin.test_binance import TestBinance

if __name__ == '__main__':
    suite = unittest.TestSuite()

    test_okex = []

    test_binance = [TestBinance("test_getConfig"),
                    TestBinance("test_minus"),
                    TestBinance("test_divide")]

    test_huobi = []
    test_gate = []

    # suite.addTests(test_okex)
    suite.addTests(test_binance)
    # suite.addTests(test_huobi)
    # suite.addTests(test_gate)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
