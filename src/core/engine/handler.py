# -*- coding: utf-8 -*-

from itertools import combinations
from multiprocessing import Process, current_process

import pandas as pd

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

    def handleListenAccountBalanceEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        [exchange] = event.args
        try:
            db = DB()
            db.insertAccountBalanceHistory(exchange)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountBalanceEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleListenAccountWithdrawEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        [exchange, asset] = event.args
        try:
            db = DB()
            db.insertAccountWithdrawHistory(exchange, asset)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenAccountWithdrawEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleListenMarketDepthEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketDepthEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        [exchange, fSymbol, tSymbol, limit] = event.args
        try:
            db = DB()
            db.insertMarketDepth(exchange, fSymbol, tSymbol, limit)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenDepthEvent { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleListenMarketKlineEvent(self, event, callback):
        # 接收事件
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketKlineEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        [exchange, fSymbol, tSymbol, interval, start, end] = event.args
        try:
            db = DB()
            db.insertMarketKline(exchange, fSymbol, tSymbol, interval, start,
                                 end)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleListenMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleListenMarketTickerEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        [exchange, fSymbol, tSymbol, aggDepth] = event.args
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol, aggDepth)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleJudgeMarketKlineEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        [args] = event.args
        try:
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def processCalcSignalTickerDis(self, exchanges, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processCalcSignalTickerDis: {process=%s, exchanges=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchanges, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalDis = calc.calcSignalTickerDis(exchanges, threshold,
                                                 resInfoSymbol)
            if not signalDis == []:
                db.insertSignalTickerDis(signalDis)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processCalcSignalTickerDis:  {exchanges=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                exchanges, threshold, resInfoSymbol, Exception(err))
            self._logger.error(errStr)

    def processCalcSignalTickerTra(self, exchanges, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processCalcSignalTickerTra: {process=%s, exchanges=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchanges, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalTra = calc.calcSignalTickerTra(
                exchanges, threshold, resInfoSymbol)
            if not signalTra == []:
                db.insertSignalTickerTra(signalTra)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processCalcSignalTickerTra:  {exchanges=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                exchanges, threshold, resInfoSymbol, Exception(err))
            self._logger.error(errStr)

    def processCalcSignalTickerPair(self, exchanges, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processCalcSignalTickerPair: {process=%s, exchanges=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchanges, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalPair = calc.calcSignalTickerPair(
                exchanges, TYPE_PAIR_THRESHOLD, resInfoSymbol)
            if not signalPair == []:
                db.insertSignalTickerPair(signalPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processCalcSignalTickerPair:  {exchanges=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                exchanges, threshold, resInfoSymbol, Exception(err))
            self._logger.error(errStr)

    def handleJudgeMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: " +
            event.type)
        # 接收事件
        [types, exchanges] = event.args
        types = str_to_list(types)
        exchanges = str_to_list(exchanges)
        try:
            db = DB()
            calc = Calc()
            resInfoSymbol = pd.DataFrame(db.getInfoSymbol())
            prs=[]
            # calc dis type
            if TYPE_DIS in types:
                p = Process(target=self.processCalcSignalTickerDis, name="%s-processCalcSignalTickerDis" % TYPE_DIS, args=(exchanges, TYPE_DIS_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            # calc tra type
            if TYPE_TRA in types:
                p = Process(target=self.processCalcSignalTickerTra, name="%s-processCalcSignalTickerTra" % TYPE_TRA, args=(exchanges, TYPE_TRA_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            # calc pair type
            if TYPE_PAIR in types:
                p = Process(target=self.processCalcSignalTickerPair, name="%s-processCalcSignalTickerPair" % TYPE_PAIR, args=(exchanges, TYPE_PAIR_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            for p in prs:
                p.join()
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleBacktestMarketKlineEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestMarketKlineEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleBacktestMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestMarketTickerEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderMarketKlineEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderMarketKlineEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderMarketTickerEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderMarketTickerEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderConfirmEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderConfirmEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderCancelEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderCancelEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleStatisticBacktestEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticBacktestEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleStatisticOrderEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticOrderEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass
