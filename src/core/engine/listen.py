# -*- coding: utf-8 -*-

import json

from src.core.db.db import DB
from src.core.engine.engine import Event
from src.core.engine.event import (LISTEN_DEPTH_EVENT, LISTEN_KLINE_EVENT,
                                   LISTEN_TICKER_EVENT)
from src.core.util.exceptions import DBException, EngineException
from src.core.util.log import Logger


class Listen(object):
    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._logger = Logger()

    def sendListenAccountBalanceEvent(self, exchange):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_ACCOUNT_BALANCE_EVENT.substitute(
                server=exchange)
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenAccountBalanceEvent: " +
                           event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenAccountWithdrawEvent(self, exchange):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute(
                server=exchange, asset=asset)
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenAccountWithdrawEvent: " +
                           event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenDepthEvent(self, exchange, fSymbol, tSymbol, limit=100):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_DEPTH_EVENT.substitute(
                server=exchange, fSymbol=fSymbol, tSymbol=tSymbol,
                limit=limit))
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenDepthEvent: " +
                           event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenKlineEvent(self, exchange, fSymbol, tSymbol, interval, start,
                             end):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_KLINE_EVENT.substitute(
                server=exchange,
                fSymbol=fSymbol,
                tSymbol=tSymbol,
                interval=interval,
                start=start,
                end=end))
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenKlineEvent: " +
                           event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenTickerEvent(self, exchange, fSymbol, tSymbol):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_TICKER_EVENT.substitute(
                server=exchange, fSymbol=fSymbol, tSymbol=tSymbol))
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenTickerEvent: " +
                           event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def handleListenAccountBalanceEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenAccountBalanceEvent")
        [exchange] = event.dict["args"]
        try:
            db = DB()
            db.insertAccountBalanceHistory(exchange)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenAccountBalanceEvent: %s" % EngineException(err)
            self._logger.error(errStr)

    def handleListenAccountWithdrawEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenAccountWithdrawEvent")
        [exchange, asset] = event.dict["args"]
        try:
            db = DB()
            db.insertAccountWithdrawHistory(exchange, asset)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenAccountWithdrawEvent: %s" % EngineException(err)
            self._logger.error(errStr)


    def handleListenDepthEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenDepthEvent")
        [exchange, fSymbol, tSymbol, limit] = event.dict["args"]
        try:
            db = DB()
            db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenDepthEvent: %s" % EngineException(err)
            self._logger.error(errStr)

    def handleListenKlineEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenKlineEvent")
        [exchange, fSymbol, tSymbol, interval, start, end] = event.dict["args"]
        try:
            db = DB()
            db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                                 end)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenKlineEvent: %s" % EngineException(err)
            self._logger.error(errStr)

    def handleListenTickerEvent(self, event):
        self._logger.debug("src.core.engine.listen.handleListenTickerEvent: " +
                           event.type)
        # 接收事件
        [exchange, fSymbol, tSymbol] = event.dict["args"]
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenTickerEvent: %s" % EngineException(err)
            self._logger.error(errStr)

    def registerListenEvent(self):
        self._logger.debug("src.core.engine.listen.registerListenEvent")
        # 构造事件
        DEPETH_EVETNT = Event(
            json.loads(
                LISTEN_DEPTH_EVENT.substitute(
                    server="", fSymbol="", tSymbol="", limit="")))
        KLINE_EVENT = Event(
            json.loads(
                LISTEN_KLINE_EVENT.substitute(
                    server="",
                    fSymbol="",
                    tSymbol="",
                    interval="",
                    start="",
                    end="")))
        TICKER_EVENT = Event(
            json.loads(
                LISTEN_TICKER_EVENT.substitute(
                    server="", fSymbol="", tSymbol="")))
        # 构造 handler
        DEPETH_EVETNT_HANDLER = self.handleListenDepthEvent
        KLINE_EVETNT_HANDLER = self.handleListenKlineEvent
        TICKER_EVETNT_HANDLER = self.handleListenTickerEvent
        # 注册事件
        self._engine.register(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.register(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.register(TICKER_EVENT, TICKER_EVETNT_HANDLER)

    def unregisterListenEvent(self):
        self._logger.debug("src.core.engine.listen.unregisterListenEvent")
        # 构造事件
        DEPETH_EVETNT = Event(
            json.loads(
                LISTEN_DEPTH_EVENT.substitute(
                    server="", fSymbol="", tSymbol="", limit="")))
        KLINE_EVENT = Event(
            json.loads(
                LISTEN_KLINE_EVENT.substitute(
                    server="",
                    fSymbol="",
                    tSymbol="",
                    interval="",
                    start="",
                    end="")))
        TICKER_EVENT = Event(
            json.loads(
                LISTEN_TICKER_EVENT.substitute(
                    server="", fSymbol="", tSymbol="")))
        # 构造 handler
        DEPETH_EVETNT_HANDLER = self.handleListenDepthEvent
        KLINE_EVETNT_HANDLER = self.handleListenKlineEvent
        TICKER_EVETNT_HANDLER = self.handleListenTickerEvent
        # 注销事件
        self._engine.unregister(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.unregister(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.unregister(TICKER_EVENT, TICKER_EVETNT_HANDLER)
