# -*- coding: utf-8 -*-
import json
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
from src.core.util.helper import json_reverse, str_to_list, utcnow_timestamp
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
    def rollbackHandleBacktestHistoryCreatEvent(self, sgn, pdOrders, exchange, resInfoSymbol):
        self._logger.debug("src.core.engine.handler.Handler.rollbackHandleBacktestHistoryCreatEvent")
        try:
            db = DB()
            # update orders sgn status
            infoOrders = []
            if not pdOrders.empty:
                for server in exchange:
                    res = []
                    orderIDs = pdOrders[(pdOrders['server'] == server
                                              )]['order_id'].tolist()
                    res = db.getTradeBacktestHistoryServerOrder([server],
                                                                orderIDs)
                    if not res == []:
                        infoOrders.extend(res)
            if not infoOrders == []:
                infoOrders = pd.DataFrame(infoOrders)
                isError = SIGNAL_MAX_NUM
                while isError > 0:
                    try:
                        isError = isError - 1
                        sgn.backtestUpdateSignalStatusByOrders(
                            infoOrders, resInfoSymbol)
                        isError = 0
                    except Exception as err:
                        self._logger.warn('rollback failed, will try again...')
                if isError > 0:
                    raise Exception('rollback error, start_base assets may loss control.')
                # insert db signals
                db.insertSignalTradeDis(
                    sgn.signals(exchange, [TYPE_DIS]), SIGNAL_BACKTEST)
                db.insertSignalTradeTra(
                    sgn.signals(exchange, [TYPE_TRA]), SIGNAL_BACKTEST)
                db.insertSignalTradePair(
                    sgn.signals(exchange, [TYPE_PAIR]), SIGNAL_BACKTEST)
            # rollback assets
            isError = SIGNAL_MAX_NUM
            while isError > 0:
                isError = isError - 1
                # calc after orders
                afterOrders = []
                isSubError = SIGNAL_MAX_NUM
                while isSubError > 0:
                    try:
                        isSubError = isSubError - 1
                        afterOrders = sgn.backtestSignalsAfterTrade(
                            resInfoSymbol)
                        isSubError = 0
                    except Exception as err:
                        self._logger.warn('rollback failed, will try again...')
                if isSubError > 0:
                    raise Exception('rollback error, start_base assets may loss control.')
                # calc afterExecOrders
                afterExecOrders = []
                if not afterOrders == []:
                    for order in afterOrders:
                        identify = identify + 1
                        isSubError = SIGNAL_MAX_NUM
                        res = []
                        while isSubError > 0:
                            try:
                                isSubError = isSubError - 1
                                res = db.insertCreatTradeBacktestHistory(
                                    order['server'], order['fSymbol'],
                                    order['tSymbol'], order['ask_or_bid'],
                                    order['price'], order['quantity'],
                                    order['ratio'], order['type'],
                                    order['signal_id'], order['group_id'], identify)
                                isSubError = 0
                            except Exception as err:
                                self._logger.warn('rollback failed, will try again...')
                        if not res == []:
                            afterExecOrders.extend(res)
                    if isSubError > 0:
                        raise Exception('rollback error, start_base assets may loss control.')
                # calc afterInfoOrders
                afterInfoOrders = []
                if not afterExecOrders == []:
                    afterExecOrders = pd.DataFrame(afterExecOrders)
                    for server in exchange:
                        res = []
                        orderIDs = preExecOrders[(
                            preExecOrders['server'] == server
                        )]['order_id'].tolist()
                        res = db.getTradeBacktestHistoryServerOrder([server],
                                                                    orderIDs)
                        if not res == []:
                            afterInfoOrders.extend(res)
                # update signals status
                if not afterInfoOrders == []:
                    afterInfoOrders = pd.DataFrame(afterInfoOrders)
                    isSubError = SIGNAL_MAX_NUM
                    while isSubError > 0:
                        try:
                            isSubError = isSubError - 1
                            sgn.backtestUpdateSignalStatusByOrders(
                                afterInfoOrders, resInfoSymbol)
                            isSubError = 0
                        except Exception as err:
                            self._logger.warn('rollback failed, will try again...')
                    if isSubError > 0:
                        raise Exception('rollback error, start_base assets may loss control.')
                    # insert db signals
                    db.insertSignalTradeDis(
                        sgn.signals(exchange, [TYPE_DIS]), SIGNAL_BACKTEST)
                    db.insertSignalTradeTra(
                        sgn.signals(exchange, [TYPE_TRA]), SIGNAL_BACKTEST)
                    db.insertSignalTradePair(
                        sgn.signals(exchange, [TYPE_PAIR]), SIGNAL_BACKTEST)
                # update isError
                isMore = sgn.backtestSignalsIsRunMore(resInfoSymbol)
                if not isMore:
                    isError = 0
        except Exception as err:
            errStr = "src.core.engine.handler.Handler.rollbackHandleBacktestHistoryCreatEvent, err=%s" % err
            self._logger.critical(errStr)

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
            identify = 0
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
            if isError > 0:
                raise Exception(errStr.substitute(here='1.1 calc pre orders'))
            # print('1. pre signals preOrders:\n%s' % preOrders)
            # 1.2 calc preExecOrders
            preExecOrders = []
            if not preOrders == []:
                for order in preOrders:
                    identify = identify + 1
                    isError = SIGNAL_MAX_NUM
                    res = []
                    while isError > 0:
                        try:
                            isError = isError - 1
                            res = db.insertCreatTradeBacktestHistory(
                                order['server'], order['fSymbol'],
                                order['tSymbol'], order['ask_or_bid'],
                                order['price'], order['quantity'],
                                order['ratio'], order['type'],
                                order['signal_id'], order['group_id'], identify)
                            isError = 0
                        except Exception as err:
                            self._logger.warn(str + warnStr.substitute(
                                err=err, here='1.2 excute preOrders'))
                    if not res == []:
                        preExecOrders.extend(res)
                if isError > 0:
                    # rollback:
                    pdOrders = pd.DataFrame(preExecOrders)
                    self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                    raise Exception(
                        errStr.substitute(here='1.2 excute preOrders'))
            # print('1. pre signals preExecOrders:\n%s' % preExecOrders)
            # 1.3 calc preInfoOrders
            preInfoOrders = []
            if not preExecOrders == []:
                preExecOrders = pd.DataFrame(preExecOrders)
                for server in exchange:
                    res = []
                    orderIDs = preExecOrders[(preExecOrders['server'] == server
                                              )]['order_id'].tolist()
                    res = db.getTradeBacktestHistoryServerOrder([server],
                                                                orderIDs)
                    if not res == []:
                        preInfoOrders.extend(res)
            # print('1. pre signals preInfoOrders:\n%s' % preInfoOrders)
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
                            err=err, here='1.4 update signals status'))
                if isError > 0:
                    # rollback:
                    pdOrders = preExecOrders
                    self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                    raise Exception(
                        errStr.substitute(here='1.4 update signals status'))
                # insert db signals
                db.insertSignalTradeDis(
                    sgn.signals(exchange, [TYPE_DIS]), SIGNAL_BACKTEST)
                db.insertSignalTradeTra(
                    sgn.signals(exchange, [TYPE_TRA]), SIGNAL_BACKTEST)
                db.insertSignalTradePair(
                    sgn.signals(exchange, [TYPE_PAIR]), SIGNAL_BACKTEST)
            print('1. pre signals after update:\n%s' % sgn.signals())
            ########################################
            # 2. run trade
            isError = True
            while isError and (time.time() - startTime < timeout
                               or timeout == 0):
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
                if isSubError > 0:
                    # rollback:
                    pdOrders = []
                    self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                    raise Exception(
                        errStr.substitute(here='2.1 calc run orders'))
                # print('2. run signals runOrders:\n%s' % runOrders)
                # 2.2 calc runExecOrders
                runExecOrders = []
                if not runOrders == []:
                    for order in runOrders:
                        identify = identify + 1
                        isSubError = SIGNAL_MAX_NUM
                        res = []
                        while isSubError > 0 and (time.time() - startTime <
                                                  timeout or timeout == 0):
                            try:
                                isSubError = isSubError - 1
                                res = db.insertCreatTradeBacktestHistory(
                                    order['server'], order['fSymbol'],
                                    order['tSymbol'], order['ask_or_bid'],
                                    order['price'], order['quantity'],
                                    order['ratio'], order['type'],
                                    order['signal_id'], order['group_id'], identify)
                                isSubError = 0
                            except Exception as err:
                                self._logger.warn(str + warnStr.substitute(
                                    err=err, here='2.2 execute runOrders'))
                        if not res == []:
                            runExecOrders.extend(res)
                    if isSubError > 0:
                        # rollback:
                        pdOrders = pd.DataFrame(runExecOrders)
                        self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                        raise Exception(
                            errStr.substitute(here='2.2 execute runOrders'))
                # print('2. run signals runExecOrders:\n%s' % runExecOrders)
                # 2.3 calc runInfoOrders
                runInfoOrders = []
                if not runExecOrders == []:
                    runExecOrders = pd.DataFrame(runExecOrders)
                    for server in exchange:
                        res = []
                        orderIDs = runExecOrders[(
                            runExecOrders['server'] == server
                        )]['order_id'].tolist()
                        res = db.getTradeBacktestHistoryServerOrder([server],
                                                                    orderIDs)
                        if not res == []:
                            runInfoOrders.extend(res)
                # print('2. run signals runInfoOrders:\n%s' % runInfoOrders)
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
                                err=err, here='2.4 update signals status'))
                    if isSubError > 0:
                        # rollback:
                        pdOrders = runExecOrders
                        self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                        raise Exception(
                            errStr.substitute(
                                here='2.4 update signals status'))
                    # insert db signals
                    db.insertSignalTradeDis(
                        sgn.signals(exchange, [TYPE_DIS]), SIGNAL_BACKTEST)
                    db.insertSignalTradeTra(
                        sgn.signals(exchange, [TYPE_TRA]), SIGNAL_BACKTEST)
                    db.insertSignalTradePair(
                        sgn.signals(exchange, [TYPE_PAIR]), SIGNAL_BACKTEST)
                print('2. run signals after update:\n%s' % sgn.signals())
                # 2.5 update isError
                isMore = sgn.backtestSignalsIsRunMore(resInfoSymbol)
                if not isMore:
                    isError = False
            ########################################
            # 3. after trade
            isError = SIGNAL_MAX_NUM
            while isError > 0:
                isError = isError - 1
                # 3.1 calc after orders
                afterOrders = []
                isSubError = SIGNAL_MAX_NUM
                while isSubError > 0:
                    try:
                        isSubError = isSubError - 1
                        afterOrders = sgn.backtestSignalsAfterTrade(
                            resInfoSymbol)
                        isSubError = 0
                    except Exception as err:
                        self._logger.warn(str + warnStr.substitute(
                            err=err, here='3.1 calc after orders'))
                if isSubError > 0:
                    # rollback
                    pdOrders = []
                    self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                    raise Exception(
                        errStr.substitute(here='3.1 calc after orders'))
                # print('3. after signals afterOrders:\n%s' % afterOrders)
                # 3.2 calc afterExecOrders
                afterExecOrders = []
                if not afterOrders == []:
                    for order in afterOrders:
                        identify = identify + 1
                        isSubError = SIGNAL_MAX_NUM
                        res = []
                        while isSubError > 0:
                            try:
                                isSubError = isSubError - 1
                                res = db.insertCreatTradeBacktestHistory(
                                    order['server'], order['fSymbol'],
                                    order['tSymbol'], order['ask_or_bid'],
                                    order['price'], order['quantity'],
                                    order['ratio'], order['type'],
                                    order['signal_id'], order['group_id'], identify)
                                isSubError = 0
                            except Exception as err:
                                self._logger.warn(str + warnStr.substitute(
                                    err=err, here='3.2 excute preOrders'))
                        if not res == []:
                            afterExecOrders.extend(res)
                    if isSubError > 0:
                        # rollback:
                        pdOrders = pd.DataFrame(afterExecOrders)
                        self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                        raise Exception(
                            errStr.substitute(here='3.2 excute preOrders'))
                # print('3. after signals afterExecOrders:\n%s' % afterExecOrders)
                # 3.3 calc afterInfoOrders
                afterInfoOrders = []
                if not afterExecOrders == []:
                    afterExecOrders = pd.DataFrame(afterExecOrders)
                    for server in exchange:
                        res = []
                        orderIDs = preExecOrders[(
                            preExecOrders['server'] == server
                        )]['order_id'].tolist()
                        res = db.getTradeBacktestHistoryServerOrder([server],
                                                                    orderIDs)
                        if not res == []:
                            afterInfoOrders.extend(res)
                # print('3. after signals afterInfoOrders:\n%s' % afterInfoOrders)
                # 3.4 update signals status
                if not afterInfoOrders == []:
                    afterInfoOrders = pd.DataFrame(afterInfoOrders)
                    isSubError = SIGNAL_MAX_NUM
                    while isSubError > 0:
                        try:
                            isSubError = isSubError - 1
                            sgn.backtestUpdateSignalStatusByOrders(
                                afterInfoOrders, resInfoSymbol)
                            isSubError = 0
                        except Exception as err:
                            self._logger.warn(str + warnStr.substitute(
                                err=err, here='3.4 update signals status'))
                    if isSubError > 0:
                        # rollback:
                        pdOrders = afterExecOrders
                        self.rollbackHandleBacktestHistoryCreatEvent(sgn, pdOrders, exchange, resInfoSymbol)
                        raise Exception(
                            errStr.substitute(
                                here='3.4 update signals status'))
                    # insert db signals
                    db.insertSignalTradeDis(
                        sgn.signals(exchange, [TYPE_DIS]), SIGNAL_BACKTEST)
                    db.insertSignalTradeTra(
                        sgn.signals(exchange, [TYPE_TRA]), SIGNAL_BACKTEST)
                    db.insertSignalTradePair(
                        sgn.signals(exchange, [TYPE_PAIR]), SIGNAL_BACKTEST)
                print('3. after signals after update:\n%s' % sgn.signals())
                # 3.5 update isError
                isMore = sgn.backtestSignalsIsRunMore(resInfoSymbol)
                if not isMore:
                    isError = 0
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    # Order 事件
    def handleOrderHistorySyncEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistorySyncEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
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
            errStr = "src.core.engine.handler.Handler.handleOrderHistorySyncEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
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
        [signals] = event.args
        signals = str_to_list(signals)
        for signal in signals:
            signal['status_assets'] = json.loads(
                json_reverse(signal['status_assets']))
        try:
            db = DB()
            calc = Calc()
            statistic = calc.calcStatisticTradeBacktestHistory(signals)
            db.insertStatisticTradeBacktestHistory(statistic)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleStatisticBacktestEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)

    def handleStatisticOrderEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticOrderEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 接收事件
        [signals] = event.args
        signals = str_to_list(signals)
        for signal in signals:
            signal['status_assets'] = json.loads(
                json_reverse(signal['status_assets']))
        try:
            db = DB()
            calc = Calc()
            statistic = calc.calcStatisticTradeOrderHistory(signals)
            db.insertStatisticTradeOrderHistory(statistic)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleStatisticOrderEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, err)
            self._logger.error(errStr)
        callback(event.id)
