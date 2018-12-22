# -*- coding: utf-8 -*-

import json

from src.core.db.db import DB
from src.core.engine.engine import Event
from src.core.engine.enums import *
from src.core.util.exceptions import EngineException
from src.core.util.helper import utcnow_timestamp
from src.core.util.log import Logger


class Sender(object):
    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._logger = Logger()

    # Account Balance 事件
    def sendListenAccountBalanceEvent(self, exchange):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                LISTEN_ACCOUNT_BALANCE_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendListenAccountBalanceEvent: "
                + json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenAccountBalanceEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Account Withdraw 事件
    def sendListenAccountWithdrawEvent(self, exchange, asset):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange,
                    asset=asset))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendListenAccountWithdrawEvent: "
                + json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenAccountWithdrawEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Market Depth 事件
    def sendListenMarketDepthEvent(self, exchange, fSymbol, tSymbol,
                                   limit=100):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                LISTEN_MARKET_DEPTH_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange,
                    fSymbol=fSymbol,
                    tSymbol=tSymbol,
                    limit=limit))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendListenMarketDepthEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenMarketDepthEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Market Kline 事件
    def sendListenMarketKlineEvent(self, exchange, fSymbol, tSymbol, interval,
                                   start, end):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                LISTEN_MARKET_KLINE_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange,
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
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenMarketKlineEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Market ticker 事件
    def sendListenMarketTickerEvent(self, exchange, fSymbol, tSymbol,
                                    aggDepth):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                LISTEN_MARKET_TICKER_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange,
                    fSymbol=fSymbol,
                    tSymbol=tSymbol,
                    aggDepth=aggDepth))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendListenMarketTickerEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenMarketTickerEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Judge 事件
    def sendJudgeMarketDepthEvent(self, args):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                JUDGE_MARKET_DEPTH_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    args=""))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendJudgeMarketDepthEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            pass
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendJudgeMarketDepthEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    def sendJudgeMarketKlineEvent(self, args):
        try:
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
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendJudgeMarketKlineEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    def sendJudgeMarketTickerEvent(self, exchange, types):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                JUDGE_MARKET_TICKER_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange,
                    types=types))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendJudgeMarketTickerEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendJudgeMarketTickerEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Backtest 事件
    def sendBacktestHistoryCreatEvent(self, signals, timeout):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                BACKTEST_HISTORY_CREAT_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    signals=signals,
                    timeout=timeout))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendBacktestHistoryCreatEvent: "
                + json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendBacktestHistoryCreatEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Order 事件
    def sendOrderHistoryInsertEvent(self, exchange, fSymbol, tSymbol, limit,
                                    ratio):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                ORDER_HISTORY_INSERT_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange=exchange,
                    fSymbol=fSymbol,
                    tSymbol=tSymbol,
                    limit=limit,
                    ratio=ratio))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendOrderHistoryInsertEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendOrderHistoryInsertEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    def sendOrderHistoryCreatEvent(self, signals):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                ORDER_HISTORY_CREAT_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    signals=signals))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendOrderHistoryCreatEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendOrderHistoryCreatEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    # Statistic 事件
    def sendStatiscJudgeEvent(self, exchange, types):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                STATISTIC_JUDGE_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    exchange = exchange,
                    types = types))
            event = Event(TEMP_EVENT)
            self._logger.debug(
                "src.core.engine.sender.Sender.sendStatiscJudgeEvent: " +
                json.dumps(TEMP_EVENT))
            # 发送事件
            self._engine.sendEvent(event)
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendStatiscJudgeEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    def sendStatiscBacktestEvent(self, args):
        try:
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
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendStatiscBacktestEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)

    def sendStatiscOrderEvent(self, args):
        try:
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
            # 返回参数
            return event
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendStatiscOrderEvent: %s" % EngineException(
                err)
            raise EngineException(errStr)
