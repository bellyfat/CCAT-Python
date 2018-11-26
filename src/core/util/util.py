# -*- coding: utf-8 -*-

import os
import time
from threading import Thread, current_thread

import pandas as pd

from src.core.config import Config
from src.core.db.db import DB
from src.core.util.exceptions import ApplicationException, DBException
from src.core.util.helper import timestamp_to_isoformat, utcnow_timestamp
from src.core.util.log import Logger


# util class
class Util(object):
    def __init__(self):
        self._logger = Logger()
        self._mainCof = Config()._main
        self._serverLimits = None

    # 初始化数据库
    def initDB(self):
        self._logger.debug("src.core.util.util.Util.initDB")
        try:
            db = DB()
            db.initDB()
            db.creatTables()
            db.creatViews()
        except DBException as err:
            errStr = "src.core.util.util.Util.initDB: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Info数据
    def initDBInfo(self):
        self._logger.debug("src.core.util.util.Util.initDBInfo")
        try:
            db = DB()
            db.insertInfoServer(self._mainCof["exchanges"])
            db.insertInfoSymbol(self._mainCof["exchanges"])
            db.insertInfoWithdraw(self._mainCof["exchanges"])
        except DBException as err:
            errStr = "src.core.util.util.Util.initDBInfo: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # ServerLimit数据
    def initServerLimits(self):
        self._logger.debug("src.core.util.util.Util.getServerLimits")
        try:
            db = DB()
            res = db.getInfoServer()
            self._serverLimits = pd.DataFrame(res).set_index(["server"],
                                                             inplace=False)
        except DBException as err:
            errStr = "src.core.util.util.Util.getServerLimits: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Balance 事件
    def updateDBAccountBalance(self, sender):
        self._logger.debug("src.core.util.util.Util.updateDBAccountBalance")
        try:
            sender.sendListenAccountBalanceEvent(self._mainCof["exchanges"])
        except DBException as err:
            errStr = "src.core.util.util.Util.updateDBAccountBalance: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Withdraw 事件
    def updateDBAccountWithdraw(self, sender):
        self._logger.debug("src.core.util.util.Util.updateDBAccountWithdraw")
        try:
            db = DB()
            ####################################################################
            # fully update
            ####################################################################
            # res = db.getInfoWithdraw()
            # for r in res:
            #     if r["can_deposite"] == "True" or r["can_withdraw"] == "True":
            #         time.sleep(float(self._mainCof["apiEpochSaveBound"]) / float(
            #             self._serverLimits.at[r["server"], "requests_second"]))
            #         sender.sendListenAccountWithdrawEvent(
            #             r["server"], r["asset"])
            ####################################################################
            # fast update
            res = db.getViewAccountBalanceCurrent(self._mainCof["exchanges"])
            for r in res:
                time.sleep(float(self._mainCof["apiEpochSaveBound"]) / float(
                    self._serverLimits.at[r["server"], "requests_second"]))
                sender.sendListenAccountWithdrawEvent(r["server"], r["asset"])

        except DBException as err:
            errStr = "src.core.util.util.Util.updateDBAccountWithdraw: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market Kline 事件
    def threadSendListenMarketKlineEvent(self, sender, res, start, end, epoch):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, sender: %s, res: %s, epoch: %s}"
            % (current_thread().name, sender, type(res), epoch))
        for r in res:
            time.sleep(epoch)
            sender.sendListenMarketKlineEvent(r["server"], r["fSymbol"],
                                              r["tSymbol"], "1h", start, end)

    def updateDBMarketKline(self, sender):
        self._logger.debug("src.core.util.util.Util.updateDBMarketKline")
        try:
            db = DB()
            db.delMarketKline()
            start = utcnow_timestamp() - 24 * 60 * 60 * 1000
            end = utcnow_timestamp()
            tds = []
            for server in self._mainCof["exchanges"]:
                epoch = float(self._mainCof["apiEpochSaveBound"]) / float(
                    self._serverLimits.at[server, "requests_second"])
                res = db.getViewInfoSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketKlineEvent,
                    name="%s-thread" % server,
                    args=(sender, res, timestamp_to_isoformat(start),
                          timestamp_to_isoformat(end), epoch))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except DBException as err:
            errStr = "src.core.util.util.Util.updateDBMarketKline: %s" % ApplicationException(
                err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market ticker 事件
    def threadSendListenMarketTickerEvent(self, sender, res, epoch):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketTickerEvent: {thread: %s, sender: %s, res: %s, epoch: %s}"
            % (current_thread().name, sender, type(res), epoch))
        for r in res:
            time.sleep(epoch)
            sender.sendListenMarketTickerEvent(r["server"], r["fSymbol"],
                                               r["tSymbol"])

    def updateDBMarketTicker(self, sender):
        self._logger.debug("src.core.util.util.Util.updateDBMarketTicker")
        try:
            db = DB()
            tds = []
            for server in self._mainCof["exchanges"]:
                epoch = float(self._mainCof["apiEpochSaveBound"]) / float(
                    self._serverLimits.at[server, "requests_second"])
                res = db.getViewMarketSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketTickerEvent,
                    name="%s-thread" % server,
                    args=(sender, res, epoch))
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

    # Trade 事件
    def updateDBTrade(self):
        pass
