# -*- coding: utf-8 -*-

import json
from src.core.db.db import DB
from src.core.engine.engine import Event
from src.core.engine.enums import *
from src.core.util.exceptions import DBException, EngineException
from src.core.util.log import Logger
from src.core.util.helper import utcnow_timestamp


class Sender(object):
    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._logger = Logger()

    def sendListenAccountBalanceEvent(self, exchange):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_ACCOUNT_BALANCE_EVENT.substitute(
                timeStamp=utcnow_timestamp(), server=exchange))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.listen.Listen.sendListenAccountBalanceEvent: " +
            event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenAccountWithdrawEvent(self, exchange, asset):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute(
                server=exchange, asset=asset))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.listen.Listen.sendListenAccountWithdrawEvent: " +
            event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenDepthEvent(self, exchange, fSymbol, tSymbol, limit=100):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_MARKET_DEPTH_EVENT.substitute(
                server=exchange, fSymbol=fSymbol, tSymbol=tSymbol,
                limit=limit))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.listen.Listen.sendListenDepthEvent: " +
            event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenKlineEvent(self, exchange, fSymbol, tSymbol, interval, start,
                             end):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_MARKET_KLINE_EVENT.substitute(
                server=exchange,
                fSymbol=fSymbol,
                tSymbol=tSymbol,
                interval=interval,
                start=start,
                end=end))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.listen.Listen.sendListenKlineEvent: " +
            event.type)
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenTickerEvent(self, exchange, fSymbol, tSymbol):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_MARKET_TICKER_EVENT.substitute(
                server=exchange, fSymbol=fSymbol, tSymbol=tSymbol))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.listen.Listen.sendListenTickerEvent: " +
            event.type)
        # 发送事件
        self._engine.sendEvent(event)
