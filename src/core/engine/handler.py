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

    def processJudgeMarketTickerCalcSignalTickerDis(self, exchange, threshold,
                                                    resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processJudgeMarketTickerCalcSignalTickerDis: {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalDis = calc.calcSignalTickerDis(exchange, threshold,
                                                 resInfoSymbol)
            if not signalDis == []:
                db.insertSignalTickerDis(signalDis)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processJudgeMarketTickerCalcSignalTickerDis:  {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                current_process().name, exchange, threshold, resInfoSymbol,
                EngineException(err))
            self._logger.error(errStr)

    def processJudgeMarketTickerCalcSignalTickerTra(self, exchange, threshold,
                                                    resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processJudgeMarketTickerCalcSignalTickerTra: {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalTra = calc.calcSignalTickerTra(exchange, threshold,
                                                 resInfoSymbol)
            if not signalTra == []:
                db.insertSignalTickerTra(signalTra)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processJudgeMarketTickerCalcSignalTickerTra:  {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
                current_process().name, exchange, threshold, resInfoSymbol,
                EngineException(err))
            self._logger.error(errStr)

    def processJudgeMarketTickerCalcSignalTickerPair(self, exchange, threshold,
                                                     resInfoSymbol):
        self._logger.debug(
            "src.core.engine.handler.Handler.processJudgeMarketTickerCalcSignalTickerPair: {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (current_process().name, exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            calc = Calc()
            signalPair = calc.calcSignalTickerPair(
                exchange, TYPE_PAIR_THRESHOLD, resInfoSymbol)
            if not signalPair == []:
                db.insertSignalTickerPair(signalPair)
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processJudgeMarketTickerCalcSignalTickerPair:  {process=%s, exchange=%s, threshold=%s, resInfoSymbol=%s}, err=%s" % (
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
                    target=self.processJudgeMarketTickerCalcSignalTickerDis,
                    name="processJudgeMarketTickerCalcSignalTickerDis",
                    args=(exchange, TYPE_DIS_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            # calc tra type
            if TYPE_TRA in types:
                p = Process(
                    target=self.processJudgeMarketTickerCalcSignalTickerTra,
                    name="processJudgeMarketTickerCalcSignalTickerTra",
                    args=(exchange, TYPE_TRA_THRESHOLD, resInfoSymbol))
                prs.append(p)
                p.start()
            # calc pair type
            if TYPE_PAIR in types:
                p = Process(
                    target=self.processJudgeMarketTickerCalcSignalTickerPair,
                    name="processJudgeMarketTickerCalcSignalTickerPair",
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

    def processStatisticJudgeStatisticSignalTickerDis(self, exchange):
        self._logger.debug(
            "src.core.engine.handler.Handler.processStatisticJudgeStatisticSignalTickerDis: {process=%s, exchange=%s}"
            % (current_process().name, exchange))
        try:
            db = DB()
            calc = Calc()
            statisticDis = calc.statisticSignalTickerDis(exchange)
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processStatisticJudgeStatisticSignalTickerDis:  {process=%s, exchange=%s}, err=%s" % (
                current_process().name, exchange, EngineException(err))
            self._logger.error(errStr)

    def processStatisticJudgeStatisticSignalTickerTra(self, exchange):
        self._logger.debug(
            "src.core.engine.handler.Handler.processStatisticJudgeStatisticSignalTickerTra: {process=%s, exchange=%s}"
            % (current_process().name, exchange))
        try:
            db = DB()
            calc = Calc()
            statisticTra = calc.statisticSignalTickerTra(exchange)
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processStatisticJudgeStatisticSignalTickerTra:  {process=%s, exchange=%s}, err=%s" % (
                current_process().name, exchange, EngineException(err))
            self._logger.error(errStr)

    def processStatisticJudgeStatisticSignalTickerPair(self, exchange):
        self._logger.debug(
            "src.core.engine.handler.Handler.processStatisticJudgeStatisticSignalTickerPair: {process=%s, exchange=%s}"
            % (current_process().name, exchange))
        try:
            db = DB()
            calc = Calc()
            statisticPair = calc.statisticSignalTickerPair(exchange)
            pass
        except (DBException, CalcException, EngineException, Exception) as err:
            errStr = "src.core.engine.handler.Handler.processStatisticJudgeStatisticSignalTickerPair:  {process=%s, exchange=%s}, err=%s" % (
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
                    target=self.processStatisticJudgeStatisticSignalTickerDis,
                    name="processStatisticJudgeStatisticSignalTickerDis",
                    args=(exchange, ))
                prs.append(p)
                p.start()
            # calc tra type
            if TYPE_TRA in types:
                p = Process(
                    target=self.processStatisticJudgeStatisticSignalTickerTra,
                    name="processStatisticJudgeStatisticSignalTickerTra",
                    args=(exchange, ))
                prs.append(p)
                p.start()
            # calc pair type
            if TYPE_PAIR in types:
                p = Process(
                    target=self.processStatisticJudgeStatisticSignalTickerPair,
                    name="processStatisticJudgeStatisticSignalTickerPair",
                    args=(exchange, ))
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
