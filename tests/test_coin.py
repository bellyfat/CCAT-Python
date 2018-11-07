# -*- coding: utf-8 -*-

import unittest
from tests.coin.test_binance import TestBinance


class TestCoin():
    def _init_(self):
        self.test_okex = []
        self.test_binance = [TestBinance("test_getConfig"),
                             TestBinance("test_getConfig"),
                             TestBinance("test_getConfig")]
        self.test_huobi = []
        self.test_gate = []

    def run(self):
        suite = unittest.TestSuite()
        # suite.addTests(self.test_okex)
        suite.addTests(self.test_binance)
        # suite.addTests(self.test_huobi)
        # suite.addTests(self.test_gate)

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
