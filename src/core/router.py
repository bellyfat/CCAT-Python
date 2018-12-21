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
        # config param
        self._epoch = Config()._Router_epoch
        self._timeout = Config()._Router_timeout
        self._marketKlineInterval = Config()._Main_marketKlineInterval
        self._marketTickerInterval = Config()._Main_marketTickerInterval
        self._statisticJudgeInterval = Config()._Main_statisticJudgeInterval
        self._asyncAccount = Config()._Main_asyncAccount
        self._syncAccountTimeout = Config()._Main_syncAccountTimeout
        self._asyncMarketKline = Config()._Main_asyncMarketKline
        self._syncMarketKlineTimeout = Config()._Main_syncMarketKlineTimeout
        self._asyncMarketDepth = Config()._Main_asyncMarketDepth
        self._syncMarketDepthTimeout = Config()._Main_syncMarketDepthTimeout
        self._asyncMarketTicker = Config()._Main_asyncMarketTicker
        self._syncMarketTickerTimeout = Config()._Main_syncMarketTickerTimeout
        self._asyncJudge = Config()._Main_asyncJudge
        self._syncJudgeTimeout = Config()._Main_syncJudgeTimeout
        self._asyncBacktest = Config()._Main_asyncBacktest
        self._syncBacktestTimeout = Config()._Main_syncBacktestTimeout
        self._asyncOrder = Config()._Main_asyncOrder
        self._syncOrderTimeout = Config()._Main_syncOrderTimeout
        self._asyncStatistic = Config()._Main_asyncStatistic
        self._syncStatisticTimeout = Config()._Main_syncStatisticTimeout
        # class instance
        self._eventEngine = EventEngine()
        self._sender = Sender(self._eventEngine)
        self._handler = Handler(self._eventEngine)
        self._register = Register(self._eventEngine, self._handler)
        self._util = Util(self._eventEngine, self._sender)
        # logger
        self._logger = Logger()
        # router param
        self._start = False
        self._startTime = time.time()
        self._marketKlineUpdateTime = time.time()
        # self._marketKlineUpdateTime = time.time() - self._marketKlineInterval
        self._marketTickerUpdateTime = time.time() - self._marketTickerInterval
        self._statisticJudgeUpdateTime = time.time(
        ) - self._statisticJudgeInterval

    def start(self):
        self._logger.info("src.core.router.Router.start")
        try:
            # register engine
            self._register.register()
            # start engine
            self._eventEngine.start()
            # set start param
            self._start = True
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.start: %s" % RouterException(err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def stop(self):
        self._logger.info("src.core.router.Router.stop")
        try:
            # stop engine
            self._eventEngine.stop()
            # unregister engine
            self._register.unregister()
            # set start param
            self._start = False
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.stop: %s" % RouterException(err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def initAPP(self):
        self._logger.info("src.core.router.Router.initAPP")
        try:
            self._util.initDB()
            self._util.initDBInfo()
            self._util.initServerLimits()
            self._util.updateDBAccountBalance(
                async=self._asyncAccount, timeout=self._syncAccountTimeout)
            # self._util.updateDBAccountWithdraw() # 暂时不考虑充提币 耗时约 1min
            # util.updateDBOrderHistoryInsert() # 暂时不同步历史交易 耗时约 2min
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.initAPP: %s" % RouterException(
                err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def updateAPP(self):
        self._logger.info("src.core.router.Router.updateAPP")
        try:
            # make sure engine start
            if not self._start:
                raise Exception(
                    'ENGINE STAUS ERROR, make sure engine is started.')
            # init first
            self._startTime = time.time()
            # run initServerLimits
            self._util.initServerLimits()
            # run monitor
            while time.time(
            ) - self._startTime < self._timeout or self._timeout == 0:
                self.runMonitor()
                self._logger.info(
                    "src.core.router.Router.updateAPP: sleep epoch for %ss" %
                    self._epoch)
                time.sleep(self._epoch)
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.updateAPP: %s" % RouterException(
                err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def runMonitor(self):
        self._logger.info("src.core.router.Router.runMonitor")
        try:
            # update market kline after interval
            if time.time(
            ) - self._marketKlineUpdateTime > self._marketKlineInterval:
                self._logger.info(
                    "src.core.router.Router.runMonitor: updateDBMarketKline")
                self._marketKlineUpdateTime = time.time()
                # update db market kline, async must be false
                self._util.updateDBMarketKline(
                    async=self._asyncMarketKline,
                    timeout=self._syncMarketKlineTimeout)
            # update market ticker after interval, update judge after ticker
            if time.time(
            ) - self._marketTickerUpdateTime > self._marketTickerInterval:
                self._logger.info(
                    "src.core.router.Router.runMonitor: updateDBMarketTicker")
                self._marketTickerUpdateTime = time.time()
                # update db market ticker, async must be false
                self._util.updateDBMarketTicker(
                    async=self._asyncMarketTicker,
                    timeout=self._syncMarketTickerTimeout)
                self._logger.info(
                    "src.core.router.Router.runMonitor: updateDBJudgeMarketTicker"
                )
                # update db judge market ticker, async false only on slow pc
                self._util.updateDBJudgeMarketTicker(
                    async=self._asyncJudge, timeout=self._syncJudgeTimeout)
            # update statistic after interval
            if time.time(
            ) - self._statisticJudgeUpdateTime > self._statisticJudgeInterval:
                self._logger.info(
                    "src.core.router.Router.runMonitor: updateDBStatisticJudge"
                )
                self._statisticJudgeUpdateTime = time.time()
                # update db statistic judge, async false only on slow pc
                self._util.updateDBStatisticJudge(
                    async=self._asyncStatistic,
                    timeout=self._syncStatisticTimeout)
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runMonitor: %s" % RouterException(
                err)
            raise RouterException(err)

    def runBacktest(self):
        self._logger.info("src.core.router.Router.runBacktest")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runBacktest: %s" % RouterException(
                err)
            self._logger.critical(errStr)
            raise RouterException(err)

    def runBacktestStatistic(self):
        self._logger.info("src.core.router.Router.runBacktestStatistic")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runBacktestStatistic: %s" % RouterException(
                err)
            raise RouterException(err)

    def runOrder(self):
        self._logger.info("src.core.router.Router.runOrder")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runOrder: %s" % RouterException(
                err)
            raise RouterException(err)

    def runOrderStatistic(self):
        self._logger.info("src.core.router.Router.runOrder")
        try:
            pass
        except (UtilException, Exception) as err:
            errStr = "src.core.router.Router.runOrder: %s" % RouterException(
                err)
            raise RouterException(err)
