# -*- coding: utf-8 -*-

import os
import time
from threading import Thread, current_thread

import pandas as pd

from src.core.config import Config
from src.core.db.db import DB
from src.core.engine.enums import (ACTIVE_STATUS_EVENT, DONE_STATUS_EVENT,
                                   QUEUE_STATUS_EVENT)
from src.core.util.exceptions import (ApplicationException, DBException,
                                      EngineException)
from src.core.util.helper import timestamp_to_isoformat, utcnow_timestamp
from src.core.util.log import Logger


# util class
class Util(object):
    def __init__(self, eventEngine, sender):
        # Config init
        # Main Settings
        self._exchanges = Config()._Main_exchanges
        self._excludeCoins = Config()._Main_excludeCoins
        self._baseCoin = Config()._Main_baseCoin
        self._marketDepthLimit = Config()._Main_marketDepthLimit
        self._marketTickerAggStep = Config()._Main_marketTickerAggStep
        self._symbolStartBaseCoin = Config()._Main_symbolStartBaseCoin
        self._symbolEndBaseCoin = Config()._Main_symbolEndBaseCoin
        self._symbolEndTimeout = Config()._Main_symbolEndTimeout
        self._apiEpochSaveBound = Config()._Main_apiEpochSaveBound
        self._apiResultEpoch = Config()._Main_apiResultEpoch
        # ServerLimit
        self._serverLimits = None
        # Engine
        self._engine = eventEngine
        self._sender = sender
        # logger
        self._logger = Logger()

    # 初始化数据库
    def initDB(self):
        self._logger.debug("src.core.util.util.Util.initDB")
        try:
            db = DB()
            db.initDB()
            db.creatTables()
            db.creatViews()
        except (DBException, Exception) as err:
            errStr = "src.core.util.util.Util.initDB: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Info数据
    def threadInsertInfoServer(self, server):
        try:
            db = DB()
            db.insertInfoServer(server)
        except (DBException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoServer: {server=%s}, exception err=%s" % (
                server, err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    def threadInsertInfoSymbol(self, server):
        try:
            db = DB()
            db.insertInfoSymbol(server)
        except (DBException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoSymbol: {server=%s}, exception err=%s" % (
                server, err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    def threadInsertInfoWithdraw(self, server):
        try:
            db = DB()
            db.insertInfoWithdraw(server)
        except (DBException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoWithdraw: {server=%s}, exception err=%s" % (
                server, err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    def initDBInfo(self):
        self._logger.debug("src.core.util.util.Util.initDBInfo")
        try:
            tds = []
            for server in self._exchanges:
                td = Thread(
                    target=self.threadInsertInfoServer,
                    name="%s-threadInsertInfoServer" % server,
                    args=([server], ))
                tds.append(td)
                td.start()
                td = Thread(
                    target=self.threadInsertInfoSymbol,
                    name="%s-threadInsertInfoSymbol" % server,
                    args=([server], ))
                tds.append(td)
                td.start()
                td = Thread(
                    target=self.threadInsertInfoWithdraw,
                    name="%s-threadInsertInfoWithdraw" % server,
                    args=([server], ))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except Exception as err:
            errStr = "src.core.util.util.Util.initDBInfo: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # ServerLimit数据
    def initServerLimits(self):
        self._logger.debug("src.core.util.util.Util.initServerLimits")
        try:
            db = DB()
            res = db.getInfoServer()
            self._serverLimits = pd.DataFrame(res).set_index(["server"],
                                                             inplace=False)
        except (DBException, Exception) as err:
            errStr = "src.core.util.util.Util.initServerLimits: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Balance 事件
    def updateDBAccountBalance(self, async=True, timeout=10):
        self._logger.debug("src.core.util.util.Util.updateDBAccountBalance")
        try:
            id = self._sender.sendListenAccountBalanceEvent(self._exchanges)
            if not async:
                st = self._engine.getEventStatus(id)
                startTime = time.time()
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.warn(
                        "src.core.util.util.Util.updateDBAccountBalance: Timeout Error, waiting for event handler result timeout."
                    )
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBAccountBalance: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Withdraw 事件
    def threadSendListenAccountWithdrawEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {\nthread: %s, \nres: \n%s, \nepoch: %s, \nasync: %s, \ntimeout: %s}"
            % (current_thread().name, res, epoch, async, timeout))
        ids = []
        for r in res:
            time.sleep(epoch)
            id = self._sender.sendListenAccountWithdrawEvent(
                r["server"], r["asset"])
            ids.append(id)
        if not async:
            st = QUEUE_STATUS_EVENT
            startTime = time.time()
            for id in ids:
                st = self._engine.getEventStatus(id)
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {\nthread: %s, \nres: \n%s, \nepoch: %s, \nasync: %s, \ntimeout: %s}, Timeout Error, waiting for event handler result timeout."
                    % (current_thread().name, res, epoch, async, timeout))

    def updateDBAccountWithdraw(self, async=True, timeout=10):
        self._logger.debug("src.core.util.util.Util.updateDBAccountWithdraw")
        try:
            db = DB()
            ####################################################################
            # fully update: bugs remain {okex res: invlid asset}
            ###################################################################
            # tds = []
            # for server in self._exchanges:
            #     epoch = float(self._apiEpochSaveBound) / float(
            #         self._serverLimits.at[server, "info_second"])
            #     res = db.getInfoWithdraw([server])
            #     td = Thread(
            #         target=self.threadSendListenAccountWithdrawEvent,
            #         name="%s-thread" % server,
            #         args=(res, epoch, async, timeout))
            #     tds.append(td)
            #     td.start()
            # for td in tds:
            #     td.join()
            ####################################################################
            # fast update
            ####################################################################
            tds = []
            for server in self._exchanges:
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "info_second"])
                res = db.getAccountBalanceHistory([server])
                td = Thread(
                    target=self.threadSendListenAccountWithdrawEvent,
                    name="%s-threadSendListenAccountWithdrawEvent" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBAccountWithdraw: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market Depth 事件
    def threadSendListenMarketDepthEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketDepthEvent: {\nthread: %s, \nres: \n%s, \nepoch: %s, \nasync: %s, \ntimeout: %s}"
            % (current_thread().name, res, epoch, async, timeout))
        ids = []
        for r in res:
            time.sleep(epoch)
            id = self._sender.sendListenMarketDepthEvent(
                r["server"], r["fSymbol"], r["tSymbol"],
                self._marketDepthLimit)
            ids.append(id)
        if not async:
            st = QUEUE_STATUS_EVENT
            startTime = time.time()
            for id in ids:
                st = self._engine.getEventStatus(id)
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenMarketDepthEvent: {\nthread: %s, \nres: \n%s, \nepoch: %s, \nasync: %s, \ntimeout: %s}, Timeout Error, waiting for event handler result timeout."
                    % (current_thread().name, res, epoch, async, timeout))

    def updateDBMarketDepth(self, async=True, timeout=10):
        self._logger.debug("src.core.util.util.Util.updateDBMarketDepth")
        try:
            db = DB()
            tds = []
            for server in self._exchanges:
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewMarketSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketDepthEvent,
                    name="%s-threadSendListenMarketDepthEvent" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketDepth: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market Kline 事件
    def threadSendListenMarketKlineEvent(self, res, start, end, epoch, async,
                                         timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketKlineEvent: {\nthread: %s, \nres: \n%s, start: %s, end: %s, \nepoch: %s, \nasync: %s, \ntimeout: %s}"
            % (current_thread().name, res, start, end, epoch, async, timeout))
        ids = []
        for r in res:
            time.sleep(epoch)
            id = self._sender.sendListenMarketKlineEvent(
                r["server"], r["fSymbol"], r["tSymbol"], "1h", start, end)
            ids.append(id)
        if not async:
            st = QUEUE_STATUS_EVENT
            startTime = time.time()
            for id in ids:
                st = self._engine.getEventStatus(id)
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenMarketKlineEvent: {\nthread: %s, \nres: \n%s, start: %s, end: %s, \nepoch: %s, \nasync: %s, \ntimeout: %s}, Timeout Error, waiting for event handler result timeout."
                    % (current_thread().name, res, start, end, epoch, async,
                       timeout))

    def updateDBMarketKline(self, async=True, timeout=10):
        self._logger.debug("src.core.util.util.Util.updateDBMarketKline")
        try:
            db = DB()
            db.delMarketKline()
            end = utcnow_timestamp() - 12 * 60 * 60 * 1000
            start = end - 24 * 60 * 60 * 1000
            tds = []
            for server in self._exchanges:
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewInfoSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketKlineEvent,
                    name="%s-threadSendListenMarketKlineEvent" % server,
                    args=(res, timestamp_to_isoformat(start),
                          timestamp_to_isoformat(end), epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketKline: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market ticker 事件
    def threadSendListenMarketTickerEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketTickerEvent: {\nthread: %s, \nres: \n%s, \nepoch: %s, \nasync: %s, \ntimeout: %s}"
            % (current_thread().name, res, epoch, async, timeout))
        ids = []
        for r in res:
            db = DB()
            aggDepth = db.getViewMarketSymbolPairsAggDepth(
                self._exchanges, r["fSymbol"],
                r["tSymbol"])[0]["aggDepth"] * self._marketTickerAggStep
            time.sleep(epoch)
            id = self._sender.sendListenMarketTickerEvent(
                r["server"], r["fSymbol"], r["tSymbol"], aggDepth)
            ids.append(id)
        if not async:
            st = QUEUE_STATUS_EVENT
            startTime = time.time()
            for id in ids:
                st = self._engine.getEventStatus(id)
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenMarketTickerEvent: Timeout Error, waiting for event handler result timeout."
                )

    def updateDBMarketTicker(self, async=True, timeout=10):
        self._logger.debug("src.core.util.util.Util.updateDBMarketTicker")
        try:
            db = DB()
            tds = []
            for server in self._exchanges:
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewMarketSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketTickerEvent,
                    name="%s-threadSendListenMarketTickerEvent" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (Exception, DBException) as err:
            errStr = "src.core.util.util.Util.updateDBMarketTicker: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Judge 事件
    def updateDBJudgeMarketKline(self):
        pass

    def updateDBJudgeMarketTicker(self, async=True, timeout=10):
        self._logger.debug("src.core.util.util.Util.updateDBJudgeMarketTicker")
        try:
            id = self._sender.sendJudgeMarketTickerEvent(
                self._excludeCoins, self._baseCoin, self._symbolStartBaseCoin,
                self._symbolEndBaseCoin, self._symbolEndTimeout)
            if not async:
                st = self._engine.getEventStatus(id)
                startTime = time.time()
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.warn(
                        "src.core.util.util.Util.updateDBJudgeMarketTicker: Timeout Error, waiting for event handler result timeout."
                    )
        except Exception as err:
            errStr = "src.core.util.util.Util.updateDBJudgeMarketTicker: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Backtest 事件
    def updateDBBacktest(self):
        pass

    # Order 事件
    def updateDBOrderConfirm(self):
        pass

    def updateDBOrderTracker(self):
        pass

    def updateDBOrderCancle(self):
        pass

    # Statistic 事件
    def updateDBStatisticBacktest(self):
        pass

    def updateDBStatisticOrder(self):
        pass

    # Util 紧急功能
    # 一键 cancle 撤销所有订单
    def oneClickCancleOrders(self):
        pass

    # 一键 order 交易所有币到baseCoin
    def oneClickOrderBaseCoin(self):
        pass

    # 一键 withdraw baseCoin 提币到冷钱包
    def oneClickWithdrawBaseCoin(self):
        pass

    # 一键 deposite baseCoin 充币到交易所钱包
    def oneClickDepositeBaseCoin(self):
        pass
