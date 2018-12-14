# -*- coding: utf-8 -*-

import time

from src.core.config import Config
from src.core.db.db import DB
from src.core.engine.engine import EventEngine
from src.core.engine.handler import Handler
from src.core.engine.register import Register
from src.core.engine.sender import Sender
from src.core.util.exceptions import RouterException, UtilException
from src.core.util.log import Logger
from src.core.util.util import Util


class Router(object):
    def __init__(self):
        # config
        self._marketKlineCycle = Config()._Main_marketKlineCycle
        self._marketKlineUpdated = False
        self._marketKlineUpdateTime = time.time()
        # class instance
        self._eventEngine = EventEngine()
        self._sender = Sender(self._eventEngine)
        self._handler = Handler(self._eventEngine)
        self._register = Register(self._eventEngine, self._handler)
        self._util = Util(self._eventEngine, self._sender)
        # logger
        self._logger = Logger()
        # register engine
        self._register.register()
        # start engine
        self._eventEngine.start()

    def __del__(self):
        # stop engine
        self._eventEngine.stop()
        # unregister engine
        self._register.unregister()

    def initAPP(self):
        self._logger.debug("src.core.router.Router.initAPP")
        try:
            self._util.initDB()
            self._util.initDBInfo()
            self._util.initServerLimits()
            self._util.updateDBAccountBalance(async=False, timeout=10)
            self._util.updateDBAccountWithdraw()
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.initAPP: %s" % RouterException(err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def updateAPP(self):
        self._logger.debug("src.core.router.Router.updateAPP")
        try:
            # init server limit first
            self._util.initServerLimits()
            # run listen
            self.runListen()
            # run backtest
            self.runBacktest()
            # run again
            self.updateAPP()
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.updateAPP: %s" % RouterException(err)
            self._logger.critical(errStr)
            raise RouterException(err)



    def runListen(self):
        self._logger.debug("src.core.router.Router.runListen")
        try:
            if time.time() - self._marketKlineUpdateTime > self._marketKlineCycle or not self._marketKlineUpdated:
                self._marketKlineUpdated = True
                self._marketKlineUpdateTime = time.time()
                self._util.updateDBMarketKline(async=False, timeout=30)
            self._util.updateDBMarketTicker(async=False, timeout=30)
            self._util.updateDBJudgeMarketTicker(async=False, timeout=10)
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runListen: %s" % RouterException(err)
            raise RouterException(err)

    def runBacktest(self):
        self._logger.debug("src.core.router.Router.runBacktest")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runBacktest: %s" % RouterException(err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def runBacktestStatistic(self):
        self._logger.debug("src.core.router.Router.runBacktestStatistic")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runBacktestStatistic: %s" % RouterException(err)
            raise RouterException(err)

    def runOrder(self):
        self._logger.debug("src.core.router.Router.runOrder")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runOrder: %s" % RouterException(err)
            raise RouterException(err)

    def runOrderStatistic(self):
        self._logger.debug("src.core.router.Router.runOrder")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runOrder: %s" % RouterException(err)
            raise RouterException(err)
