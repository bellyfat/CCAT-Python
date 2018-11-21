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
            "src.core.engine.listen.ListenHandler.handleListenAccountBalanceEvent: "
            + event.type)
        [exchange] = event.dict["args"]
        try:
            db = DB()
            db.insertAccountBalanceHistory(exchange)
        except DBException as err:
            errStr = "src.core.engine.listen.ListenHandler.handleListenAccountBalanceEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenAccountWithdrawEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.listen.ListenHandler.handleListenAccountWithdrawEvent: "
            + event.type)
        [exchange, asset] = event.dict["args"]
        try:
            db = DB()
            db.insertAccountWithdrawHistory(exchange, asset)
        except DBException as err:
            errStr = "src.core.engine.listen.ListenHandler.handleListenAccountWithdrawEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenDepthEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.listen.ListenHandler.handleListenDepthEvent: " +
            event.type)
        [exchange, fSymbol, tSymbol, limit] = event.dict["args"]
        try:
            db = DB()
            db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except DBException as err:
            errStr = "src.core.engine.listen.ListenHandler.handleListenDepthEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenKlineEvent(self, event):
        # 接收事件
        self._logger.debug(
            "src.core.engine.listen.ListenHandler.handleListenKlineEvent: " +
            event.type)
        [exchange, fSymbol, tSymbol, interval, start, end] = event.dict["args"]
        try:
            db = DB()
            db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                                 end)
        except DBException as err:
            errStr = "src.core.engine.listen.ListenHandler.handleListenKlineEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)

    def handleListenTickerEvent(self, event):
        self._logger.debug(
            "src.core.engine.listen.ListenHandler.handleListenTickerEvent: " +
            event.type)
        # 接收事件
        [exchange, fSymbol, tSymbol] = event.dict["args"]
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol)
        except DBException as err:
            errStr = "src.core.engine.listen.ListenHandler.handleListenTickerEvent: %s" % EngineException(
                err)
            self._logger.error(errStr)
