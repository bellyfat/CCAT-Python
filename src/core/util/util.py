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
        # self._basePriceVolume = Config()._Main_basePriceVolume
        # self._basePriceTimeout = Config()._Main_basePriceTimeout
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
        except (DBException, EngineException) as err:
            errStr = "src.core.util.util.Util.initDB: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Info数据
    def initDBInfo(self):
        self._logger.debug("src.core.util.util.Util.initDBInfo")
        try:
            db = DB()
            db.insertInfoServer(self._exchanges)
            db.insertInfoSymbol(self._exchanges)
            db.insertInfoWithdraw(self._exchanges)
        except (DBException, EngineException) as err:
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
        except (DBException, EngineException) as err:
            errStr = "src.core.util.util.Util.initServerLimits: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Balance 事件
    def updateDBAccountBalance(self, async=True, timeout=30):
        self._logger.debug("src.core.util.util.Util.updateDBAccountBalance")
        try:
            id = self._sender.sendListenAccountBalanceEvent(self._exchanges)
            if not async:
                st = self._engine.getEventStatus(id)
                startTime = time.time()
                while st != DONE_STATUS_EVENT and time.time()-startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.warn(
                        "src.core.util.util.Util.updateDBAccountBalance: Timeout Error, waiting for event handler result timeout."
                    )
        except (DBException, EngineException) as err:
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
                while st != DONE_STATUS_EVENT  and time.time()-startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: Timeout Error, waiting for event handler result timeout."
                )

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
                    name="%s-thread" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException) as err:
            errStr = "src.core.util.util.Util.updateDBAccountWithdraw: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market Kline 事件
    def threadSendListenMarketKlineEvent(self, res, start, end, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketKlineEvent: {\nthread: %s, \nres: \n%s, \nepoch: %s, \nasync: %s, \ntimeout: %s}"
            % (current_thread().name, res, epoch, async, timeout))
        ids=[]
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
                while st != DONE_STATUS_EVENT  and time.time()-startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenMarketKlineEvent: Timeout Error, waiting for event handler result timeout."
                )

    def updateDBMarketKline(self, async=True, timeout=30):
        self._logger.debug("src.core.util.util.Util.updateDBMarketKline")
        try:
            db = DB()
            db.delMarketKline()
            start = utcnow_timestamp() - 24 * 60 * 60 * 1000
            end = utcnow_timestamp()
            tds = []
            for server in self._exchanges:
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewInfoSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketKlineEvent,
                    name="%s-thread" % server,
                    args=(res, timestamp_to_isoformat(start),
                          timestamp_to_isoformat(end), epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException) as err:
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
            time.sleep(epoch)
            self._sender.sendListenMarketTickerEvent(r["server"], r["fSymbol"],
                                                     r["tSymbol"])
            ids.append(id)
        if not async:
            st = QUEUE_STATUS_EVENT
            startTime = time.time()
            for id in ids:
                st = self._engine.getEventStatus(id)
                while st != DONE_STATUS_EVENT  and time.time()-startTime < timeout:
                    st = self._engine.getEventStatus(id)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.warn(
                    "src.core.util.util.Util.threadSendListenMarketTickerEvent: Timeout Error, waiting for event handler result timeout."
                )

    def updateDBMarketTicker(self, async=True, timeout=30):
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
                    name="%s-thread" % server,
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

    # Judge ticker 事件
    def updateDBJudgeMarketTicker(self):
        self._logger.debug("src.core.util.util.Util.updateDBJudgeMarketTicker")
        try:
            self._sender.sendJudgeMarketTickerEvent(
                self._excludeCoins, self._baseCoin, self._symbolStartBaseCoin,
                self._symbolEndBaseCoin, self._symbolEndTimeout)
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
