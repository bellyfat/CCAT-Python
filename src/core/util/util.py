# -*- coding: utf-8 -*-

import os
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

    def initAPP(self):
        self._logger.debug("src.core.util.util.initAPP")
        try:
            self.initDB()
            self.initDBInfo()
        except ApplicationException as err:
            errStr = "src.core.util.util.initAPP: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # 初始化数据库
    def initDB(self):
        self._logger.debug("src.core.util.util.initDB")
        try:
            db = DB()
            db.initDB()
            db.creatTables()
            db.creatViews()
        except DBException as err:
            errStr = "src.core.util.util.initDB: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Info数据
    def initDBInfo(self):
        self._logger.debug("src.core.util.util.initDBInfo")
        try:
            db = DB()
            db.insertInfoServer(self._mainCof["exchanges"])
            db.insertInfoSymbol(self._mainCof["exchanges"])
            db.insertInfoWithdraw(self._mainCof["exchanges"])
        except DBException as err:
            errStr = "src.core.util.util.initDBInfo: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Account数据
    def updateDBAccount(self, listen):
        self._logger.debug("src.core.util.util.updateDBAccount")
        try:
            for exchange in self._mainCof["exchanges"]:
                listen.sendListenAccountBalanceEvent(exchange)
            db = DB()
            res = db.getInfoWithdraw()
            for r in res:
                if r["can_deposite"] == "True" and r["can_withdraw"] == "True":
                    listen.sendListenAccountWithdrawEvent(r["server"], r["asset"])
        except DBException as err:
            errStr = "src.core.util.util.updateDBAccount: %s" % ApplicationException(err)
            self._logger.critical(errStr)
            raise ApplicationException(err)

    # Market数据
    def updateDBMarket(self):
        pass

    # Trade数据
    def updateDBTrade(self):
        pass
