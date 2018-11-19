# -*- coding: utf-8 -*-

import os
import json
from src.core.db.db import DB
from src.core.config import Config
from src.core.util.log import Logger
from src.core.engine.engine import Event
from src.core.util.exceptions import DBException
from src.core.engine.event import LISTEN_DEPTH_EVENT, LISTEN_KLINE_EVENT, LISTEN_TICKER_EVENT


class Listen(object):
    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._db = DB()
        self._logger = Logger()

    def sendListenDepthEvent(self, exchange, fSymbol, tSymbol, limit=100):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_DEPTH_EVENT.substitute(
                server=exchange,
                fSymbol=fSymbol,
                tSymbol=tSymbol,
                limit=limit))
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenDepthEvent: "+event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenKlineEvent(self, exchange, fSymbol, tSymbol, interval,
                             start, end):
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
        self._logger.debug("src.core.engine.listen.sendListenKlineEvent: "+event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenTickerEvent(self, exchange, fSymbol, tSymbol):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_TICKER_EVENT.substitute(
                server=exchange, fSymbol=fSymbol, tSymbol=tSymbol))
        event = Event(TEMP_EVENT)
        self._logger.debug("src.core.engine.listen.sendListenTickerEvent: "+event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def handleListenDepthEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenDepthEvent")
        exchange = event.dict["server"]
        [fSymbol, tSymbol, limit] = event.dict["args"]
        try:
            self._db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenDepthEvent Error: %s" % err
            self._logger.error(errStr)

    def handleListenKlineEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenKlineEvent")
        exchange = event.dict["server"]
        [fSymbol, tSymbol, interval, start, end] = event.dict["args"]
        try:
            self._db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                              end)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenKlineEvent Error: %s" % err
            self._logger.error(errStr)

    def handleListenTickerEvent(self, event):
        # 接收事件
        self._logger.debug("src.core.engine.listen.handleListenTickerEvent")
        exchange = event.dict["server"]
        [fSymbol, tSymbol] = event.dict["args"]
        try:
            self._db.insertMarketTicker(exchange, fSymbol, tSymbol)
        except DBException as err:
            errStr = "src.core.engine.listen.handleListenTickerEvent Error: %s" % err
            self._logger.error(errStr)

    def registerListenEvent(self):
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
        self._logger.debug(DEPETH_EVETNT)
        self._logger.debug(DEPETH_EVETNT_HANDLER)
        self._engine.register(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.register(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.register(TICKER_EVENT, TICKER_EVETNT_HANDLER)

    def unregisterListenEvent(self):
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
        self._logger.debug(DEPETH_EVETNT)
        self._logger.debug(DEPETH_EVETNT_HANDLER)
        self._engine.unregister(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.unregister(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.unregister(TICKER_EVENT, TICKER_EVETNT_HANDLER)
