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

    def sendListenAccountBalanceEvent(self, exchange):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenAccountBalanceEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)


    def sendListenAccountWithdrawEvent(self, exchange, asset):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenAccountWithdrawEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendListenMarketDepthEvent(self, exchange, fSymbol, tSymbol,
                                   limit=100):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenMarketDepthEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendListenMarketKlineEvent(self, exchange, fSymbol, tSymbol, interval,
                                   start, end):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenMarketKlineEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendListenMarketTickerEvent(self, exchange, fSymbol, tSymbol, aggDepth):
        try:
            # 构造事件对象
            TEMP_EVENT = json.loads(
                LISTEN_MARKET_TICKER_EVENT.substitute(
                    id=self._engine.getEventID(),
                    timeStamp=utcnow_timestamp(),
                    server=exchange,
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
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendListenMarketTickerEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

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
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendJudgeMarketTickerEvent(self, excludeCoins, baseCoin,
                                   symbolStartBaseCoin, symbolEndBaseCoin,
                                   symbolEndTimeout):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendJudgeMarketTickerEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendBacktestMarketKlineEvent(self, args):
        try:
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
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendBacktestMarketKlineEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendBacktestMarketTickerEvent(self, args):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendBacktestMarketTickerEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendOrderMarketKlineEvent(self, args):
        try:
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
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendOrderMarketKlineEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendOrderMarketTickerEvent(self, args):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendOrderMarketTickerEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendOrderConfirmEvent(self, args):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendOrderConfirmEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendOrderCancleEvent(self, args):
        try:
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
            # 返回参数
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendOrderCancleEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

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
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendStatiscBacktestEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

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
            return event.id
        except Exception as err:
            errStr = "src.core.engine.sender.Sender.sendStatiscOrderEvent: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)
