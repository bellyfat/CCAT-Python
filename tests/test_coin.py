# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.getcwd())

from tests.coin.test_okex import TestOkex
from tests.coin.test_binance import TestBinance
from tests.coin.test_huobi import TestHuobi


# list of test_coin
# okex test items
test_okex = [
    # TestOkex("test_getConfig"),
    # TestOkex("test_setProxy"),
    # TestOkex("test_getServerTime"),
    # TestOkex("test_getServerLimits"),
    # TestOkex("test_getServerSymbols"),
    # TestOkex("test_getSymbolsLimits"),
    # TestOkex("test_getMarketOrderbookTicker"),
    # TestOkex("test_getMarketOrderbookDepth"),
    TestOkex("test_getMarketKline"),
    # TestOkex("test_getTradeFees"),
    # TestOkex("test_getTradeOpen"),
    # TestOkex("test_getTradeHistory"),
    # TestOkex("test_getTradeSucceed"),
    # TestOkex("test_getAccountBalances"),
    # TestOkex("test_getAccountLimits"),
    # TestOkex("test_getAccountAssetBalance"),
    # TestOkex("test_getAccountAssetDetail"),
    # # TestOkex("test_createOrder"),
    # TestOkex("test_checkOrder"),
    # TestOkex("test_cancelOrder"),
    # TestOkex("test_cancelBatchOrder"),
    # TestOkex("test_depositeAsset"),
    # TestOkex("test_withdrawAsset")
]
# binance test items
test_binance = [
    # TestBinance("test_getConfig"),
    # TestBinance("test_setProxy"),
    # TestBinance("test_getServerTime"),
    # TestBinance("test_getServerLimits"),
    # TestBinance("test_getServerSymbols"),
    # TestBinance("test_getSymbolsLimits"),
    # TestBinance("test_getMarketOrderbookTicker"),
    # TestBinance("test_getMarketOrderbookDepth"),
    TestBinance("test_getMarketKline"),
    # TestBinance("test_getTradeFees"),
    # TestBinance("test_getTradeOpen"),
    # TestBinance("test_getTradeHistory"),
    # TestBinance("test_getTradeSucceed"),
    # TestBinance("test_getAccountBalances"),
    # TestBinance("test_getAccountLimits"),
    # TestBinance("test_getAccountAssetBalance"),
    # TestBinance("test_getAccountAssetDetail"),
    # # TestBinance("test_createOrder"),
    # TestBinance("test_checkOrder"),
    # TestBinance("test_cancelOrder"),
    # TestBinance("test_cancelBatchOrder"),
    # TestBinance("test_depositeAsset"),
    # TestBinance("test_withdrawAsset")
]
# huobi test items
test_huobi = [
    # TestHuobi("test_getConfig"),
    # TestHuobi("test_setProxy"),
    # TestHuobi("test_getServerTime"),
    # TestHuobi("test_getServerLimits"),
    # TestHuobi("test_getServerSymbols"),
    # TestHuobi("test_getSymbolsLimits"),
    # TestHuobi("test_getMarketOrderbookTicker"),
    # TestHuobi("test_getMarketOrderbookDepth"),
    TestHuobi("test_getMarketKline"),
    # TestHuobi("test_getTradeFees"),
    # TestHuobi("test_getTradeOpen"),
    # TestHuobi("test_getTradeHistory"),
    # TestHuobi("test_getTradeSucceed"),
    # TestHuobi("test_getAccountBalances"),
    # TestHuobi("test_getAccountLimits"),
    # TestHuobi("test_getAccountAssetBalance"),
    # TestHuobi("test_getAccountAssetDetail"),
    # # TestHuobi("test_createOrder"),
    # TestHuobi("test_checkOrder"),
    # TestHuobi("test_cancelOrder"),
    # TestHuobi("test_cancelBatchOrder"),
    # TestHuobi("test_depositeAsset"),
    # TestHuobi("test_withdrawAsset")

]
# gate test items
test_gate = []


# Begin Test
if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    # suite.addTests(test_okex)
    # suite.addTests(test_binance)
    suite.addTests(test_huobi)
    suite.addTests(test_gate)
    # run test
    runner.run(suite)
