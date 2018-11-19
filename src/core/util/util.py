# -*- coding: utf-8 -*-

import os
from src.core.db.db import DB
from src.core.config import Config
from src.core.util.log import Logger
from src.core.util.exceptions import DBException, ApplicationException

# util class
class Util(object):

    def __init__(self):
        self._logger = Logger()

    def initAPP(self):
        self._logger.debug("src.core.util.util.initAPP")
        # 初始化数据库
        self.initDB()
        # 插入静态Info数据

        pass

    def initDB(self):
        self._logger.debug("src.core.util.util.initDB")
        try:
            db = DB()
            db.initDB()
            db.creatTables()
            db.creatViews()
        except DBException as err:
            errStr = "src.core.util.util.init: Critical. ApplicationException: Can Not Init DB File. %s" % err
            self._logger.critical(errStr)
            raise ApplicationException(errStr)

    def updateDBInfo(self):
        self._logger.debug("src.core.util.util.initDBInfo")
        try:
            db = DB()
            # Info数据
            db.insertServerInfo()
            db.insertSymbolInfo()
            db.insertWithdrawInfo()
        except DBException as err:
            errStr = "src.core.util.util.init: Critical. ApplicationException: Can Not Init DB File. %s" % err
            self._logger.critical(errStr)
            raise ApplicationException(errStr)

    def updateDBAccount(self):
        # History数据
        db.insertAccountBalanceHistory()
        db.insertAccountWithdrawHistory("xxx")
