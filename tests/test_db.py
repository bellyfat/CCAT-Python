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


    def test_getViewStatisticSignalTickerPairCurrentServer(self):
        res = db.getViewStatisticSignalTickerPairCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticSignalTickerPairCurrent(self):
        res = db.getViewStatisticSignalTickerPairCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticSignalTickerTraCurrentServer(self):
        res = db.getViewStatisticSignalTickerTraCurrentServer(['huobi'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticSignalTickerTraCurrent(self):
        res = db.getViewStatisticSignalTickerTraCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticSignalTickerDisCurrentServer(self):
        res = db.getViewStatisticSignalTickerDisCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticSignalTickerDisCurrent(self):
        res = db.getViewStatisticSignalTickerDisCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeSignalTickerPairCurrentServer(self):
        res = db.getViewJudgeSignalTickerPairCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeSignalTickerPairCurrent(self):
        res = db.getViewJudgeSignalTickerPairCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeSignalTickerTraCurrentServer(self):
        res = db.getViewJudgeSignalTickerTraCurrentServer(['huobi'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeSignalTickerTraCurrent(self):
        res = db.getViewJudgeSignalTickerTraCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeSignalTickerDisCurrentServer(self):
        res = db.getViewJudgeSignalTickerDisCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeSignalTickerDisCurrent(self):
        res = db.getViewJudgeSignalTickerDisCurrent()
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
        res = db.getAccountBalanceHistory()
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

    def test_getTradeBacktestHistoryServerOrder(self):
        res = db.getTradeBacktestHistoryServerOrder(['okex'],[1974405445330944, 1974402275218432])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOrderHistoryServerOrder(self):
        res = db.getTradeOrderHistoryServerOrder(['okex'],[1974405445330944, 1974402275218432])
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

    def test_getJudgeSignalTickerDis(self):
        res = db.getJudgeSignalTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delJudgeSignalTickerDis(self):
        db.delJudgeSignalTickerDis()
        res = db.getJudgeSignalTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getJudgeSignalTickerTra(self):
        res = db.getJudgeSignalTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delJudgeSignalTickerTra(self):
        db.delJudgeSignalTickerTra()
        res = db.getJudgeSignalTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getJudgeSignalTickerPair(self):
        res = db.getJudgeSignalTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delJudgeSignalTickerPair(self):
        db.delJudgeSignalTickerPair()
        res = db.getJudgeSignalTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticSignalTickerDis(self):
        res = db.getStatisticSignalTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticSignalTickerDis(self):
        db.delStatisticSignalTickerDis()
        res = db.getStatisticSignalTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticSignalTickerTra(self):
        res = db.getStatisticSignalTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticSignalTickerTra(self):
        db.delStatisticSignalTickerTra()
        res = db.getStatisticSignalTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticSignalTickerPair(self):
        res = db.getStatisticSignalTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticSignalTickerPair(self):
        db.delStatisticSignalTickerPair()
        res = db.getStatisticSignalTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertAccountBalanceHistory(self):
        db.insertAccountBalanceHistory("all")
        res = db.getAccountBalanceHistory()
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
        res = db.getInfoSymbol(['okex','huobi','binance'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertCreatTradeBacktestHistory(self):
        db.insertCreatTradeBacktestHistory("all", "ETH", "USDT", "bid", 70, 0.1)
        res = db.getTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSyncTradeOrderHistory(self):
        db.insertSyncTradeOrderHistory("all", "ETH", "USDT")
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertCreatTradeOrderHistory(self):
        db.insertCreatTradeOrderHistory("all", "ETH", "USDT", "bid", 70, 0.15)
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertCheckTradeOrderHistory(self):
        db.insertCheckTradeOrderHistory(["okex"], [1974405445330944, 1974402275218432], "ETH", "USDT")
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertCancleTradeOrderHistory(self):
        db.insertCancleTradeOrderHistory(["okex"], [1974718040778752, 1974776653094912], "ETH", "USDT")
        db.insertCancleTradeOrderHistory(["binance"], [151350838, 151356632], "ETH", "USDT")
        db.insertCancleTradeOrderHistory(["huobi"], [19369194055, 19369969707], "ETH", "USDT")
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertAccountWithdrawHistory(self):
        db.insertAccountWithdrawHistory("all")
        res = db.getAccountWithdrawHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertAccountWithdrawHistoryAsset(self):
        db.insertAccountWithdrawHistoryAsset("all", "USDT")
        res = db.getAccountWithdrawHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertInfoWithdraw(self):
        db.insertInfoWithdraw()
        res = db.getInfoWithdraw(["okex", "binance", "huobi"])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertJudgeSignalTickerDis(self):
        res = calc.calcJudgeSignalTickerDis(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertJudgeSignalTickerTra(self):
        res = calc.calcJudgeSignalTickerTra(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertJudgeSignalTickerPair(self):
        res = calc.calcJudgeSignalTickerPair(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticSignalTickerDis(self):
        res = calc.calcStatisticSignalTickerDis(["okex", "binance", "huobi"], 300)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticSignalTickerTra(self):
        res = calc.calcStatisticSignalTickerTra(["okex", "binance", "huobi"], 300)
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticSignalTickerPair(self):
        res = calc.calcStatisticSignalTickerPair(["okex", "binance", "huobi"], 300)
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
    TestDB("test_initDB"),
    TestDB("test_creatTables"),
    TestDB("test_creatViews"),
    TestDB("test_insertAccountBalanceHistory"),
    TestDB("test_insertAccountWithdrawHistory"),
    TestDB("test_insertAccountWithdrawHistoryAsset"),
    TestDB("test_insertInfoServer"),
    TestDB("test_insertInfoSymbol"),
    TestDB("test_insertInfoWithdraw"),
    TestDB("test_insertMarketDepth"),
    TestDB("test_insertMarketKline"),
    TestDB("test_insertMarketTicker"),
    TestDB("test_insertJudgeSignalTickerDis"),
    TestDB("test_insertJudgeSignalTickerTra"),
    TestDB("test_insertJudgeSignalTickerPair"),
    TestDB("test_insertCreatTradeBacktestHistory"),
    TestDB("test_insertSyncTradeOrderHistory"),
    # # TestDB("test_insertCreatTradeOrderHistory"),
    # # TestDB("test_insertCheckTradeOrderHistory"),
    # # TestDB("test_insertCancleTradeOrderHistory"),
    TestDB("test_insertStatisticSignalTickerDis"),
    TestDB("test_insertStatisticSignalTickerTra"),
    TestDB("test_insertStatisticSignalTickerPair"),
    TestDB("test_oneClickCancleOrders"),
    # # TestDB("test_oneClickTransToBaseCoin"),
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
    TestDB("test_getTradeBacktestHistoryServerOrder"),
    TestDB("test_getTradeOrderHistoryServerOrder"),
    TestDB("test_getJudgeSignalTickerDis"),
    TestDB("test_getJudgeSignalTickerTra"),
    TestDB("test_getJudgeSignalTickerPair"),
    TestDB("test_getStatisticSignalTickerDis"),
    TestDB("test_getStatisticSignalTickerTra"),
    TestDB("test_getStatisticSignalTickerPair"),
    TestDB("test_getViews"),
    TestDB("test_getViewStatisticSignalTickerPairCurrentServer"),
    TestDB("test_getViewStatisticSignalTickerPairCurrent"),
    TestDB("test_getViewStatisticSignalTickerTraCurrentServer"),
    TestDB("test_getViewStatisticSignalTickerTraCurrent"),
    TestDB("test_getViewStatisticSignalTickerDisCurrentServer"),
    TestDB("test_getViewStatisticSignalTickerDisCurrent"),
    TestDB("test_getViewJudgeSignalTickerPairCurrentServer"),
    TestDB("test_getViewJudgeSignalTickerPairCurrent"),
    TestDB("test_getViewJudgeSignalTickerTraCurrentServer"),
    TestDB("test_getViewJudgeSignalTickerTraCurrent"),
    TestDB("test_getViewJudgeSignalTickerDisCurrentServer"),
    TestDB("test_getViewJudgeSignalTickerDisCurrent"),
    TestDB("test_getViewMarketTickerCurrentPairServer"),
    TestDB("test_getViewMarketTickerCurrentPair"),
    TestDB("test_getViewMarketTickerCurrentTraServer"),
    TestDB("test_getViewMarketTickerCurrentTra"),
    TestDB("test_getViewMarketTickerCurrentDisServer"),
    TestDB("test_getViewMarketTickerCurrentDis"),
    TestDB("test_getViewMarketTickerCurrent"),
    TestDB("test_getViewMarketKlineCurrent"),
    TestDB("test_getViewAccountBalanceCurrent"),
    TestDB("test_getViewMarketTickerSymbol"),
    TestDB("test_getViewAccountWithdrawCurrent"),
    TestDB("test_getViewMarketSymbolPairs"),
    TestDB("test_getViewAccountBalanceCurrent"),
    TestDB("test_getViewInfoSymbolPairs"),
    TestDB("test_delJudgeSignalTickerDis"),
    TestDB("test_delJudgeSignalTickerTra"),
    TestDB("test_delJudgeSignalTickerPair"),
    TestDB("test_delStatisticSignalTickerDis"),
    TestDB("test_delStatisticSignalTickerTra"),
    TestDB("test_delStatisticSignalTickerPair"),
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_db)
    # run test
    runner.run(suite)
