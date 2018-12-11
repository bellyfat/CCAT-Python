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
                    res = db.getViewMarketTickerCurrentDisServer(
                        item[0], item[1])
                    # calc gains with fee
                    for r in res:
                        r['bid_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['bid_server'])
                            & (resInfoSymbol['fSymbol'] == r['fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['tSymbol']
                             )]['fee_taker'].values[0]
                        r['ask_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['ask_server'])
                            & (resInfoSymbol['fSymbol'] == r['fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['tSymbol']
                             )]['fee_taker'].values[0]
                        # calc gain_base
                        r['gain_base'] = r['bid_price_base'] * r[
                            'bid_size'] - r['ask_price_base'] * r[
                                'ask_size'] - r['bid_price_base'] * r[
                                    'bid_size'] * r['bid_fee'] - r[
                                        'ask_price_base'] * r['ask_size'] * r[
                                            'ask_fee']
                        # calc gain_ratio
                        r['gain_ratio'] = (r['bid_price'] - r['ask_price'] -
                                           r['bid_price'] * r['bid_fee'] -
                                           r['ask_price'] * r['ask_fee']) / (
                                               r['bid_price'] + r['ask_price'])
                        # calc signal
                        if r['gain_ratio'] > CCAT_DIS_TYPE_THRESHOLD:
                            signal.append({'type': CCAT_DIS_TYPE, 'sig': r})

            # calc tra type
            if CCAT_TRA_TYPE in types:
                res = db.getViewMarketTickerCurrentTraServer(exchanges)
                # calc gains with fee
                for r in res:
                    r['V1_fee'] = resInfoSymbol[
                        (resInfoSymbol['server'] == r['server'])
                        & (resInfoSymbol['fSymbol'] == r['V1_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                         )]['fee_taker'].values[0]
                    r['V2_fee'] = resInfoSymbol[
                        (resInfoSymbol['server'] == r['server'])
                        & (resInfoSymbol['fSymbol'] == r['V2_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                         )]['fee_taker'].values[0]
                    r['V3_fee'] = resInfoSymbol[
                        (resInfoSymbol['server'] == r['server'])
                        & (resInfoSymbol['fSymbol'] == r['V3_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                         )]['fee_taker'].values[0]
                    # calc common symbol
                    r['C1_symbol'] = [
                        i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                        if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                    ][0]
                    r['C2_symbol'] = [
                        i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                        if i in [r['V2_fSymbol'], r['V2_tSymbol']]
                    ][0]
                    r['C3_symbol'] = [
                        i for i in [r['V2_fSymbol'], r['V2_tSymbol']]
                        if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                    ][0]
                    # calc V1
                    if r['C1_symbol'] == r['V1_fSymbol']:  # fSymbol -> tSymbol
                        r['V1_one_price'] = r['V1_bid_one_price']
                        r['V1_one_price_base'] = r['V1_bid_one_price_base']
                        r['V1_one_size'] = r['V1_bid_one_size']
                    else:  # tSymbol -> fSymbol
                        r['V1_one_price'] = r['V1_ask_one_price']
                        r['V1_one_price_base'] = r['V1_ask_one_price_base']
                        r['V1_one_size'] = r['V1_ask_one_size']
                    # calc V2
                    if r['C2_symbol'] == r['V2_fSymbol']:  # fSymbol -> tSymbol
                        r['V2_one_price'] = r['V2_bid_one_price']
                        r['V2_one_price_base'] = r['V2_bid_one_price_base']
                        r['V2_one_size'] = r['V2_bid_one_size']
                    else:  # tSymbol -> fSymbol
                        r['V2_one_price'] = r['V2_ask_one_price']
                        r['V2_one_price_base'] = r['V2_ask_one_price_base']
                        r['V2_one_size'] = r['V2_ask_one_size']
                    # calc V3
                    if r['C3_symbol'] == r['V3_fSymbol']:  # fSymbol -> tSymbol
                        r['V3_one_price'] = r['V3_bid_one_price']
                        r['V3_one_price_base'] = r['V3_bid_one_price_base']
                        r['V3_one_size'] = r['V3_bid_one_size']
                    else:  # tSymbol -> fSymbol
                        r['V3_one_price'] = r['V3_ask_one_price']
                        r['V3_one_price_base'] = r['V3_ask_one_price_base']
                        r['V3_one_size'] = r['V3_ask_one_size']
                    # calc symbol size
                    r['V1_one_size'] = min(
                        r['V1_one_price_base'] * r['V1_one_size'],
                        r['V2_one_price_base'] * r['V2_one_size'],
                        r['V3_one_price_base'] *
                        r['V3_one_size']) / r['V1_one_price_base']
                    r['V2_one_size'] = min(
                        r['V1_one_price_base'] * r['V1_one_size'],
                        r['V2_one_price_base'] * r['V2_one_size'],
                        r['V3_one_price_base'] *
                        r['V3_one_size']) / r['V2_one_price_base']
                    r['V3_one_size'] = min(
                        r['V1_one_price_base'] * r['V1_one_size'],
                        r['V2_one_price_base'] * r['V2_one_size'],
                        r['V3_one_price_base'] *
                        r['V3_one_size']) / r['V3_one_price_base']
                    # calc symbol price
                    if r['C3_symbol'] == r['V3_fSymbol']:  # Type clockwise
                        C1_symbol_price = 1 / r['V1_one_price']
                        C2_symbol_price = r['V2_one_price']
                        C3_symbol_price = 1 / r['V3_one_price']
                    else:  # Type anti-clockwise
                        C1_symbol_price = 1 / r['V1_one_price']
                        C2_symbol_price = r['V2_one_price']
                        C3_symbol_price = r['V3_one_price']
                    # calc tra result
                    candy = False
                    # Type I
                    if C2_symbol_price * C3_symbol_price > 1 / C1_symbol_price:  # tra C1_symbol
                        direct_spend = 1 / C1_symbol_price * r['V1_one_size']
                        direct_left = 1 / C1_symbol_price * r[
                            'V1_one_size'] * (1 - r['V1_fee'])
                        tra_spend = C2_symbol_price * C3_symbol_price * r[
                            'V1_one_size']
                        tra_left = C2_symbol_price * C3_symbol_price * r[
                            'V1_one_size'] * (1 - r['V1_fee']) * (
                                1 - r['V2_fee']) * (1 - r['V3_fee'])
                        # calc gain_ratio
                        r['gain_ratio'] = (tra_left - direct_left) / (
                            direct_spend + tra_spend)
                        # calc gain_base
                        r['gain_base'] = (
                            tra_left - direct_left
                        ) / r['V2_one_price'] * r['V2_one_price_base']
                        # calc gain_symbol
                        r['gain_symbol'] = r['C1_symbol']
                        # change candy
                        candy = True
                    # Type II
                    if C1_symbol_price * C3_symbol_price > 1 / C2_symbol_price:  # tra C2_symbol
                        direct_spend = 1 / C2_symbol_price * r['V2_one_size']
                        direct_left = 1 / C2_symbol_price * r[
                            'V2_one_size'] * (1 - r['V2_fee'])
                        tra_spend = C1_symbol_price * C3_symbol_price * r[
                            'V2_one_size']
                        tra_left = C1_symbol_price * C3_symbol_price * r[
                            'V2_one_size'] * (1 - r['V1_fee']) * (
                                1 - r['V2_fee']) * (1 - r['V3_fee'])
                        if not candy:
                            # calc gain_ratio
                            r['gain_ratio'] = (tra_left - direct_left) / (
                                direct_spend + tra_spend)
                            # calc gain_base
                            r['gain_base'] = (
                                tra_left - direct_left
                            ) / r['V3_one_price'] * r['V3_one_price_base']
                            # calc gain_symbol
                            r['gain_symbol'] = r['C2_symbol']
                        else:
                            if (tra_left - direct_left) / (
                                    direct_spend +
                                    tra_spend) > r['gain_ratio']:
                                # calc gain_ratio
                                r['gain_ratio'] = (tra_left - direct_left) / (
                                    direct_spend + tra_spend)
                                # calc gain_base
                                r['gain_base'] = (
                                    tra_left - direct_left
                                ) / r['V3_one_price'] * r['V3_one_price_base']
                                # calc gain_symbol
                                r['gain_symbol'] = r['C2_symbol']
                        # change candy
                        candy = True
                    # Type III
                    if C1_symbol_price * C2_symbol_price > 1 / C3_symbol_price:  # tra C3_symbol
                        direct_spend = 1 / C3_symbol_price * r['V3_one_size']
                        direct_left = 1 / C3_symbol_price * r[
                            'V3_one_size'] * (1 - r['V3_fee'])
                        tra_spend = C1_symbol_price * C2_symbol_price * r[
                            'V3_one_size']
                        tra_left = C1_symbol_price * C2_symbol_price * r[
                            'V3_one_size'] * (1 - r['V1_fee']) * (
                                1 - r['V2_fee']) * (1 - r['V3_fee'])
                        if not candy:
                            # calc gain_ratio
                            r['gain_ratio'] = (tra_left - direct_left) / (
                                direct_spend + tra_spend)
                            # calc gain_base
                            r['gain_base'] = (
                                tra_left - direct_left
                            ) / r['V1_one_price'] * r['V1_one_price_base']
                            # calc gain_symbol
                            r['gain_symbol'] = r['C3_symbol']
                        else:
                            if (tra_left - direct_left) / (
                                    direct_spend +
                                    tra_spend) > r['gain_ratio']:
                                # calc gain_ratio
                                r['gain_ratio'] = (tra_left - direct_left) / (
                                    direct_spend + tra_spend)
                                # calc gain_base
                                r['gain_base'] = (
                                    tra_left - direct_left
                                ) / r['V1_one_price'] * r['V1_one_price_base']
                                # calc gain_symbol
                                r['gain_symbol'] = r['C3_symbol']
                        # change candy
                        candy = True
                    # calc signal
                    if candy:
                        if r['gain_ratio'] > CCAT_TRA_TYPE_THRESHOLD:
                            signal.append({'type': CCAT_TRA_TYPE, 'sig': r})

            # calc pair type
            if CCAT_PAIR_TYPE in types:
                for item in combinations(exchanges, 2):
                    res = db.getViewMarketTickerCurrentPairServer(
                        item[0], item[1])
                    # calc gains with fee
                    for r in res:
                        r['J1_V1_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['J1_server'])
                            & (resInfoSymbol['fSymbol'] == r['V1_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                             )]['fee_taker'].values[0]
                        r['J1_V2_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['J1_server'])
                            & (resInfoSymbol['fSymbol'] == r['V2_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                             )]['fee_taker'].values[0]
                        r['J1_V3_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['J1_server'])
                            & (resInfoSymbol['fSymbol'] == r['V3_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                             )]['fee_taker'].values[0]
                        r['J2_V1_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['J2_server'])
                            & (resInfoSymbol['fSymbol'] == r['V1_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                             )]['fee_taker'].values[0]
                        r['J2_V2_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['J2_server'])
                            & (resInfoSymbol['fSymbol'] == r['V2_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                             )]['fee_taker'].values[0]
                        r['J2_V3_fee'] = resInfoSymbol[
                            (resInfoSymbol['server'] == r['J2_server'])
                            & (resInfoSymbol['fSymbol'] == r['V3_fSymbol']) &
                            (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                             )]['fee_taker'].values[0]
                        # calc common symbol
                        r['C1_symbol'] = [
                            i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                            if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                        ][0]
                        r['C2_symbol'] = [
                            i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                            if i in [r['V2_fSymbol'], r['V2_tSymbol']]
                        ][0]
                        r['C3_symbol'] = [
                            i for i in [r['V2_fSymbol'], r['V2_tSymbol']]
                            if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                        ][0]
                        # calc J1_V1, J2_V1
                        if r['C1_symbol'] == r[
                                'V1_fSymbol']:  # fSymbol -> tSymbol
                            r['J1_V1_one_price'] = r['J1_V1_bid_one_price']
                            r['J1_V1_one_price_base'] = r[
                                'J1_V1_bid_one_price_base']
                            r['J1_V1_one_size'] = min(r['J1_V1_bid_one_size'],
                                                      r['J2_V1_ask_one_size'])
                            r['J2_V1_one_price'] = r['J2_V1_ask_one_price']
                            r['J2_V1_one_price_base'] = r[
                                'J2_V1_ask_one_price_base']
                            r['J2_V1_one_size'] = min(r['J1_V1_bid_one_size'],
                                                      r['J2_V1_ask_one_size'])
                        else:  # tSymbol -> fSymbol
                            r['J1_V1_one_price'] = r['J1_V1_ask_one_price']
                            r['J1_V1_one_price_base'] = r[
                                'J1_V1_ask_one_price_base']
                            r['J1_V1_one_size'] = min(r['J1_V1_ask_one_size'],
                                                      r['J2_V1_bid_one_size'])
                            r['J2_V1_one_price'] = r['J2_V1_bid_one_price']
                            r['J2_V1_one_price_base'] = r[
                                'J2_V1_bid_one_price_base']
                            r['J2_V1_one_size'] = min(r['J1_V1_ask_one_size'],
                                                      r['J2_V1_bid_one_size'])
                        # calc J1_V2, J2_V2
                        if r['C2_symbol'] == r[
                                'V2_fSymbol']:  # fSymbol -> tSymbol
                            r['J1_V2_one_price'] = r['J1_V2_bid_one_price']
                            r['J1_V2_one_price_base'] = r[
                                'J1_V2_bid_one_price_base']
                            r['J1_V2_one_size'] = min(r['J1_V2_bid_one_size'],
                                                      r['J2_V2_ask_one_size'])
                            r['J2_V2_one_price'] = r['J2_V2_ask_one_price']
                            r['J2_V2_one_price_base'] = r[
                                'J2_V2_ask_one_price_base']
                            r['J2_V2_one_size'] = min(r['J1_V2_bid_one_size'],
                                                      r['J2_V2_ask_one_size'])
                        else:  # tSymbol -> fSymbol
                            r['J1_V2_one_price'] = r['J1_V2_ask_one_price']
                            r['J1_V2_one_price_base'] = r[
                                'J1_V2_ask_one_price_base']
                            r['J1_V2_one_size'] = min(r['J1_V2_ask_one_size'],
                                                      r['J2_V2_bid_one_size'])
                            r['J2_V2_one_price'] = r['J2_V2_bid_one_price']
                            r['J2_V2_one_price_base'] = r[
                                'J2_V2_bid_one_price_base']
                            r['J2_V2_one_size'] = min(r['J1_V2_ask_one_size'],
                                                      r['J2_V2_bid_one_size'])
                        # calc J1_V3, J2_V3
                        if r['C3_symbol'] == r[
                                'V3_fSymbol']:  # fSymbol -> tSymbol
                            r['J1_V3_one_price'] = r['J1_V3_bid_one_price']
                            r['J1_V3_one_price_base'] = r[
                                'J1_V3_bid_one_price_base']
                            r['J1_V3_one_size'] = min(r['J1_V3_bid_one_size'],
                                                      r['J2_V3_ask_one_size'])
                            r['J2_V3_one_price'] = r['J2_V3_ask_one_price']
                            r['J2_V3_one_price_base'] = r[
                                'J2_V3_ask_one_price_base']
                            r['J2_V3_one_size'] = min(r['J1_V3_bid_one_size'],
                                                      r['J2_V3_ask_one_size'])
                        else:  # tSymbol -> fSymbol
                            r['J1_V3_one_price'] = r['J1_V3_ask_one_price']
                            r['J1_V3_one_price_base'] = r[
                                'J1_V3_ask_one_price_base']
                            r['J1_V3_one_size'] = min(r['J1_V3_ask_one_size'],
                                                      r['J2_V3_bid_one_size'])
                            r['J2_V3_one_price'] = r['J2_V3_bid_one_price']
                            r['J2_V3_one_price_base'] = r[
                                'J2_V3_bid_one_price_base']
                            r['J2_V3_one_size'] = min(r['J1_V3_ask_one_size'],
                                                      r['J2_V3_bid_one_size'])
                        # calc symbol size
                        r['J1_V1_one_size'] = min(
                            r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                            r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                            r['J1_V3_one_price_base'] *
                            r['J1_V3_one_size']) / r['J1_V1_one_price_base']
                        r['J1_V2_one_size'] = min(
                            r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                            r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                            r['J1_V3_one_price_base'] *
                            r['J1_V3_one_size']) / r['J1_V2_one_price_base']
                        r['J1_V3_one_size'] = min(
                            r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                            r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                            r['J1_V3_one_price_base'] *
                            r['J1_V3_one_size']) / r['J1_V3_one_price_base']
                        r['J2_V1_one_size'] = min(
                            r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                            r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                            r['J2_V3_one_price_base'] *
                            r['J2_V3_one_size']) / r['J2_V1_one_price_base']
                        r['J2_V2_one_size'] = min(
                            r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                            r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                            r['J2_V3_one_price_base'] *
                            r['J2_V3_one_size']) / r['J2_V2_one_price_base']
                        r['J2_V3_one_size'] = min(
                            r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                            r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                            r['J2_V3_one_price_base'] *
                            r['J2_V3_one_size']) / r['J2_V3_one_price_base']
                        r['J1_V1_one_size'] = min(r['J1_V1_one_size'],
                                                  r['J2_V1_one_size'])
                        r['J1_V2_one_size'] = min(r['J1_V2_one_size'],
                                                  r['J2_V2_one_size'])
                        r['J1_V3_one_size'] = min(r['J1_V3_one_size'],
                                                  r['J2_V3_one_size'])
                        r['J2_V1_one_size'] = min(r['J1_V1_one_size'],
                                                  r['J2_V1_one_size'])
                        r['J2_V2_one_size'] = min(r['J1_V2_one_size'],
                                                  r['J2_V2_one_size'])
                        r['J2_V3_one_size'] = min(r['J1_V3_one_size'],
                                                  r['J2_V3_one_size'])
                        # calc gain_base
                        C1_symbol_gain_base = r['J1_V1_one_price_base'] * r[
                            'J1_V1_one_size'] - r['J2_V1_one_price_base'] * r[
                                'J2_V1_one_size'] - r[
                                    'J1_V1_one_price_base'] * r[
                                        'J1_V1_one_size'] * r['J1_V1_fee'] - r[
                                            'J2_V1_one_price_base'] * r[
                                                'J2_V1_one_size'] * r[
                                                    'J2_V1_fee']
                        C2_symbol_gain_base = r['J1_V2_one_price_base'] * r[
                            'J1_V2_one_size'] - r['J2_V2_one_price_base'] * r[
                                'J2_V2_one_size'] - r[
                                    'J1_V2_one_price_base'] * r[
                                        'J1_V2_one_size'] * r['J1_V2_fee'] - r[
                                            'J2_V2_one_price_base'] * r[
                                                'J2_V2_one_size'] * r[
                                                    'J2_V2_fee']
                        C3_symbol_gain_base = r['J1_V3_one_price_base'] * r[
                            'J1_V3_one_size'] - r['J2_V3_one_price_base'] * r[
                                'J2_V3_one_size'] - r[
                                    'J1_V3_one_price_base'] * r[
                                        'J1_V3_one_size'] * r['J1_V3_fee'] - r[
                                            'J2_V3_one_price_base'] * r[
                                                'J2_V3_one_size'] * r[
                                                    'J2_V3_fee']
                        r['gain_base'] = C1_symbol_gain_base + C2_symbol_gain_base + C3_symbol_gain_base
                        # calc gain_ratio
                        C1_symbol_gain_ratio = (
                            r['J1_V1_one_price'] - r['J2_V1_one_price'] -
                            r['J1_V1_one_price'] * r['J1_V1_fee'] -
                            r['J2_V1_one_price'] * r['J2_V1_fee']) / (
                                r['J1_V1_one_price'] + r['J2_V1_one_price'])
                        C2_symbol_gain_ratio = (
                            r['J1_V2_one_price'] - r['J2_V2_one_price'] -
                            r['J1_V2_one_price'] * r['J1_V2_fee'] -
                            r['J2_V2_one_price'] * r['J2_V2_fee']) / (
                                r['J1_V2_one_price'] + r['J2_V2_one_price'])
                        C3_symbol_gain_ratio = (
                            r['J1_V3_one_price'] - r['J2_V3_one_price'] -
                            r['J1_V3_one_price'] * r['J1_V3_fee'] -
                            r['J2_V3_one_price'] * r['J2_V3_fee']) / (
                                r['J1_V3_one_price'] + r['J2_V3_one_price'])
                        r['gain_ratio'] = C1_symbol_gain_ratio + C2_symbol_gain_ratio + C3_symbol_gain_ratio
                        # calc signal
                        if r['gain_ratio'] > CCAT_PAIR_TYPE_THRESHOLD:
                            signal.append({'type': CCAT_PAIR_TYPE, 'sig': r})
            infoStr = "src.core.engine.handler.Handler.handleJudgeMarketTickerEvent: { signal = %s }" % signal
            self._logger.info(infoStr)
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
