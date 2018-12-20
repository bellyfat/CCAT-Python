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
        exchange = str_to_list(exchange)
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
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertAccountWithdrawHistoryAsset(exchange, asset)
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
        exchange = str_to_list(exchange)
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
        exchange = str_to_list(exchange)
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
        exchange = str_to_list(exchange)
        try:
            db = DB()
            db.insertMarketTicker(exchange, fSymbol, tSymbol, aggDepth)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleListenTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleJudgeMarketDepthEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleJudgeMarketDepthEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        [args] = event.args
        try:
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketDepthEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
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

    def processJudgeMarketTickerCalcJudgeSignalTickerDis(self, exchange, threshold,
                                                    resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processJudgeMarketTickerCalcJudgeSignalTickerDis: {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalDis = calc.calcJudgeSignalTickerDis(exchange, threshold,
                                                 resInfoSymbol)
            if not signalDis == []:
                db.insertJudgeSignalTickerDis(signalDis)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processJudgeMarketTickerCalcJudgeSignalTickerDis:  {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                current_process().name, exchange, threshold, resInfoSymbol,
                EngineException(err))
            self._logger.error(errStr)

    def processJudgeMarketTickerCalcJudgeSignalTickerTra(self, exchange, threshold,
                                                    resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processJudgeMarketTickerCalcJudgeSignalTickerTra: {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalTra = calc.calcJudgeSignalTickerTra(exchange, threshold,
                                                 resInfoSymbol)
            if not signalTra == []:
                db.insertJudgeSignalTickerTra(signalTra)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processJudgeMarketTickerCalcJudgeSignalTickerTra:  {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                current_process().name, exchange, threshold, resInfoSymbol,
                EngineException(err))
            self._logger.error(errStr)

    def processJudgeMarketTickerCalcJudgeSignalTickerPair(self, exchange, threshold,
                                                     resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processJudgeMarketTickerCalcJudgeSignalTickerPair: {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalPair = calc.calcJudgeSignalTickerPair(
                exchange, TYPE_PAIR_THRESHOLD, resInfoSymbol)
            if not signalPair == []:
                db.insertJudgeSignalTickerPair(signalPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processJudgeMarketTickerCalcJudgeSignalTickerPair:  {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                current_process().name, exchange, threshold, resInfoSymbol,
                EngineException(err))
            self._logger.error(errStr)

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
            resInfoSymbol = pd.DataFrame(db.getInfoSymbol(exchange))
            prs = []
            # calc dis type
            if TYPE_DIS in types:
                p = Process(
                    target=self.processJudgeMarketTickerCalcJudgeSignalTickerDis,
                    name="processJudgeMarketTickerCalcJudgeSignalTickerDis",
                    args=(exchange, TYPE_DIS_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            # calc tra type
            if TYPE_TRA in types:
                p = Process(
                    target=self.processJudgeMarketTickerCalcJudgeSignalTickerTra,
                    name="processJudgeMarketTickerCalcJudgeSignalTickerTra",
                    args=(exchange, TYPE_TRA_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            # calc pair type
            if TYPE_PAIR in types:
                p = Process(
                    target=self.processJudgeMarketTickerCalcJudgeSignalTickerPair,
                    name="processJudgeMarketTickerCalcJudgeSignalTickerPair",
                    args=(exchange, TYPE_PAIR_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            for p in prs:
                p.join()
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

    def handleBacktestHistoryCreatEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleBacktestHistoryCreatEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderHistoryInsertEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryInsertEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
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
        callback(event)

    def handleOrderHistoryCreatEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCreatEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderHistoryCheckEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCheckEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def handleOrderHistoryCancelEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleOrderHistoryCancelEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        pass

    def processStatisticJudgeCalcStatisticSignalTickerDis(self, exchange,
                                                      timeWindow):
        self._logger.debug(
            "src.core.engine.handler.Handler.processStatisticJudgeCalcStatisticSignalTickerDis: {process=%s, exchange=%s}"
            % (current_process().name, exchange))
        try:
            db = DB()
            calc = Calc()
            statisticDis = calc.calcStatisticSignalTickerDis(exchange, timeWindow)
            if not statisticDis == []:
                db.insertStatisticSignalTickerDis(statisticDis)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processStatisticJudgeCalcStatisticSignalTickerDis:  {process=%s, exchange=%s}, err=%s" % (
                current_process().name, exchange, EngineException(err))
            self._logger.error(errStr)

    def processStatisticJudgeCalcStatisticSignalTickerTra(self, exchange,
                                                      timeWindow):
        self._logger.debug(
            "src.core.engine.handler.Handler.processStatisticJudgeCalcStatisticSignalTickerTra: {process=%s, exchange=%s}"
            % (current_process().name, exchange))
        try:
            db = DB()
            calc = Calc()
            statisticTra = calc.calcStatisticSignalTickerTra(exchange, timeWindow)
            if not statisticTra == []:
                db.insertStatisticSignalTickerTra(statisticTra)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processStatisticJudgeCalcStatisticSignalTickerTra:  {process=%s, exchange=%s}, err=%s" % (
                current_process().name, exchange, EngineException(err))
            self._logger.error(errStr)

    def processStatisticJudgeCalcStatisticSignalTickerPair(self, exchange,
                                                       timeWindow):
        self._logger.debug(
            "src.core.engine.handler.Handler.processStatisticJudgeCalcStatisticSignalTickerPair: {process=%s, exchange=%s}"
            % (current_process().name, exchange))
        try:
            db = DB()
            calc = Calc()
            statisticPair = calc.calcStatisticSignalTickerPair(exchange, timeWindow)
            if not statisticPair == []:
                db.insertStatisticSignalTickerPair(statisticPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processStatisticJudgeCalcStatisticSignalTickerPair:  {process=%s, exchange=%s}, err=%s" % (
                current_process().name, exchange, EngineException(err))
            self._logger.error(errStr)

    def handleStatisticJudgeEvent(self, event, callback):
        self._logger.debug(
            "src.core.engine.handler.Handler.handleStatisticJudgeEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 接收事件
        [exchange, types] = event.args
        exchange = str_to_list(exchange)
        types = str_to_list(types)
        try:
            calc = Calc()
            prs = []
            # calc dis type
            if TYPE_DIS in types:
                p = Process(
                    target=self.processStatisticJudgeCalcStatisticSignalTickerDis,
                    name="processStatisticJudgeCalcStatisticSignalTickerDis",
                    args=(exchange, TYPE_DIS_TIMEWINDOW))
                prs.append(p)
                p.start()
            # calc tra type
            if TYPE_TRA in types:
                p = Process(
                    target=self.processStatisticJudgeCalcStatisticSignalTickerTra,
                    name="processStatisticJudgeCalcStatisticSignalTickerTra",
                    args=(exchange, TYPE_TRA_TIMEWINDOW))
                prs.append(p)
                p.start()
            # calc pair type
            if TYPE_PAIR in types:
                p = Process(
                    target=self.processStatisticJudgeCalcStatisticSignalTickerPair,
                    name="processStatisticJudgeCalcStatisticSignalTickerPair",
                    args=(exchange, TYPE_PAIR_TIMEWINDOW))
                prs.append(p)
                p.start()
            for p in prs:
                p.join()
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.handleStatisticJudgeEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

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
