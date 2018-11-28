# -*- coding: utf-8 -*-

import json

from src.core.db.db import DB
from src.core.engine.engine import Event
from src.core.engine.enums import *
from src.core.util.exceptions import DBException, EngineException
from src.core.util.helper import utcnow_timestamp
from src.core.util.log import Logger


class Sender(object):
    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._logger = Logger()

    def sendListenAccountBalanceEvent(self, exchange):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_ACCOUNT_BALANCE_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                server=exchange))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendListenAccountBalanceEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenAccountWithdrawEvent(self, exchange, asset):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                server=exchange,
                asset=asset))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendListenAccountWithdrawEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenMarketDepthEvent(self, exchange, fSymbol, tSymbol,
                                   limit=100):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_MARKET_DEPTH_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                server=exchange,
                fSymbol=fSymbol,
                tSymbol=tSymbol,
                limit=limit))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendListenMarketDepthEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenMarketKlineEvent(self, exchange, fSymbol, tSymbol, interval,
                                   start, end):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_MARKET_KLINE_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                server=exchange,
                fSymbol=fSymbol,
                tSymbol=tSymbol,
                interval=interval,
                start=start,
                end=end))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendListenMarketKlineEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendListenMarketTickerEvent(self, exchange, fSymbol, tSymbol):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            LISTEN_MARKET_TICKER_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                server=exchange,
                fSymbol=fSymbol,
                tSymbol=tSymbol))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendListenMarketTickerEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendJudgeMarketKlineEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            JUDGE_MARKET_KLINE_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendJudgeMarketKlineEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        pass

    def sendJudgeMarketTickerEvent(self, excludeCoins, baseCoin,
                                   symbolStartBaseCoin, symbolEndBaseCoin,
                                   symbolEndTimeout):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            JUDGE_MARKET_TICKER_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                excludeCoins=excludeCoins,
                baseCoin=baseCoin,
                symbolStartBaseCoin=symbolStartBaseCoin,
                symbolEndBaseCoin=symbolEndBaseCoin,
                symbolEndTimeout=symbolEndTimeout))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendJudgeMarketTickerEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendBacktestMarketKlineEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            BACKTEST_MARKET_KLINE_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendBacktestMarketKlineEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        pass

    def sendBacktestMarketTickerEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            BACKTEST_MARKET_TICKER_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendBacktestMarketTickerEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendOrderMarketKlineEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            ORDER_MARKET_KLINE_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendOrderMarketKlineEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        pass

    def sendOrderMarketTickerEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            ORDER_MARKET_TICKER_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendOrderMarketTickerEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendOrderConfirmEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            ORDER_CONFIRM_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendOrderConfirmEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendOrderCancleEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            ORDER_CANCEL_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendOrderCancleEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendStatiscBacktestEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            STATISTIC_BACKTEST_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendStatiscBacktestEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)

    def sendStatiscOrderEvent(self, args):
        # 构造事件对象
        TEMP_EVENT = json.loads(
            STATISTIC_ORDER_EVENT.substitute(
                id=self._engine.getEventID(),
                timeStamp=utcnow_timestamp(),
                args=""))
        event = Event(TEMP_EVENT)
        self._logger.debug(
            "src.core.engine.sender.Sender.sendStatiscOrderEvent: " +
            json.dumps(TEMP_EVENT))
        # 发送事件
        self._engine.sendEvent(event)
