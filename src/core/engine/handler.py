# -*- coding: utf-8 -*-
import time
from itertools import combinations
from string import Template

import pandas as pd

from src.core.calc.calc import Calc
from src.core.calc.enums import SIGNAL_MAX_NUM
from src.core.calc.signal import Signal
from src.core.db.db import DB
from src.core.engine.enums import *
from src.core.util.exceptions import (CalcException, DBException,
                                      EngineException)
from src.core.util.helper import str_to_list, utcnow_timestamp
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
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        [exchange] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertAccountBalanceHistory(exchange)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Account Withdraw 事件
    def handleListenAccountWithdrawEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        [exchange, asset] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertAccountWithdrawHistoryAsset(exchange, asset)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Market Depth 事件
    def handleListenMarketDepthEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketDepthEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        [exchange, fSymbol, tSymbol, limit] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenDepthEvent { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Market Kline 事件
    def handleListenMarketKlineEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketKlineEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        [exchange, fSymbol, tSymbol, interval, start, end] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                                 end)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Market ticker 事件
    def handleListenMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketTickerEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        [exchange, fSymbol, tSymbol, aggDepth] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol, aggDepth)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Judge 事件
    def handleJudgeMarketDepthEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketDepthEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        [args] = event.args
        try:
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketDepthEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    def handleJudgeMarketKlineEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        [args] = event.args
        try:
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    def handleJudgeMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: " +
            event.type)
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
                signalDis = calc.calcJudgeMarketTickerDis(
                    exchange, TYPE_DIS_THRESHOLD, resInfoSymbol)
                if not signalDis == []:
                    db.insertJudgeMarketTickerDis(signalDis)
            # calc tra type
            if TYPE_TRA in types:
                signalTra = calc.calcJudgeMarketTickerTra(
                    exchange, TYPE_TRA_THRESHOLD, resInfoSymbol)
                if not signalTra == []:
                    db.insertJudgeMarketTickerTra(signalTra)
            # calc pair type
            if TYPE_PAIR in types:
                signalPair = calc.calcJudgeMarketTickerPair(
                    exchange, TYPE_PAIR_THRESHOLD, resInfoSymbol)
                if not signalPair == []:
                    db.insertJudgeMarketTickerPair(signalPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Backtest 事件
    def handleBacktestHistoryCreatEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        [exchange, signals, timeout] = event.args
        exchange = str_to_list(exchange)
        signals = str_to_list(signals)
        timeout = float(timeout)
        # 处理事件
        try:
            db = DB()
            sgn = Signal(signals)
            resInfoSymbol = pd.DataFrame(db.getViewMarketSymbolPairs(exchange))
            # 0. start
            startTime = time.time()
            str = "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: { type=%s, priority=%s, args=%s }" % (
                event.type, event.priority, event.args)
            warnStr = Template(
                ", err=$err, backtest trade filed at $here, will try again...")
            errStr = Template(
                "BACKTEST TRADE ERROR. pre trade failed at $here.")
            ########################################
            # 1. pre trade
            # 1.1 calc pre orders
            preOrders = []
            isError = SIGNAL_MAX_NUM
            while isError > 0:
                try:
                    isError = isError - 1
                    preOrders = sgn.backtestSignalsPreTrade(resInfoSymbol)
                    isError = 0
                except Exception as err:
                    self._logger.warn(str + warnStr.substitute(
                        err=err, here='1.1 calc pre orders'))
            if isError>0:
                raise Exception(errStr.substitute(here='1.1 calc pre orders'))
            # 1.2 calc preExecOrders
            preExecOrders = []
            if not preOrders == []:
                for order in preOrders:
                    isError = SIGNAL_MAX_NUM
                    while isError > 0:
                        try:
                            isError = isError - 1
                            res = db.insertCreatTradeBacktestHistory(
                                order['server'], order['fSymbol'],
                                order['tSymbol'], order['ask_or_bid'],
                                order['price'], order['quantity'],
                                order['ratio'], order['type'],
                                order['group_id'])
                            isError = 0
                        except Exception as err:
                            self._logger.warn(str + warnStr.substitute(
                                err=err, here='1.2 excute preOrders'))
                    if not res == []:
                        preExecOrders.extend(res)
                if isError>0:
                    # rollback:
                    raise Exception(
                        errStr.substitute(here='1.2 excute preOrders'))
            # 1.3 calc preInfoOrders
            preInfoOrders = []
            if not preExecOrders == []:
                preExecOrders = pd.DataFrame(preExecOrders)
                for server in exchange:
                    orderIDs = preExecOrders[(preExecOrders['server'] == server
                                              )]['order_id'].tolist()
                    res = db.getTradeBacktestHistoryServerOrder([server],
                                                                orderIDs)
                    if not res == []:
                        preInfoOrders.extend(res)
            # 1.4 update signals status
            if not preInfoOrders == []:
                preInfoOrders = pd.DataFrame(preInfoOrders)
                isError = SIGNAL_MAX_NUM
                while isError > 0:
                    try:
                        isError = isError - 1
                        sgn.backtestUpdateSignalStatusByOrders(
                            preInfoOrders, resInfoSymbol)
                        isError = 0
                    except Exception as err:
                        self._logger.warn(str + warnStr.substitute(
                            err=err, here='1.4 update signal status'))
                if isError>0:
                    # rollback:

                    raise Exception(
                        errStr.substitute(here='1.4 update signal status'))
                print('1. pre signals after update:\n%s' % sgn.signals())
            ########################################
            # 2. run trade
            # 2.1 calc run orders
            runOrders = []
            isSubError = SIGNAL_MAX_NUM
            while isSubError > 0 and (time.time() - startTime < timeout
                                      or timeout == 0):
                try:
                    isSubError = isSubError - 1
                    runOrders = sgn.backtestSignalsRunTrade(resInfoSymbol)
                    isSubError = 0
                except Exception as err:
                    self._logger.warn(str + warnStr.substitute(
                        err=err, here='2.1 calc run orders'))
            if isSubError>0:
                # rollback:
                raise Exception(errStr.substitute(here='2.1 calc run orders'))
            # 2.2 calc runExecOrders
            print('runOrders=%s' % runOrders)
            runExecOrders = []
            if not runOrders == []:
                for order in runOrders:
                    isSubError = SIGNAL_MAX_NUM
                    while isSubError > 0 and (time.time() - startTime < timeout
                                              or timeout == 0):
                        try:
                            isSubError = isSubError - 1
                            res = db.insertCreatTradeBacktestHistory(
                                order['server'], order['fSymbol'],
                                order['tSymbol'], order['ask_or_bid'],
                                order['price'], order['quantity'],
                                order['ratio'], order['type'],
                                order['group_id'])
                            isSubError = 0
                        except Exception as err:
                            self._logger.warn(str + warnStr.substitute(
                                err=err, here='2.2 execute runOrders'))
                    if not res == []:
                        runExecOrders.extend(res)
                if isSubError>0:
                    # rollback:
                    raise Exception(
                        errStr.substitute(here='2.2 execute runOrders'))
            # 2.3 calc runInfoOrders
            runInfoOrders = []
            if not runExecOrders == []:
                runExecOrders = pd.DataFrame(runExecOrders)
                for server in exchange:
                    orderIDs = runExecOrders[(runExecOrders['server'] == server
                                              )]['order_id'].tolist()
                    res = db.getTradeBacktestHistoryServerOrder([server],
                                                                orderIDs)
                    if not res == []:
                        runInfoOrders.extend(res)
            # 2.4 update signals status
            if not runInfoOrders == []:
                runInfoOrders = pd.DataFrame(runInfoOrders)
                isSubError = SIGNAL_MAX_NUM
                while isSubError > 0 and (time.time() - startTime < timeout
                                          or timeout == 0):
                    try:
                        isSubError = isSubError - 1
                        sgn.backtestUpdateSignalStatusByOrders(
                            runInfoOrders, resInfoSymbol)
                        isSubError = 0
                    except Exception as err:
                        self._logger.warn(str + warnStr.substitute(
                            err=err, here='2.4 update signal status'))
                if isSubError>0:
                    # rollback:
                    raise Exception(
                        errStr.substitute(here='2.4 update signal status'))
                print('2. run signals after update:\n%s' % sgn.signals())
            ########################################
            # 3. after trade
            # 3.1 calc after orders
            afterOrders = []
            isError = SIGNAL_MAX_NUM
            while isError > 0:
                try:
                    isError = isError - 1
                    afterOrders = sgn.backtestSignalsAfterTrade(resInfoSymbol)
                    isError = 0
                except Exception as err:
                    self._logger.warn(str + warnStr.substitute(
                        err=err, here='3.1 calc after orders'))
            if isError>0:
                raise Exception(
                    errStr.substitute(here='3.1 calc after orders'))
            # 3.2 calc afterExecOrders
            afterExecOrders = []
            if not afterOrders == []:
                for order in afterOrders:
                    isError = SIGNAL_MAX_NUM
                    while isError > 0:
                        try:
                            isError = isError - 1
                            res = db.insertCreatTradeBacktestHistory(
                                order['server'], order['fSymbol'],
                                order['tSymbol'], order['ask_or_bid'],
                                order['price'], order['quantity'],
                                order['ratio'], order['type'],
                                order['group_id'])
                            isError = 0
                        except Exception as err:
                            self._logger.warn(str + warnStr.substitute(
                                err=err, here='3.2 excute preOrders'))
                    if not res == []:
                        preExecOrders.extend(res)
                if isError>0:
                    # rollback:
                    raise Exception(
                        errStr.substitute(here='3.2 excute preOrders'))
            # 3.3 calc afterInfoOrders
            afterInfoOrders = []
            if not afterExecOrders == []:
                afterExecOrders = pd.DataFrame(afterExecOrders)
                for server in exchange:
                    orderIDs = preExecOrders[(preExecOrders['server'] == server
                                              )]['order_id'].tolist()
                    res = db.getTradeBacktestHistoryServerOrder([server],
                                                                orderIDs)
                    if not res == []:
                        preInfoOrders.extend(res)
            # 3.4 update signals status
            if not preInfoOrders == []:
                preInfoOrders = pd.DataFrame(preInfoOrders)
                isError = SIGNAL_MAX_NUM
                while isError > 0:
                    try:
                        isError = isError - 1
                        sgn.backtestUpdateSignalStatusByOrders(
                            preInfoOrders, resInfoSymbol)
                        isError = 0
                    except Exception as err:
                        self._logger.warn(str + warnStr.substitute(
                            err=err, here='3.4 update signal status'))
                if isError>0:
                    # rollback:

                    raise Exception(
                        errStr.substitute(here='3.4 update signal status'))
                print('3. after signals after update:\n%s' % sgn.signals())

        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Order 事件
    def handleOrderHistoryInsertEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryInsertEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        [exchange, fSymbol, tSymbol, limit, ratio] = event.args
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertSyncTradeOrderHistory(exchange, fSymbol, tSymbol, limit,
                                           ratio)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleOrderHistoryInsertEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    def handleOrderHistoryCreatEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCreatEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        pass

    def handleOrderHistoryCheckEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCheckEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        pass

    def handleOrderHistoryCancelEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCancelEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        pass

    # Statistic 事件
    def handleStatisticJudgeEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticJudgeEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
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
                statisticDis = calc.calcStatisticJudgeMarketTickerDis(
                    exchange, TYPE_DIS_TIMEWINDOW)
                if not statisticDis == []:
                    db.insertStatisticJudgeMarketTickerDis(statisticDis)
            # calc tra type
            if TYPE_TRA in types:
                statisticTra = calc.calcStatisticJudgeMarketTickerTra(
                    exchange, TYPE_TRA_TIMEWINDOW)
                if not statisticTra == []:
                    db.insertStatisticJudgeMarketTickerTra(statisticTra)
            # calc pair type
            if TYPE_PAIR in types:
                statisticPair = calc.calcStatisticJudgeMarketTickerPair(
                    exchange, TYPE_PAIR_TIMEWINDOW)
                if not statisticPair == []:
                    db.insertStatisticJudgeMarketTickerPair(statisticPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleStatisticJudgeEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    def handleStatisticBacktestEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticBacktestEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        pass

    def handleStatisticOrderEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticOrderEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        pass
