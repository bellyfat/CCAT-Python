# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

import unittest
from tests.coin.test_binance import TestBinance

# list of test_coin
# okex test items
test_okex = []
# binance test items
test_binance = [TestBinance("test_getConfig")]
# huobi test items
test_huobi = []
# gate test items
test_gate = []


# Begin Test
if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=1)

    # suite.addTests(test_okex)
    suite.addTests(test_binance)
    # suite.addTests(test_huobi)
    # suite.addTests(test_gate)

    runner.run(suite)
