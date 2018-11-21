# -*- coding: utf-8 -*-

from src.core.engine.enums import *


class Register(object):
    def __init__(self):
        self._logger = Logger()

    def registeEvent(self, handler):
        self._logger.debug("src.core.engine.listen.Listen.registerListenEvent")
        # 构造事件
        ACCOUNT_BALANCE_EVETNT = Event(
            json.loads(LISTEN_ACCOUNT_BALANCE_EVENT.substitute(server="")))
        ACCOUNT_WITHDRAW_EVENT = Event(
            json.loads(
                LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute(server="", asset="")))
        DEPETH_EVETNT = Event(
            json.loads(
                LISTEN_MARKET_DEPTH_EVENT.substitute(
                    server="", fSymbol="", tSymbol="", limit="")))
        KLINE_EVENT = Event(
            json.loads(
                LISTEN_MARKET_KLINE_EVENT.substitute(
                    server="",
                    fSymbol="",
                    tSymbol="",
                    interval="",
                    start="",
                    end="")))
        TICKER_EVENT = Event(
            json.loads(
                LISTEN_MARKET_TICKER_EVENT.substitute(
                    server="", fSymbol="", tSymbol="")))
        # 构造 handler
        ACCOUNT_BALANCE_EVETNT_HANDLER = handler.handleListenAccountBalanceEvent
        ACCOUNT_WITHDRAW_EVENT_HANDLER = handler.handleListenAccountWithdrawEvent
        DEPETH_EVETNT_HANDLER = handler.handleListenDepthEvent
        KLINE_EVETNT_HANDLER = handler.handleListenKlineEvent
        TICKER_EVETNT_HANDLER = handler.handleListenTickerEvent
        # 注册事件
        self._engine.register(ACCOUNT_BALANCE_EVETNT,
                              ACCOUNT_BALANCE_EVETNT_HANDLER)
        self._engine.register(ACCOUNT_WITHDRAW_EVENT,
                              ACCOUNT_WITHDRAW_EVENT_HANDLER)
        self._engine.register(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.register(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.register(TICKER_EVENT, TICKER_EVETNT_HANDLER)

    def unRegisterListenEvent(self, handler):
        self._logger.debug(
            "src.core.engine.listen.Listen.unregisterListenEvent")
        # 构造事件
        ACCOUNT_BALANCE_EVETNT = Event(
            json.loads(LISTEN_ACCOUNT_BALANCE_EVENT.substitute(server="")))
        ACCOUNT_WITHDRAW_EVENT = Event(
            json.loads(
                LISTEN_ACCOUNT_WITHDRAW_EVENT.substitute(server="", asset="")))
        DEPETH_EVETNT = Event(
            json.loads(
                LISTEN_MARKET_DEPTH_EVENT.substitute(
                    server="", fSymbol="", tSymbol="", limit="")))
        KLINE_EVENT = Event(
            json.loads(
                LISTEN_MARKET_KLINE_EVENT.substitute(
                    server="",
                    fSymbol="",
                    tSymbol="",
                    interval="",
                    start="",
                    end="")))
        TICKER_EVENT = Event(
            json.loads(
                LISTEN_MARKET_TICKER_EVENT.substitute(
                    server="", fSymbol="", tSymbol="")))
        # 构造 handler
        ACCOUNT_BALANCE_EVETNT_HANDLER = handler.handleListenAccountBalanceEvent
        ACCOUNT_WITHDRAW_EVENT_HANDLER = handler.handleListenAccountWithdrawEvent
        DEPETH_EVETNT_HANDLER = handler.handleListenDepthEvent
        KLINE_EVETNT_HANDLER = handler.handleListenKlineEvent
        TICKER_EVETNT_HANDLER = handler.handleListenTickerEvent
        # 注销事件
        self._engine.unregister(ACCOUNT_BALANCE_EVETNT,
                                ACCOUNT_BALANCE_EVETNT_HANDLER)
        self._engine.unregister(ACCOUNT_WITHDRAW_EVENT,
                                ACCOUNT_WITHDRAW_EVENT_HANDLER)
        self._engine.unregister(DEPETH_EVETNT, DEPETH_EVETNT_HANDLER)
        self._engine.unregister(KLINE_EVENT, KLINE_EVETNT_HANDLER)
        self._engine.unregister(TICKER_EVENT, TICKER_EVETNT_HANDLER)
