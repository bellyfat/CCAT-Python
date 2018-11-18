# -*- coding: utf-8 -*-

from src.core.config import Config
from src.core.util.log import Logger
from src.core.engine.engine import Event, EventEngine
from src.core.engine.event import LISTEN_DEPTH_EVENT, LISTEN_KLINE_EVENT, LISTEN_TICKER_EVENT


class Listen(Engine):

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
        if not event["type"] == LISTEN_DEPTH_EVENT["type"]:
            return
        exchanges = event["dict"]["servers"]
        [fSymbol, tSymbol, limit] = event["dict"]["args"]
        try:
            # OKEX
            if exchange == "all" or self.okexConf["exchange"] in exchange:
