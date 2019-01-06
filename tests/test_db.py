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


    def test_getViewStatisticJudgeMarketTickerPairCurrentServer(self):
        res = db.getViewStatisticJudgeMarketTickerPairCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticJudgeMarketTickerPairCurrent(self):
        res = db.getViewStatisticJudgeMarketTickerPairCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticJudgeMarketTickerTraCurrentServer(self):
        res = db.getViewStatisticJudgeMarketTickerTraCurrentServer(['huobi'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticJudgeMarketTickerTraCurrent(self):
        res = db.getViewStatisticJudgeMarketTickerTraCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticJudgeMarketTickerDisCurrentServer(self):
        res = db.getViewStatisticJudgeMarketTickerDisCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewStatisticJudgeMarketTickerDisCurrent(self):
        res = db.getViewStatisticJudgeMarketTickerDisCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeMarketTickerPairCurrentServer(self):
        res = db.getViewJudgeMarketTickerPairCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeMarketTickerPairCurrent(self):
        res = db.getViewJudgeMarketTickerPairCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeMarketTickerTraCurrentServer(self):
        res = db.getViewJudgeMarketTickerTraCurrentServer(['huobi'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeMarketTickerTraCurrent(self):
        res = db.getViewJudgeMarketTickerTraCurrent()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeMarketTickerDisCurrentServer(self):
        res = db.getViewJudgeMarketTickerDisCurrentServer('huobi', 'binance')
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getViewJudgeMarketTickerDisCurrent(self):
        res = db.getViewJudgeMarketTickerDisCurrent()
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

    def test_delTradeBacktestHistory(self):
        db.delTradeBacktestHistory()
        res = db.getTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTradeOrderHistory(self):
        res = db.getTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delTradeOrderHistory(self):
        db.delTradeOrderHistory()
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

    def test_getJudgeMarketTickerDis(self):
        res = db.getJudgeMarketTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delJudgeMarketTickerDis(self):
        db.delJudgeMarketTickerDis()
        res = db.getJudgeMarketTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getJudgeMarketTickerTra(self):
        res = db.getJudgeMarketTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delJudgeMarketTickerTra(self):
        db.delJudgeMarketTickerTra()
        res = db.getJudgeMarketTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getJudgeMarketTickerPair(self):
        res = db.getJudgeMarketTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delJudgeMarketTickerPair(self):
        db.delJudgeMarketTickerPair()
        res = db.getJudgeMarketTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticTradeOrderHistory(self):
        res = db.getStatisticTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticTradeOrderHistory(self):
        db.delStatisticTradeOrderHistory()
        res = db.getStatisticTradeOrderHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticTradeBacktestHistory(self):
        res = db.getStatisticTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticTradeBacktestHistory(self):
        db.delStatisticTradeBacktestHistory()
        res = db.getStatisticTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticJudgeMarketTickerDis(self):
        res = db.getStatisticJudgeMarketTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticJudgeMarketTickerDis(self):
        db.delStatisticJudgeMarketTickerDis()
        res = db.getStatisticJudgeMarketTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticJudgeMarketTickerTra(self):
        res = db.getStatisticJudgeMarketTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticJudgeMarketTickerTra(self):
        db.delStatisticJudgeMarketTickerTra()
        res = db.getStatisticJudgeMarketTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getStatisticJudgeMarketTickerPair(self):
        res = db.getStatisticJudgeMarketTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_delStatisticJudgeMarketTickerPair(self):
        db.delStatisticJudgeMarketTickerPair()
        res = db.getStatisticJudgeMarketTickerPair()
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

    def test_insertJudgeMarketTickerDis(self):
        signal = calc.calcJudgeMarketTickerDis(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        db.insertJudgeMarketTickerDis(signal)
        res = db.getJudgeMarketTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertJudgeMarketTickerTra(self):
        res = calc.calcJudgeMarketTickerTra(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        db.insertJudgeMarketTickerTra(signal)
        res = db.getJudgeMarketTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertJudgeMarketTickerPair(self):
        signal = calc.calcJudgeMarketTickerPair(["okex", "binance", "huobi"], 0.001,
                                       resInfoSymbol)
        db.insertJudgeMarketTickerPair(signal)
        res = db.getJudgeMarketTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSignalTradeDis(self):
        signal = []
        db.insertSignalTradeDis(signal)
        res = db.getSignalTradeDis(['signal_id'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSignalTradeTra(self):
        signal = []
        db.insertSignalTradeTra(signal)
        res = db.getSignalTradeTra(['signal_id'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSignalTradePair(self):
        signal = []
        db.insertSignalTradePair(signal)
        res = db.getSignalTradePair(['signal_id'])
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticJudgeMarketTickerDis(self):
        statistic = calc.calcStatisticJudgeMarketTickerDis(["okex", "binance", "huobi"], 300)
        db.insertStatisticJudgeMarketTickerDis(statistic)
        res = db.getStatisticJudgeMarketTickerDis()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticJudgeMarketTickerTra(self):
        statistic = calc.calcStatisticJudgeMarketTickerTra(["okex", "binance", "huobi"], 300)
        db.insertStatisticJudgeMarketTickerTra(statistic)
        res = db.getStatisticJudgeMarketTickerTra()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticJudgeMarketTickerPair(self):
        statistic = calc.calcStatisticJudgeMarketTickerPair(["okex", "binance", "huobi"], 300)
        db.insertStatisticJudgeMarketTickerPair(statistic)
        res = db.getStatisticJudgeMarketTickerPair()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticTradeBacktestHistory(self):
        statistic = []
        db.insertStatisticTradeBacktestHistory(statistic)
        res = db.getStatisticTradeBacktestHistory()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertStatisticTradeOrderHistory(self):
        statistic = []
        db.insertStatisticTradeOrderHistory(statistic)
        res = db.getStatisticTradeOrderHistory()
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
    # TestDB("test_creatViews"),
    # TestDB("test_insertAccountBalanceHistory"),
    # TestDB("test_insertAccountWithdrawHistory"),
    # TestDB("test_insertAccountWithdrawHistoryAsset"),
    # TestDB("test_insertInfoServer"),
    # TestDB("test_insertInfoSymbol"),
    # TestDB("test_insertInfoWithdraw"),
    # TestDB("test_insertMarketDepth"),
    # TestDB("test_insertMarketKline"),
    # TestDB("test_insertMarketTicker"),
    # TestDB("test_insertJudgeMarketTickerDis"),
    # TestDB("test_insertJudgeMarketTickerTra"),
    # TestDB("test_insertJudgeMarketTickerPair"),
    TestDB("test_insertSignalTradeDis"),
    TestDB("test_insertSignalTradeTra"),
    TestDB("test_insertSignalTradePair"),
    # TestDB("test_insertCreatTradeBacktestHistory"),
    # TestDB("test_insertSyncTradeOrderHistory"),
    # # # TestDB("test_insertCreatTradeOrderHistory"),
    # # # TestDB("test_insertCheckTradeOrderHistory"),
    # # # TestDB("test_insertCancleTradeOrderHistory"),
    # TestDB("test_insertStatisticJudgeMarketTickerDis"),
    # TestDB("test_insertStatisticJudgeMarketTickerTra"),
    # TestDB("test_insertStatisticJudgeMarketTickerPair"),
    TestDB("test_insertStatisticTradeBacktestHistory"),
    TestDB("test_insertStatisticTradeOrderHistory"),
    # TestDB("test_oneClickCancleOrders"),
    # # # TestDB("test_oneClickTransToBaseCoin"),
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
    # TestDB("test_getTradeBacktestHistoryServerOrder"),
    # TestDB("test_getTradeOrderHistoryServerOrder"),
    # TestDB("test_getJudgeMarketTickerDis"),
    # TestDB("test_getJudgeMarketTickerTra"),
    # TestDB("test_getJudgeMarketTickerPair"),
    # TestDB("test_getStatisticJudgeMarketTickerDis"),
    # TestDB("test_getStatisticJudgeMarketTickerTra"),
    # TestDB("test_getStatisticJudgeMarketTickerPair"),
    TestDB("test_getStatisticTradeBacktestHistory"),
    TestDB("test_getStatisticTradeOrderHistory"),
    # TestDB("test_getViews"),
    # TestDB("test_getViewStatisticJudgeMarketTickerPairCurrentServer"),
    # TestDB("test_getViewStatisticJudgeMarketTickerPairCurrent"),
    # TestDB("test_getViewStatisticJudgeMarketTickerTraCurrentServer"),
    # TestDB("test_getViewStatisticJudgeMarketTickerTraCurrent"),
    # TestDB("test_getViewStatisticJudgeMarketTickerDisCurrentServer"),
    # TestDB("test_getViewStatisticJudgeMarketTickerDisCurrent"),
    # TestDB("test_getViewJudgeMarketTickerPairCurrentServer"),
    # TestDB("test_getViewJudgeMarketTickerPairCurrent"),
    # TestDB("test_getViewJudgeMarketTickerTraCurrentServer"),
    # TestDB("test_getViewJudgeMarketTickerTraCurrent"),
    # TestDB("test_getViewJudgeMarketTickerDisCurrentServer"),
    # TestDB("test_getViewJudgeMarketTickerDisCurrent"),
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
    # TestDB("test_delJudgeMarketTickerDis"),
    # TestDB("test_delJudgeMarketTickerTra"),
    # TestDB("test_delJudgeMarketTickerPair"),
    TestDB("test_delTradeBacktestHistory"),
    TestDB("test_delTradeOrderHistory"),
    # TestDB("test_delStatisticJudgeMarketTickerDis"),
    # TestDB("test_delStatisticJudgeMarketTickerTra"),
    # TestDB("test_delStatisticJudgeMarketTickerPair"),
    TestDB("test_delStatisticTradeBacktestHistory"),
    TestDB("test_delStatisticTradeOrderHistory"),
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_db)
    # run test
    runner.run(suite)
