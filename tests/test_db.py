# -*- coding: utf-8 -*-

import os
import sys
import unittest
import pandas as pd

sys.path.append(os.getcwd())

from src.core.calc.calc import Calc
from src.core.db.db import DB
from src.core.util.log import Logger


db = DB()
calc = Calc()
logger = Logger()
resInfoSymbol = pd.DataFrame(db.getInfoSymbol(['okex','binance','huobi']))


class TestDB(unittest.TestCase):
    def test_initDB(self):
        db.initDB()
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViews(self):
        res = db.getViews()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_creatViews(self):
        db.creatViews()
        res = db.getViews()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrentPairServer(self):
        res = db.getViewMarketTickerCurrentPairServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrentPair(self):
        res = db.getViewMarketTickerCurrentPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrentTraServer(self):
        res = db.getViewMarketTickerCurrentTraServer(
            ['okex', 'huobi', 'binance'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrentTra(self):
        res = db.getViewMarketTickerCurrentTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrentDisServer(self):
        res = db.getViewMarketTickerCurrentDisServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrentDis(self):
        res = db.getViewMarketTickerCurrentDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerCurrent(self):
        res = db.getViewAccountWithdrawCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketKlineCurrent(self):
        res = db.getViewAccountWithdrawCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerSymbol(self):
        res = db.getViewAccountWithdrawCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewAccountWithdrawCurrent(self):
        res = db.getViewAccountWithdrawCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketSymbolPairs(self):
        res = db.getViewMarketSymbolPairs(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewAccountBalanceCurrent(self):
        res = db.getViewAccountBalanceCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewInfoSymbolPairs(self):
        res = db.getViewInfoSymbolPairs(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTables(self):
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_creatTables(self):
        db.creatTables()
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountBalanceHistory(self):
        res = db.getAccountBalanceHistory(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getMarketDepth(self):
        res = db.getMarketDepth()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getMarketKline(self):
        res = db.getMarketKline()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getMarketTicker(self):
        res = db.getMarketTicker()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getInfoServer(self):
        res = db.getInfoServer()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getInfoSymbol(self):
        res = db.getInfoSymbol(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeBacktestHistory(self):
        res = db.getTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOrderHistory(self):
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountWithdrawHistory(self):
        res = db.getAccountWithdrawHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getInfoWithdraw(self):
        res = db.getInfoWithdraw(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertAccountBalanceHistory(self):
        db.insertAccountBalanceHistory("all")
        res = db.getAccountBalanceHistory(["okex"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertMarketDepth(self):
        db.insertMarketDepth("all", "ETH", "USDT")
        res = db.getMarketDepth()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertMarketKline(self):
        db.insertMarketKline("all", "BTC", "USDT", "1m",
                             "2018-11-17T00:00:00.000Z",
                             "2018-11-17T01:00:00.000Z")
        res = db.getMarketKline()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertMarketTicker(self):
        db.insertMarketTicker("all", "BTC", "USDT")
        res = db.getMarketTicker()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertInfoServer(self):
        db.insertInfoServer()
        res = db.getInfoServer()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertInfoSymbol(self):
        db.insertInfoSymbol()
        res = db.getInfoSymbol()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertTradeBacktestHistory(self):
        db.insertTradeBacktestHistory("all", "ETH", "USDT", "bid", 70, 0.1)
        res = db.getTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertTradeOrderHistory(self):
        db.insertTradeOrderHistory("all", "ETH", "USDT")
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_updateCreatTradeOrderHistory(self):
        db.updateCreatTradeOrderHistory("all", "ETH", "USDT", "bid", 70, 0.15)
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_updateCheckTradeOrderHistory(self):
        db.updateCheckTradeOrderHistory("okex", [1974405445330944, 1974402275218432], "ETH", "USDT")
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_updateCancleTradeOrderHistory(self):
        db.updateCancleTradeOrderHistory("okex", [1974718040778752, 1974776653094912], "ETH", "USDT")
        db.updateCancleTradeOrderHistory("binance", [151350838, 151356632], "ETH", "USDT")
        db.updateCancleTradeOrderHistory("huobi", [19369194055, 19369969707], "ETH", "USDT")
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertAccountWithdrawHistory(self):
        db.insertAccountWithdrawHistory("all", "USDT")
        res = db.getAccountWithdrawHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertInfoWithdraw(self):
        db.insertInfoWithdraw()
        res = db.getInfoWithdraw(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSignalTickerDis(self):
        res = calc.calcSignalTickerDis(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSignalTickerTra(self):
        res = calc.calcSignalTickerTra(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSignalTickerPair(self):
        res = calc.calcSignalTickerPair(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_oneClickCancleOrders(self):
        res = db.oneClickCancleOrders(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, bool)

    def test_oneClickTransToBaseCoin(self):
        res = db.oneClickTransToBaseCoin(["okex", "binance", "huobi"], 'USDT')
        logger.debug(res)
        self.assertIsInstance(res, bool)

# list of test_db
# db test items
test_db = [
    # TestDB("test_initDB"),
    # TestDB("test_creatTables"),
    # TestDB("test_getTables"),
    # TestDB("test_getAccountBalanceHistory"),
    # TestDB("test_getAccountWithdrawHistory"),
    # TestDB("test_getMarketDepth"),
    # TestDB("test_getMarketKline"),
    # TestDB("test_getMarketTicker"),
    # TestDB("test_getInfoServer"),
    # TestDB("test_getInfoSymbol"),
    # TestDB("test_getInfoWithdraw"),
    # TestDB("test_getTradeBacktestHistory"),
    # TestDB("test_getTradeOrderHistory"),
    # TestDB("test_insertAccountBalanceHistory"),
    # TestDB("test_insertAccountWithdrawHistory"),
    # TestDB("test_insertMarketDepth"),
    # TestDB("test_insertMarketKline"),
    # TestDB("test_insertMarketTicker"),
    # TestDB("test_insertInfoServer"),
    # TestDB("test_insertInfoSymbol"),
    # TestDB("test_insertInfoWithdraw"),
    # TestDB("test_insertSignalTickerDis"),
    # TestDB("test_insertSignalTickerTra"),
    # TestDB("test_insertSignalTickerPair"),
    # TestDB("test_insertTradeBacktestHistory"),
    # TestDB("test_insertTradeOrderHistory"),
    # # TestDB("test_updateCreatTradeOrderHistory"),
    # TestDB("test_updateCheckTradeOrderHistory"),
    # TestDB("test_updateCancleTradeOrderHistory"),
    TestDB("test_oneClickCancleOrders"),
    # TestDB("test_oneClickTransToBaseCoin"),
    # TestDB("test_creatViews"),
    # TestDB("test_getViews"),
    # TestDB("test_getViewMarketTickerCurrentPairServer"),
    # TestDB("test_getViewMarketTickerCurrentPair"),
    # TestDB("test_getViewMarketTickerCurrentTraServer"),
    # TestDB("test_getViewMarketTickerCurrentTra"),
    # TestDB("test_getViewMarketTickerCurrentDisServer"),
    # TestDB("test_getViewMarketTickerCurrentDis"),
    # TestDB("test_getViewMarketTickerCurrent"),
    # TestDB("test_getViewMarketKlineCurrent"),
    # TestDB("test_getViewAccountBalanceCurrent"),
    # TestDB("test_getViewMarketTickerSymbol"),
    # TestDB("test_getViewAccountWithdrawCurrent"),
    # TestDB("test_getViewMarketSymbolPairs"),
    # TestDB("test_getViewAccountBalanceCurrent"),
    # TestDB("test_getViewInfoSymbolPairs"),
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_db)
    # run test
    runner.run(suite)
