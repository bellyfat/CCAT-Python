# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.getcwd())

from src.core.db.db import DB
from src.core.util.log import Logger

db = DB()
logger = Logger()


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

    def test_getViewMarketTickerTraCurrent(self):
        res = db.getViewAccountWithdrawCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewMarketTickerDisCurrent(self):
        res = db.getViewAccountWithdrawCurrent()
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
        res = db.getViewMarketSymbolPairs(["okex", "binance"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewAccountBalanceCurrent(self):
        res = db.getViewAccountBalanceCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewInfoSymbolPairs(self):
        res = db.getViewInfoSymbolPairs(["okex", "binance"])
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
        res = db.getAccountBalanceHistory(["okex", "binance"])
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
        res = db.getInfoSymbol()
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
        res = db.getInfoWithdraw(["okex", "binance"])
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
        db.insertTradeBacktestHistory("all", "ETH", "USDT", "ask", 150, 0.1)
        res = db.getTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertTradeOrderHistory(self):
        db.insertTradeOrderHistory("binance", "ETH", "USDT", "ask", 150, 0.1)
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
        res = db.getInfoWithdraw(["okex", "binance"])
        logger.debug(res)
        self.assertIsInstance(res, list)


# list of test_db
# db test items
test_db = [
    TestDB("test_initDB"),
    TestDB("test_creatTables"),
    TestDB("test_getTables"),
    TestDB("test_getAccountBalanceHistory"),
    TestDB("test_getAccountWithdrawHistory"),
    TestDB("test_getMarketDepth"),
    TestDB("test_getMarketKline"),
    TestDB("test_getMarketTicker"),
    TestDB("test_getInfoServer"),
    TestDB("test_getInfoSymbol"),
    TestDB("test_getInfoWithdraw"),
    TestDB("test_getTradeBacktestHistory"),
    TestDB("test_getTradeOrderHistory"),
    TestDB("test_insertAccountBalanceHistory"),
    TestDB("test_insertAccountWithdrawHistory"),
    TestDB("test_insertMarketDepth"),
    TestDB("test_insertMarketKline"),
    TestDB("test_insertMarketTicker"),
    TestDB("test_insertInfoServer"),
    TestDB("test_insertInfoSymbol"),
    TestDB("test_insertInfoWithdraw"),
    TestDB("test_insertTradeBacktestHistory"),
    # TestDB("test_insertTradeOrderHistory"),
    TestDB("test_creatViews"),
    TestDB("test_getViews"),
    TestDB("test_getViewMarketTickerTraCurrent"),
    TestDB("test_getViewMarketTickerDisCurrent"),
    TestDB("test_getViewMarketTickerCurrent"),
    TestDB("test_getViewMarketKlineCurrent"),
    TestDB("test_getViewAccountBalanceCurrent"),
    TestDB("test_getViewMarketTickerSymbol"),
    TestDB("test_getViewAccountWithdrawCurrent"),
    TestDB("test_getViewMarketSymbolPairs"),
    TestDB("test_getViewAccountBalanceCurrent"),
    TestDB("test_getViewInfoSymbolPairs"),
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_db)
    # run test
    runner.run(suite)
