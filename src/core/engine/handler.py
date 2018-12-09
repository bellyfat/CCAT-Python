# -*- coding: utf-8 -*-

import json
from itertools import combinations

import pandas as pd

from src.core.db.db import DB
from src.core.engine.enums import *
from src.core.util.exceptions import DBException, EngineException
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
        except DBException as err:
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
        except DBException as err:
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
        except DBException as err:
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
        except DBException as err:
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
        except DBException as err:
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
        except DBException as err:
            errStr = "src.core.engine.handler.Handler.handleJudgeMarketKlineEvent: { type=%s, priority=%s, args=%s }, err=%s" % (
                event.type, event.priority, event.args, EngineException(err))
            self._logger.error(errStr)
        callback(event)

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
            resInfoSymbol = pd.DataFrame(db.getInfoSymbol())
            signal = []
            # calc dis type
            if CCAT_DIS_TYPE in types:
                for item in combinations(exchanges, 2):
                    df = []
                    res = db.getViewMarketTickerCurrentDisServer(
                        item[0], item[1])
                    # calc gains with fee
                    for r in res:
                        bid_fee = resInfoSymbol[
                            (resInfoSymbol['server'] == r['bid_server'])
                            & (resInfoSymbol['fSymbol'] == r['fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['tSymbol']
                             )]['fee_taker'].values[0]
                        ask_fee = resInfoSymbol[
                            (resInfoSymbol['server'] == r['ask_server'])
                            & (resInfoSymbol['fSymbol'] == r['fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['tSymbol']
                             )]['fee_taker'].values[0]
                        # calc gain_base
                        r['gain_base'] = r['bid_price_base'] * r[
                            'bid_size'] - r['ask_price_base'] * r[
                                'ask_size'] - r['bid_price_base'] * r[
                                    'bid_size'] * bid_fee - r[
                                        'ask_price_base'] * r[
                                            'ask_size'] * ask_fee
                        # calc gain_ratio
                        r['gain_ratio'] = (r['bid_price'] - r['ask_price'] -
                                           r['bid_price'] * bid_fee -
                                           r['ask_price'] * ask_fee) / (
                                               r['bid_price'] + r['ask_price'])
                        df.append(r)
                    df = pd.DataFrame(df)
                    df['gain_ratio_group'] = df.groupby(
                        ['fSymbol',
                         'tSymbol'])['gain_ratio'].transform(lambda x: x.sum())
                    # 判断是否产生交易信号
                    sig = df[df['gain_ratio_group'] > 0]
                    if not sig.empty:
                        signal.append({'type': CCAT_DIS_TYPE, 'sig': sig})
            # calc tra type
            if CCAT_TRA_TYPE in types:
                for item in exchanges:
                    df = []
                    res = db.getViewMarketTickerCurrentTraServer([item])
                    # calc gains with fee
                    for r in res:
                        V1_fee = resInfoSymbol[
                            (resInfoSymbol['server'] == r['server'])
                            & (resInfoSymbol['fSymbol'] == r['V1_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                             )]['fee_taker'].values[0]
                        V2_fee = resInfoSymbol[
                            (resInfoSymbol['server'] == r['server'])
                            & (resInfoSymbol['fSymbol'] == r['V2_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                             )]['fee_taker'].values[0]
                        V3_fee = resInfoSymbol[
                            (resInfoSymbol['server'] == r['server'])
                            & (resInfoSymbol['fSymbol'] == r['V3_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                             )]['fee_taker'].values[0]
                        C1_symbol = [
                            i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                            if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                        ]
                        C2_symbol = [
                            i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                            if i in [r['V2_fSymbol'], r['V2_tSymbol']]
                        ]
                        C3_symbol = [
                            i for i in [r['V2_fSymbol'], r['V2_tSymbol']]
                            if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                        ]
                        # calc V1
                        if C1_symbol == r['V1_fSymbol']:  # fSymbol -> tSymbol
                            C1_symbol_price = r['V1_bid_one_price']
                            C1_symbol_price_base = r['V1_bid_one_price_base']
                            C1_symbol_size = r['V1_bid_one_size']
                        else:  # tSymbol -> fSymbol
                            C1_symbol_price = 0 - r['V1_ask_one_price']
                            C1_symbol_price_base = 0 - r[
                                'V1_ask_one_price_base']
                            C1_symbol_size = r['V1_ask_one_size']
                        # calc V2
                        if C2_symbol == r['V2_fSymbol']:  # fSymbol -> tSymbol
                            C2_symbol_price = r['V2_bid_one_price']
                            C2_symbol_price_base = r['V2_bid_one_price_base']
                            C2_symbol_size = r['V2_bid_one_size']
                        else:  # tSymbol -> fSymbol
                            C2_symbol_price = 0 - r['V2_ask_one_price']
                            C2_symbol_price_base = 0 - r[
                                'V2_ask_one_price_base']
                            C2_symbol_size = r['V2_ask_one_size']
                        # calc V3
                        if C3_symbol == r['V3_fSymbol']:  # fSymbol -> tSymbol
                            C3_symbol_price = r['V3_bid_one_price']
                            C3_symbol_price_base = r['V3_bid_one_price_base']
                            C3_symbol_size = r['V3_bid_one_size']
                        else:  # tSymbol -> fSymbol
                            C3_symbol_price = 0 - r['V3_ask_one_price']
                            C3_symbol_price_base = 0 - r[
                                'V3_ask_one_price_base']
                            C3_symbol_size = r['V3_ask_one_size']
                        symbol_size = min(C1_symbol_size, C2_symbol_size,
                                          C3_symbol_size)
                        r['gain_base'] = (
                            C1_symbol_price_base + C2_symbol_price_base +
                            C3_symbol_price_base - abs(C1_symbol_price_base) *
                            V1_fee - abs(C2_symbol_price_base) * V2_fee -
                            abs(C3_symbol_price_base) * V3_fee) * symbol_size
                        r['gain_ratio'] = (
                            C1_symbol_price_base + C2_symbol_price_base +
                            C3_symbol_price_base - abs(C1_symbol_price_base) *
                            V1_fee - abs(C2_symbol_price_base) * V2_fee -
                            abs(C3_symbol_price_base) * V3_fee
                        ) / (abs(C1_symbol_price_base) + abs(
                            C2_symbol_price_base) + abs(C3_symbol_price_base))
                        df.append(r)
                    df = pd.DataFrame(df)
                    # 判断是否产生交易信号
                    sig = df[df['gain_ratio'] > 0]
                    if not sig.empty:
                        signal.append({'type': CCAT_TRA_TYPE, 'sig': sig})
            # calc pair type
            if CCAT_PAIR_TYPE in types:
                resPair = db.getViewMarketTickerCurrentPair()

            self._logger.error(signal)
        except DBException as err:
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
