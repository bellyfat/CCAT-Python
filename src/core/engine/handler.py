# -*- coding: utf-8 -*-

import json

from src.core.db.db import DB
from src.core.engine.enums import *
from src.core.util.exceptions import DBException, EngineException
from src.core.util.log import Logger


class Handler(object):
    def __init__(self):
        self._logger = Logger()

    def handleListenAccountBalanceEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: "
            + event.type)
        [exchange] = event.args
        try:
            db = DB()
            db.insertAccountBalanceHistory(exchange)
        except DBException as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenAccountWithdrawEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: "
            + event.type)
        [exchange, asset] = event.args
        try:
            db = DB()
            db.insertAccountWithdrawHistory(exchange, asset)
        except DBException as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenMarketDepthEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketDepthEvent: " +
            event.type)
        [exchange, fSymbol, tSymbol, limit] = event.args
        try:
            db = DB()
            db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except DBException as err:
            errStr = "src.core.engine.handler.Handler.handleListenDepthEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenMarketKlineEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketKlineEvent: " +
            event.type)
        [exchange, fSymbol, tSymbol, interval, start, end] = event.args
        try:
            db = DB()
            db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                                 end)
        except DBException as err:
            errStr = "src.core.engine.handler.Handler.handleListenKlineEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenMarketTickerEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketTickerEvent: " +
            event.type)
        # 接收事件
        [exchange, fSymbol, tSymbol] = event.args
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol)
        except DBException as err:
            errStr = "src.core.engine.handler.Handler.handleListenTickerEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleJudgeMarketKlineEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: " +
            event.type)
        # 接收事件
        pass

    def handleJudgeMarketTickerEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: " +
            event.type)
        # 接收事件
        pass

    def handleBacktestMarketKlineEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestMarketKlineEvent: " +
            event.type)
        # 接收事件
        pass

    def handleBacktestMarketTickerEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestMarketTickerEvent: " +
            event.type)
        # 接收事件
        pass

    def handleOrderMarketKlineEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderMarketKlineEvent: " +
            event.type)
        # 接收事件
        pass

    def handleOrderMarketTickerEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderMarketTickerEvent: " +
            event.type)
        # 接收事件
        pass

    def handleOrderConfirmEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderConfirmEvent: " +
            event.type)
        # 接收事件
        pass

    def handleOrderCancelEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderCancelEvent: " +
            event.type)
        # 接收事件
        pass

    def handleStatisticBacktestEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticBacktestEvent: " +
            event.type)
        # 接收事件
        pass

    def handleStatisticOrderEvent(self, event):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticOrderEvent: " +
            event.type)
        # 接收事件
        pass
