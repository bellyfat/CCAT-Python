# -*- coding: utf-8 -*-

import os
import sys
import unittest

from tests.coin.test_binance import TestBinance

sys.path.append(os.getcwd())


# list of test_coin
# okex test items
test_okex = []
# binance test items
test_binance = [
    TestBinance("test_getConfig"),
    TestBinance("test_setProxy"),
    TestBinance("test_getServerTime"),
    TestBinance("test_getServerLimits"),
    TestBinance("test_getServerSymbols")
]
# huobi test items
test_huobi = []
# gate test items
test_gate = []


# Begin Test
if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_okex)
    suite.addTests(test_binance)
    suite.addTests(test_huobi)
    suite.addTests(test_gate)
    # run test
    runner.run(suite)
