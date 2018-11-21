# -*- coding: utf-8 -*-

import os
import time
import pandas as pd
from src.core.db.db import DB
from src.core.config import Config
from src.core.util.log import Logger
from src.core.engine.listen import Listen
from src.core.util.exceptions import DBException, ApplicationException

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
            errStr = "src.core.util.util.Util.initDB: %s" % ApplicationException(err)
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
            errStr = "src.core.util.util.Util.initDBInfo: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # ServerLimit数据
    def initServerLimits(self):
        self._logger.debug("src.core.util.util.Util.getServerLimits")
        try:
            db = DB()
            res = db.getInfoServer()
            self._serverLimits = pd.DataFrame(res).set_index(["server"], inplace=False)
        except DBException as err:
            errStr = "src.core.util.util.Util.getServerLimits: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Balance 数据
    def updateDBAccountBalance(self, listen):
        self._logger.debug("src.core.util.util.Util.updateDBAccountBalance")
        try:
            for exchange in self._mainCof["exchanges"]:
                listen.sendListenAccountBalanceEvent(exchange)
        except DBException as err:
            errStr = "src.core.util.util.Util.updateDBAccountBalance: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account Withdraw 数据
    def updateDBAccountWithdraw(self, listen):
        self._logger.debug("src.core.util.util.Util.updateDBAccountWithdraw")
        try:
            db = DB()
            res = db.getInfoWithdraw()
            for r  in res:
                if r["can_deposite"] == "True" and r["can_withdraw"] == "True":
                    time.sleep(float(1.25/self._serverLimits["requests_second"].min()))
                    listen.sendListenAccountWithdrawEvent(r["server"], r["asset"])
        except DBException as err:
            errStr = "src.core.util.util.Util.updateDBAccountWithdraw: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market数据
    def updateDBMarket(self):
        self._logger.debug("src.core.util.util.Util.updateDBMarket")
        pass

    # Trade数据
    def updateDBTrade(self):
        pass
