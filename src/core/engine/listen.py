# -*- coding: utf-8 -*-

import json
from src.core.util.log import Logger
from src.core.engine.engine import Event
from src.core.engine.event import LISTEN_DEPTH_EVENT, LISTEN_KLINE_EVENT, LISTEN_TICKER_EVENT


class Listen(object):

    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._logger = Logger()

    def sendListenDepthEvent(self, *exchanges, fSymbol, tSymbol, limit=100):
        # 构造事件对象
        _EVETNT = LISTEN_DEPTH_EVENT.substitute(
            servers=exchanges,
            fSymbol=fSymbol,
            tSymbol=tSymbol,
            limit=limit
        )
        self._logger.debug(_EVETNT)
        event = Event(_EVENT)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenKlineEvent(self, *exchanges, fSymbol, tSymbol, interval, start, end):
        # 构造事件对象
        _EVENT = LISTEN_KLINE_EVENT.substitute(
            servers=exchanges,
            fSymbol=fSymbol,
            tSymbol=tSymbol,
            interval=interval,
            start=start,
            end=end
        )
        event = Event(_EVENT)
        # 发送事件
        self._logger.debug(event)
        self._engine.sendEvent(event)

    def sendListenTickerEvent(self, *exchanges, fSymbol, tSymbol):
        # 构造事件对象
        _EVENT = LISTEN_TICKER_EVENT.substitute(
            servers=exchanges,
            fSymbol=fSymbol,
            tSymbol=tSymbol
        )
        event = Event(_EVENT)
        # 发送事件
        self._logger.debug(event)
        self._engine.sendEvent(event)

    def handleListenDepthEvent(self, event):
        # 接收事件
        self._logger.debug(event)
        exchanges = event["dict"]["servers"]
        [fSymbol, tSymbol, limit] = event["dict"]["args"]
        try:
            insertMarketDepth(exchanges, fSymbol, tSymbol, limit)
        except DBException as err:
            errStr = "%s/n, Engine Listen Error. Can Not handle listen depth event." % err
            self._logger.error(errStr)

    def handleListenKlineEvent(self, event):
        # 接收事件
        self._logger.debug(event)
        exchanges = event["dict"]["servers"]
        [fSymbol, tSymbol, interval, start, end] = event["dict"]["args"]
        try:
            insertMarketKline(exchanges, fSymbol, tSymbol, interval, start, end)
        except DBException as err:
            errStr = "%s/n, Engine Listen Error. Can Not handle listen kline event." % err
            self._logger.error(errStr)

    def handleListenTickerEvent(self, event):
        # 接收事件
        self._logger.debug(event)
        exchanges = event["dict"]["servers"]
        [fSymbol, tSymbol] = event["dict"]["args"]
        try:
            insertMarketTicker(exchanges, fSymbol, tSymbol)
        except DBException as err:
            errStr = "%s/n, Engine Listen Error. Can Not handle listen ticker event." % err
            self._logger.error(errStr)

    def registerListenEvent(self):
        # 构造事件
        DEPETH_EVETNT = json.loads(LISTEN_DEPTH_EVENT.substitute(
            servers="",
            fSymbol="",
            tSymbol="",
            limit=""
        ))
        KLINE_EVENT = json.loads(LISTEN_KLINE_EVENT.substitute(
            servers="",
            fSymbol="",
            tSymbol="",
            interval="",
            start="",
            end=""
        ))
        TICKER_EVENT = json.loads(LISTEN_TICKER_EVENT.substitute(
            servers="",
            fSymbol="",
            tSymbol=""
        ))
        # 构造 handler
        DEPETH_EVETNT_HANDLER = self.handleListenDepthEvent
        KLINE_EVETNT_HANDLER = self.handleListenKlineEvent
        TICKER_EVETNT_HANDLER = self.handleListenTickerEvent
        # 注册事件
        self._engine.register(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.register(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.register(TICKER_EVENT, TICKER_EVETNT_HANDLER)

    def unregisterListenEvent(self):
        # 构造事件
        DEPETH_EVETNT = LISTEN_DEPTH_EVENT.substitute(
            servers="",
            fSymbol="",
            tSymbol="",
            limit=""
        )
        KLINE_EVENT = LISTEN_KLINE_EVENT.substitute(
            servers="",
            fSymbol="",
            tSymbol="",
            interval="",
            start="",
            end=""
        )
        TICKER_EVENT = LISTEN_TICKER_EVENT.substitute(
            servers="",
            fSymbol="",
            tSymbol=""
        )
        # 构造 handler
        DEPETH_EVETNT_HANDLER = self.handleListenDepthEvent
        KLINE_EVETNT_HANDLER = self.handleListenKlineEvent
        TICKER_EVETNT_HANDLER = self.handleListenTickerEvent
        # 注销事件
        self._engine.unregister(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.unregister(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.unregister(TICKER_EVENT, TICKER_EVETNT_HANDLER)
