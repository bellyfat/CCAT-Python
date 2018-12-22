# -*- coding: utf-8 -*-
from itertools import combinations

import pandas as pd
from src.core.calc.signal import Signal
from src.core.calc.calc import Calc
from src.core.db.db import DB
from src.core.engine.enums import *
from src.core.util.exceptions import (CalcException, DBException,
                                      EngineException)
from src.core.util.helper import str_to_list
from src.core.util.log import Logger


class Handler(object):
    def __init__(self, eventEngine):
        self._engine = eventEngine
        self._logger = Logger()

    # Account Balance 事件
    def handleListenAccountBalanceEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        [exchange] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertAccountBalanceHistory(exchange)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Account Withdraw 事件
    def handleListenAccountWithdrawEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        [exchange, asset] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertAccountWithdrawHistoryAsset(exchange, asset)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Market Depth 事件
    def handleListenMarketDepthEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketDepthEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        [exchange, fSymbol, tSymbol, limit] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenDepthEvent { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Market Kline 事件
    def handleListenMarketKlineEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketKlineEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        [exchange, fSymbol, tSymbol, interval, start, end] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                                 end)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Market ticker 事件
    def handleListenMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketTickerEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        [exchange, fSymbol, tSymbol, aggDepth] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol, aggDepth)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Judge 事件
    def handleJudgeMarketDepthEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketDepthEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        [args] = event.args
        try:
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketDepthEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    def handleJudgeMarketKlineEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        [args] = event.args
        try:
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    def handleJudgeMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: "
            + event.type)
        # 接收事件
        [exchange, types] = event.args
        exchange = str_to_list(exchange)
        types = str_to_list(types)
        try:
            db = DB()
            calc = Calc()
            resInfoSymbol = pd.DataFrame(db.getViewMarketSymbolPairs(exchange))
            prs = []
            # calc dis type
            if TYPE_DIS in types:
                signalDis = calc.calcJudgeSignalTickerDis(exchange, TYPE_DIS_THRESHOLD,
                                                          resInfoSymbol)
                if not signalDis == []:
                    db.insertJudgeSignalTickerDis(signalDis)
            # calc tra type
            if TYPE_TRA in types:
                signalTra = calc.calcJudgeSignalTickerTra(exchange, TYPE_TRA_THRESHOLD,
                                                          resInfoSymbol)
                if not signalTra == []:
                    db.insertJudgeSignalTickerTra(signalTra)
            # calc pair type
            if TYPE_PAIR in types:
                signalPair = calc.calcJudgeSignalTickerPair(
                    exchange, TYPE_PAIR_THRESHOLD, resInfoSymbol)
                if not signalPair == []:
                    db.insertJudgeSignalTickerPair(signalPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Backtest 事件
    def handleBacktestHistoryCreatEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        [signals, timeout] = event.args
        signals = str_to_list(signals)
        try:
            db = DB()
            sgn = Signal(signals)
            resInfoSymbol = pd.DataFrame(db.getViewMarketSymbolPairs(exchange))
            # pre trans
            res = sgn.backtestSignalsPreTrans(resInfoSymbol, timeout)

            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    # Order 事件
    def handleOrderHistoryInsertEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryInsertEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        [exchange, fSymbol, tSymbol, limit, ratio] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertTradeOrderHistory(exchange, fSymbol, tSymbol, limit,
                                       ratio)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleOrderHistoryInsertEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    def handleOrderHistoryCreatEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCreatEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        pass

    def handleOrderHistoryCheckEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCheckEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        pass

    def handleOrderHistoryCancelEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCancelEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        pass

    # Statistic 事件
    def handleStatisticJudgeEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticJudgeEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        [exchange, types] = event.args
        exchange = str_to_list(exchange)
        types = str_to_list(types)
        try:
            db = DB()
            calc = Calc()
            prs = []
            # calc dis type
            if TYPE_DIS in types:
                statisticDis = calc.calcStatisticSignalTickerDis(
                    exchange, TYPE_DIS_TIMEWINDOW)
                if not statisticDis == []:
                    db.insertStatisticSignalTickerDis(statisticDis)
            # calc tra type
            if TYPE_TRA in types:
                statisticTra = calc.calcStatisticSignalTickerTra(
                    exchange, TYPE_TRA_TIMEWINDOW)
                if not statisticTra == []:
                    db.insertStatisticSignalTickerTra(statisticTra)
            # calc pair type
            if TYPE_PAIR in types:
                statisticPair = calc.calcStatisticSignalTickerPair(
                    exchange, TYPE_PAIR_TIMEWINDOW)
                if not statisticPair == []:
                    db.insertStatisticSignalTickerPair(statisticPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleStatisticJudgeEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event.id)

    def handleStatisticBacktestEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticBacktestEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        pass

    def handleStatisticOrderEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticOrderEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp, event.args))
        # 接收事件
        pass
