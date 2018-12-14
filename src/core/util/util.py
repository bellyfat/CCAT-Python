# -*- coding: utf-8 -*-

import os
import time
from threading import Thread, current_thread

import pandas as pd

from src.core.config import Config
from src.core.db.db import DB
from src.core.engine.enums import (ACTIVE_STATUS_EVENT, DONE_STATUS_EVENT,
                                   QUEUE_STATUS_EVENT)
from src.core.util.exceptions import (DBException, EngineException,
                                      UtilException)
from src.core.util.helper import timestamp_to_isoformat, utcnow_timestamp
from src.core.util.log import Logger


# util class
class Util(object):
    def __init__(self, eventEngine, sender):
        # Config init
        # Main Settings
        self._types = Config()._Main_types
        self._exchanges = Config()._Main_exchanges
        self._excludeCoins = Config()._Main_excludeCoins
        self._baseCoin = Config()._Main_baseCoin
        self._marketDepthLimit = Config()._Main_marketDepthLimit
        self._marketTickerAggStep = Config()._Main_marketTickerAggStep
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
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.initDB: %s" % UtilException(err)
            raise UtilException(err)

    # Info数据
    def threadInsertInfoServer(self, server):
        try:
            db = DB()
            db.insertInfoServer(server)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoServer: {thread=%s, server=%s}, exception err=%s" % (
                current_thread().name, server, UtilException(err))
            self._logger.critical(errStr)

    def threadInsertInfoSymbol(self, server):
        try:
            db = DB()
            db.insertInfoSymbol(server)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoSymbol: {thread=%s, server=%s}, exception err=%s" % (
                current_thread().name, server, UtilException(err))
            self._logger.critical(errStr)

    def threadInsertInfoWithdraw(self, server):
        try:
            db = DB()
            db.insertInfoWithdraw(server)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoWithdraw: {thread=%s, server=%s}, exception err=%s" % (
                current_thread().name, server, UtilException(err))
            self._logger.critical(errStr)

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
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.initDBInfo: %s" % UtilException(
                err)
            raise UtilException(err)

    # ServerLimit数据
    def initServerLimits(self):
        self._logger.debug("src.core.util.util.Util.initServerLimits")
        try:
            db = DB()
            res = db.getInfoServer()
            self._serverLimits = pd.DataFrame(res).set_index(["server"],
                                                             inplace=False)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.initServerLimits: %s" % UtilException(
                err)
            raise UtilException(err)

    # Account Balance 事件
    def updateDBAccountBalance(self, async=True, timeout=30):
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
                        "src.core.util.util.Util.updateDBAccountBalance: err=Timeout Error, waiting for event handler result timeout."
                    )
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBAccountBalance: %s" % UtilException(
                err)
            raise UtilException(err)

    # Account Withdraw 事件
    def threadSendListenAccountWithdrawEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
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
                    "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, err=Timeout Error, waiting for event handler result timeout."
                    % (current_thread().name, res, epoch, async, timeout))

    def updateDBAccountWithdraw(self, async=True, timeout=30):
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
            errStr = "src.core.util.util.Util.updateDBAccountWithdraw: %s" % UtilException(
                err)
            raise UtilException(err)

    # Market Depth 事件
    def threadSendListenMarketDepthEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketDepthEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
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
                    "src.core.util.util.Util.threadSendListenMarketDepthEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, err=Timeout Error, waiting for event handler result timeout."
                    % (current_thread().name, res, epoch, async, timeout))

    def updateDBMarketDepth(self, async=True, timeout=30):
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
            errStr = "src.core.util.util.Util.updateDBMarketDepth: %s" % UtilException(
                err)
            raise UtilException(err)

    # Market Kline 事件
    def threadSendListenMarketKlineEvent(self, res, start, end, interval,
                                         epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, res: %s, start: %s, interval: %s, end: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, res, start, end, interval, epoch, async,
               timeout))
        ids = []
        for r in res:
            time.sleep(epoch)
            id = self._sender.sendListenMarketKlineEvent(
                r["server"], r["fSymbol"], r["tSymbol"], interval, start, end)
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
                    "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, res: %s, start: %s, end: %s, interval: %s, epoch: %s, async: %s, timeout: %s}, err=Timeout Error, waiting for event handler result timeout."
                    % (current_thread().name, res, start, end, interval, epoch,
                       async, timeout))

    def updateDBMarketKline(self, async=True, timeout=30):
        self._logger.debug("src.core.util.util.Util.updateDBMarketKline")
        try:
            db = DB()
            db.delMarketKline()
            db.delSignalTickerDis()
            db.delSignalTickerTra()
            db.delSignalTickerPair()
            interval = '1h'
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
                          timestamp_to_isoformat(end), interval, epoch, async,
                          timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketKline: %s" % UtilException(
                err)
            raise UtilException(err)

    # Market ticker 事件
    def threadSendListenMarketTickerEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketTickerEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, res, epoch, async, timeout))
        ids = []
        for r in res:
            db = DB()
            aggDepth = db.getViewMarketSymbolPairsAggDepth(
                self._exchanges, r["fSymbol"],
                r["tSymbol"])[0]["aggDepth"] * self._marketTickerAggStep
            aggDepth = 1.0 if aggDepth > 1 else aggDepth  # make sure < 1.0
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
                    "src.core.util.util.Util.threadSendListenMarketTickerEvent: err=Timeout Error, waiting for event handler result timeout."
                )

    def updateDBMarketTicker(self, async=True, timeout=30):
        self._logger.debug("src.core.util.util.Util.updateDBMarketTicker")
        try:
            db = DB()
            db.delMarketTicker()
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
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketTicker: %s" % UtilException(
                err)
            raise UtilException(err)

    # Judge 事件
    def updateDBJudgeMarketKline(self):
        pass

    def updateDBJudgeMarketTicker(self, async=True, timeout=30):
        self._logger.debug("src.core.util.util.Util.updateDBJudgeMarketTicker")
        try:
            id = self._sender.sendJudgeMarketTickerEvent(
                self._types, self._exchanges)
            if not async:
                st = self._engine.getEventStatus(id)
                startTime = time.time()
                while st != DONE_STATUS_EVENT and time.time(
                ) - startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.warn(
                        "src.core.util.util.Util.updateDBJudgeMarketTicker: err=Timeout Error, waiting for event handler result timeout."
                    )
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBJudgeMarketTicker: %s" % UtilException(
                err)
            raise UtilException(err)

    # Backtest 事件
    def updateDBBacktest(self, async=True, timeout=30):
        self._logger.debug("src.core.util.util.Util.updateDBBacktest")
        try:
            pass
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBBacktest: %s" % UtilException(
                err)
            raise UtilException(err)

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
