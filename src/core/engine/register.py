# -*- coding: utf-8 -*-

import json

from src.core.engine.enums import *
from src.core.util.exceptions import EngineException
from src.core.util.log import Logger


class Register(object):
    def __init__(self, eventEngine, handler):
        self._eventEngine = eventEngine
        self._handler = handler
        self._logger = Logger()
        # 事件
        # listen event
        self.LISTEN_ACCOUNT_BALANCE_EVENT_TYPE = json.loads(
            LISTEN_ACCOUNT_BALANCE_EVENT.substitute())["type"]
        self.LISTEN_ACCOUNT_WITHDRAW_EVENT_TYPE = json.loads(
            LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute())["type"]
        self.LISTEN_MARKET_KLINE_EVENT_TYPE = json.loads(
            LISTEN_MARKET_KLINE_EVENT.substitute())["type"]
        self.LISTEN_MARKET_TICKER_EVENT_TYPE = json.loads(
            LISTEN_MARKET_TICKER_EVENT.substitute())["type"]
        self.LISTEN_MARKET_DEPTH_EVENT_TYPE = json.loads(
            LISTEN_MARKET_DEPTH_EVENT.substitute())["type"]
        # judge event
        self.JUDGE_MARKET_KLINE_EVENT_TYPE = json.loads(
            JUDGE_MARKET_KLINE_EVENT.substitute())["type"]
        self.JUDGE_MARKET_TICKER_EVENT_TYPE = json.loads(
            JUDGE_MARKET_TICKER_EVENT.substitute())["type"]
        # backtest event
        self.BACKTEST_MARKET_KLINE_EVENT_TYPE = json.loads(
            BACKTEST_MARKET_KLINE_EVENT.substitute())["type"]
        self.BACKTEST_MARKET_TICKER_EVENT_TYPE = json.loads(
            BACKTEST_MARKET_TICKER_EVENT.substitute())["type"]
        # order event
        self.ORDER_MARKET_KLINE_EVENT_TYPE = json.loads(
            ORDER_MARKET_KLINE_EVENT.substitute())["type"]
        self.ORDER_MARKET_TICKER_EVENT_TYPE = json.loads(
            ORDER_MARKET_TICKER_EVENT.substitute())["type"]
        self.ORDER_CONFIRM_EVENT_TYPE = json.loads(
            ORDER_CONFIRM_EVENT.substitute())["type"]
        self.ORDER_CANCEL_EVENT_TYPE = json.loads(
            ORDER_CANCEL_EVENT.substitute())["type"]
        # statistic event
        self.STATISTIC_BACKTEST_EVENT_TYPE = json.loads(
            STATISTIC_BACKTEST_EVENT.substitute())["type"]
        self.STATISTIC_ORDER_EVENT_TYPE = json.loads(
            STATISTIC_ORDER_EVENT.substitute())["type"]
        # handler
        # listen handler
        self.LISTEN_ACCOUNT_BALANCE_EVENT_HANDLER = self._handler.handleListenAccountBalanceEvent
        self.LISTEN_ACCOUNT_WITHDRAW_EVENT_HANDLER = self._handler.handleListenAccountWithdrawEvent
        self.LISTEN_MARKET_KLINE_EVENT_HANDLER = self._handler.handleListenMarketKlineEvent
        self.LISTEN_MARKET_TICKER_EVENT_HANDLER = self._handler.handleListenMarketTickerEvent
        self.LISTEN_MARKET_DEPTH_EVENT_HANDLER = self._handler.handleListenMarketDepthEvent
        # judge handler
        self.JUDGE_MARKET_KLINE_EVENT_HANDLER = self._handler.handleJudgeMarketKlineEvent
        self.JUDGE_MARKET_TICKER_EVENT_HANDLER = self._handler.handleJudgeMarketTickerEvent
        # backtest handler
        self.BACKTEST_MARKET_KLINE_EVENT_HANDLER = self._handler.handleBacktestMarketKlineEvent
        self.BACKTEST_MARKET_TICKER_EVENT_HANDLER = self._handler.handleBacktestMarketTickerEvent
        # order handler
        self.ORDER_MARKET_KLINE_EVENT_HANDLER = self._handler.handleOrderMarketKlineEvent
        self.ORDER_MARKET_TICKER_EVENT_HANDLER = self._handler.handleOrderMarketTickerEvent
        self.ORDER_CONFIRM_EVENT_HANDLER = self._handler.handleOrderConfirmEvent
        self.ORDER_CANCEL_EVENT_HANDLER = self._handler.handleOrderCancelEvent
        # statistic handler
        self.STATISTIC_BACKTEST_EVENT_HANDLER = self._handler.handleStatisticBacktestEvent
        self.STATISTIC_ORDER_EVENT_HANDLER = self._handler.handleStatisticOrderEvent

    def register(self):
        self._logger.info("src.core.engine.register.Register.register")
        try:
            # 注册事件
            self._eventEngine.register(
                self.LISTEN_ACCOUNT_BALANCE_EVENT_TYPE,
                self.LISTEN_ACCOUNT_BALANCE_EVENT_HANDLER)
            self._eventEngine.register(
                self.LISTEN_ACCOUNT_WITHDRAW_EVENT_TYPE,
                self.LISTEN_ACCOUNT_WITHDRAW_EVENT_HANDLER)
            self._eventEngine.register(self.LISTEN_MARKET_KLINE_EVENT_TYPE,
                                       self.LISTEN_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.register(self.LISTEN_MARKET_TICKER_EVENT_TYPE,
                                       self.LISTEN_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.register(self.LISTEN_MARKET_DEPTH_EVENT_TYPE,
                                       self.LISTEN_MARKET_DEPTH_EVENT_HANDLER)
            self._eventEngine.register(self.JUDGE_MARKET_KLINE_EVENT_TYPE,
                                       self.JUDGE_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.register(self.JUDGE_MARKET_TICKER_EVENT_TYPE,
                                       self.JUDGE_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.register(
                self.BACKTEST_MARKET_KLINE_EVENT_TYPE,
                self.BACKTEST_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.register(
                self.BACKTEST_MARKET_TICKER_EVENT_TYPE,
                self.BACKTEST_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.register(self.ORDER_MARKET_KLINE_EVENT_TYPE,
                                       self.ORDER_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.register(self.ORDER_MARKET_TICKER_EVENT_TYPE,
                                       self.ORDER_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.register(self.ORDER_CONFIRM_EVENT_TYPE,
                                       self.ORDER_CONFIRM_EVENT_HANDLER)
            self._eventEngine.register(self.ORDER_CANCEL_EVENT_TYPE,
                                       self.ORDER_CANCEL_EVENT_HANDLER)
            self._eventEngine.register(self.STATISTIC_BACKTEST_EVENT_TYPE,
                                       self.STATISTIC_BACKTEST_EVENT_HANDLER)
            self._eventEngine.register(self.STATISTIC_ORDER_EVENT_TYPE,
                                       self.STATISTIC_ORDER_EVENT_HANDLER)
        except Exception as err:
            errStr = "src.core.engine.register.Register.register: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def unregister(self):
        self._logger.info("src.core.engine.register.Register.unregister")
        try:
            # 注销事件
            self._eventEngine.unregister(
                self.LISTEN_ACCOUNT_BALANCE_EVENT_TYPE,
                self.LISTEN_ACCOUNT_BALANCE_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.LISTEN_ACCOUNT_WITHDRAW_EVENT_TYPE,
                self.LISTEN_ACCOUNT_WITHDRAW_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.LISTEN_MARKET_KLINE_EVENT_TYPE,
                self.LISTEN_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.LISTEN_MARKET_TICKER_EVENT_TYPE,
                self.LISTEN_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.LISTEN_MARKET_DEPTH_EVENT_TYPE,
                self.LISTEN_MARKET_DEPTH_EVENT_HANDLER)
            self._eventEngine.unregister(self.JUDGE_MARKET_KLINE_EVENT_TYPE,
                                         self.JUDGE_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.JUDGE_MARKET_TICKER_EVENT_TYPE,
                self.JUDGE_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.BACKTEST_MARKET_KLINE_EVENT_TYPE,
                self.BACKTEST_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.BACKTEST_MARKET_TICKER_EVENT_TYPE,
                self.BACKTEST_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.unregister(self.ORDER_MARKET_KLINE_EVENT_TYPE,
                                         self.ORDER_MARKET_KLINE_EVENT_HANDLER)
            self._eventEngine.unregister(
                self.ORDER_MARKET_TICKER_EVENT_TYPE,
                self.ORDER_MARKET_TICKER_EVENT_HANDLER)
            self._eventEngine.unregister(self.ORDER_CONFIRM_EVENT_TYPE,
                                         self.ORDER_CONFIRM_EVENT_HANDLER)
            self._eventEngine.unregister(self.ORDER_CANCEL_EVENT_TYPE,
                                         self.ORDER_CANCEL_EVENT_HANDLER)
            self._eventEngine.unregister(self.STATISTIC_BACKTEST_EVENT_TYPE,
                                         self.STATISTIC_BACKTEST_EVENT_HANDLER)
            self._eventEngine.unregister(self.STATISTIC_ORDER_EVENT_TYPE,
                                         self.STATISTIC_ORDER_EVENT_HANDLER)
        except Exception as err:
            errStr = "src.core.engine.register.Register.unregister: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)
