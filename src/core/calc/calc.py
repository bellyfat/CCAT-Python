# -*- coding: utf-8 -*-

from itertools import combinations

import pandas as pd
from src.core.coin.enums import CCAT_ORDER_SIDE_BUY, CCAT_ORDER_SIDE_SELL
from src.core.db.db import DB
from src.core.util.exceptions import CalcException, DBException
from src.core.util.helper import utcnow_timestamp
from src.core.util.log import Logger


class Calc(object):
    def __init__(self):
        # logger
        self._logger = Logger()

    def calcStatisticSignalTickerDis(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticSignalTickerDis: {exchange=%s, timeWindow=%s}"
            % (exchange, timeWindow))
        try:
            statistic = []
            db = DB()
            # statistic dis type
            for server, server_pair in combinations(exchange, 2):
                signal = db.getViewJudgeSignalTickerDisCurrentServer(
                    server, server_pair)
                if not signal == []:
                    df = pd.DataFrame(signal)
                    for (fSymbol,
                         tSymbol), group in df.groupby(['fSymbol', 'tSymbol']):
                        # calc timeStamp
                        period = []
                        periodTime = 0
                        lastTime = group['timeStamp'].min()
                        for index, value in group['timeStamp'].sort_values(
                        ).items():
                            if value - lastTime < timeWindow:
                                periodTime = periodTime + (value - lastTime)
                            else:
                                period.append(periodTime)
                                periodTime = 0
                            lastTime = value
                        period.append(periodTime)
                        # calc sta
                        sta = {
                            "timeStamp":
                            utcnow_timestamp(),
                            "bid_server":
                            server,
                            "ask_server":
                            server_pair,
                            "fSymbol":
                            fSymbol,
                            "tSymbol":
                            tSymbol,
                            "timeStamp_start":
                            group['timeStamp'].min(),
                            "timeStamp_end":
                            group['timeStamp'].max(),
                            "timeStamp_times":
                            len(period),
                            "timeStamp_period_times":
                            sum([p > 0 for p in period]),
                            "timeStamp_period_longest":
                            max(period),
                            "count_total":
                            group.shape[0],
                            "count_forward":
                            group[(group['bid_server'] == server)].shape[0],
                            "count_backward":
                            group[(
                                group['bid_server'] == server_pair)].shape[0],
                            "gain_base_max":
                            group['gain_base'].max(),
                            "gain_base_min":
                            group['gain_base'].min(),
                            "gain_base_mean":
                            group['gain_base'].mean(),
                            "gain_base_std":
                            group['gain_base'].std(),
                            "gain_ratio_max":
                            group['gain_ratio'].max(),
                            "gain_ratio_min":
                            group['gain_ratio'].min(),
                            "gain_ratio_mean":
                            group['gain_ratio'].mean(),
                            "gain_ratio_std":
                            group['gain_ratio'].std()
                        }
                        # update statistic
                        statistic.append(sta)
            return statistic
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcStatisticSignalTickerTra(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticSignalTickerTra: {exchange=%s, timeWindow=%s}"
            % (exchange, timeWindow))
        try:
            statistic = []
            db = DB()
            # statistic dis type
            signal = db.getViewJudgeSignalTickerTraCurrentServer(exchange)
            if not signal == []:
                df = []
                # calc sort df
                for s in signal:
                    symbol_pair = [
                        s['C1_symbol'], s['C2_symbol'], s['C3_symbol']
                    ]
                    symbol_pair.sort()
                    s['symbol_pair'] = ', '.join(symbol_pair)
                    df.append(s)
                df = pd.DataFrame(signal)
                # calc
                for (server, symbol_pair), group in df.groupby(
                    ['server', 'symbol_pair']):
                    # calc timeStamp
                    period = []
                    periodTime = 0
                    lastTime = group['timeStamp'].min()
                    for index, value in group['timeStamp'].sort_values().items(
                    ):
                        if value - lastTime < timeWindow:
                            periodTime = periodTime + (value - lastTime)
                        else:
                            period.append(periodTime)
                            periodTime = 0
                        lastTime = value
                    period.append(periodTime)
                    # calc sta
                    sta = {
                        "timeStamp":
                        utcnow_timestamp(),
                        "server":
                        server,
                        "symbol_pair":
                        symbol_pair,
                        "timeStamp_start":
                        group['timeStamp'].min(),
                        "timeStamp_end":
                        group['timeStamp'].max(),
                        "timeStamp_times":
                        len(period),
                        "timeStamp_period_times":
                        sum([p > 0 for p in period]),
                        "timeStamp_period_longest":
                        max(period),
                        "count_total":
                        group.shape[0],
                        "count_forward":
                        group[(group['C3_symbol'] == group['V3_fSymbol'])].shape[0],
                        "count_backward":
                        group[(group['C3_symbol'] == group['V3_tSymbol'])].shape[0],
                        "gain_base_max":
                        group['gain_base'].max(),
                        "gain_base_min":
                        group['gain_base'].min(),
                        "gain_base_mean":
                        group['gain_base'].mean(),
                        "gain_base_std":
                        group['gain_base'].std(),
                        "gain_ratio_max":
                        group['gain_ratio'].max(),
                        "gain_ratio_min":
                        group['gain_ratio'].min(),
                        "gain_ratio_mean":
                        group['gain_ratio'].mean(),
                        "gain_ratio_std":
                        group['gain_ratio'].std()
                    }
                    # update statistic
                    statistic.append(sta)
            return statistic
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcStatisticSignalTickerPair(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticSignalTickerPair: {exchange=%s}"
            % exchange)
        try:
            statistic = []
            db = DB()
            # statistic dis type
            for server, server_pair in combinations(exchange, 2):
                signal = db.getViewJudgeSignalTickerPairCurrentServer(
                    server, server_pair)
                if not signal == []:
                    df = []
                    # calc sort df
                    for s in signal:
                        symbol_pair = [
                            s['C1_symbol'], s['C2_symbol'], s['C3_symbol']
                        ]
                        symbol_pair.sort()
                        s['symbol_pair'] = ', '.join(symbol_pair)
                        df.append(s)
                    df = pd.DataFrame(signal)
                    # calc
                    for symbol_pair, group in df.groupby(
                        ['symbol_pair']):
                        # calc timeStamp
                        period = []
                        periodTime = 0
                        lastTime = group['timeStamp'].min()
                        for index, value in group['timeStamp'].sort_values().items(
                        ):
                            if value - lastTime < timeWindow:
                                periodTime = periodTime + (value - lastTime)
                            else:
                                period.append(periodTime)
                                periodTime = 0
                            lastTime = value
                        period.append(periodTime)
                        # calc sta
                        sta = {
                            "timeStamp":
                            utcnow_timestamp(),
                            "J1_server":
                            server,
                            "J2_server":
                            server_pair,
                            "symbol_pair":
                            symbol_pair,
                            "timeStamp_start":
                            group['timeStamp'].min(),
                            "timeStamp_end":
                            group['timeStamp'].max(),
                            "timeStamp_times":
                            len(period),
                            "timeStamp_period_times":
                            sum([p > 0 for p in period]),
                            "timeStamp_period_longest":
                            max(period),
                            "count_total":
                            group.shape[0],
                            "count_forward":
                            group[(group['C3_symbol'] == group['V3_fSymbol'])].shape[0],
                            "count_backward":
                            group[(group['C3_symbol'] == group['V3_tSymbol'])].shape[0],
                            "gain_base_max":
                            group['gain_base'].max(),
                            "gain_base_min":
                            group['gain_base'].min(),
                            "gain_base_mean":
                            group['gain_base'].mean(),
                            "gain_base_std":
                            group['gain_base'].std(),
                            "gain_ratio_max":
                            group['gain_ratio'].max(),
                            "gain_ratio_min":
                            group['gain_ratio'].min(),
                            "gain_ratio_mean":
                            group['gain_ratio'].mean(),
                            "gain_ratio_std":
                            group['gain_ratio'].std()
                        }
                        # update statistic
                        statistic.append(sta)
                return statistic
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcJudgeSignalTickerDis(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeSignalTickerDis: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            signal = []
            # calc dis type
            for server, server_pair in combinations(exchange, 2):
                res = db.getViewMarketTickerCurrentDisServer(
                    server, server_pair)
                # calc gains with fee
                for r in res:
                    if not r['bid_price'] > r['ask_price']:
                        continue
                    # calc fees
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
                    if r['bid_fee'] == 'NULL':
                        r['bid_fee'] = 0
                    if r['ask_fee'] == 'NULL':
                        r['ask_fee'] = 0
                    # calc size
                    r['bid_size'] = min(r['bid_size'], r['ask_size'])
                    r['ask_size'] = min(r['bid_size'], r['ask_size'])
                    # calc base price
                    tSymbol_base_price = (
                        r['bid_price_base'] / r['bid_price'] +
                        r['ask_price_base'] / r['ask_price']) / 2
                    # calc gain_base
                    r['gain_base'] = (
                        r['bid_price'] * r['bid_size'] -
                        r['ask_price'] * r['ask_size'] - r['bid_price'] *
                        r['bid_size'] * r['bid_fee'] - r['ask_price'] *
                        r['ask_size'] * r['ask_fee']) * tSymbol_base_price
                    # calc gain_ratio
                    r['gain_ratio'] = (
                        r['bid_price'] - r['ask_price'] -
                        r['bid_price'] * r['bid_fee'] -
                        r['ask_price'] * r['ask_fee']) / r['ask_price']
                    # calc signal
                    if r['gain_ratio'] > threshold:
                        signal.append(r)
            # return signal
            return signal
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcJudgeSignalTickerTra(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeSignalTickerTra: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            signal = []
            # calc tra type
            res = db.getViewMarketTickerCurrentTraServer(exchange)
            # calc gains with fee
            for r in res:
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
                    r['V1_one_side'] = CCAT_ORDER_SIDE_SELL
                    r['V1_one_size'] = r['V1_bid_one_size']
                else:  # tSymbol -> fSymbol
                    r['V1_one_price'] = r['V1_ask_one_price']
                    r['V1_one_side'] = CCAT_ORDER_SIDE_BUY
                    r['V1_one_size'] = r['V1_ask_one_size']
                # calc V2
                if r['C2_symbol'] == r['V2_fSymbol']:  # fSymbol -> tSymbol
                    r['V2_one_price'] = r['V2_bid_one_price']
                    r['V2_one_side'] = CCAT_ORDER_SIDE_SELL
                    r['V2_one_size'] = r['V2_bid_one_size']
                else:  # tSymbol -> fSymbol
                    r['V2_one_price'] = r['V2_ask_one_price']
                    r['V2_one_side'] = CCAT_ORDER_SIDE_BUY
                    r['V2_one_size'] = r['V2_ask_one_size']
                # calc V3
                if r['C3_symbol'] == r['V3_fSymbol']:  # fSymbol -> tSymbol
                    r['V3_one_price'] = r['V3_bid_one_price']
                    r['V3_one_side'] = CCAT_ORDER_SIDE_SELL
                    r['V3_one_size'] = r['V3_bid_one_size']
                else:  # tSymbol -> fSymbol
                    r['V3_one_price'] = r['V3_ask_one_price']
                    r['V3_one_side'] = CCAT_ORDER_SIDE_BUY
                    r['V3_one_size'] = r['V3_ask_one_size']
                # calc symbol one price ratio
                if r['C3_symbol'] == r['V3_fSymbol']:
                    # Type clockwise
                    C1_C2_one_price = r['V1_one_price']
                    C2_C3_one_price = 1 / r['V2_one_price']
                    C3_C1_one_price = r['V3_one_price']
                else:
                    # Type anti-clockwise
                    C1_C2_one_price = r['V1_one_price']
                    C2_C3_one_price = 1 / r['V2_one_price']
                    C3_C1_one_price = 1 / r['V3_one_price']
                # calc tra result
                if not C1_C2_one_price * C2_C3_one_price * C3_C1_one_price > 1:
                    continue
                # calc fees
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
                if r['V1_fee'] == 'NULL':
                    r['V1_fee'] = 0
                if r['V2_fee'] == 'NULL':
                    r['V2_fee'] = 0
                if r['V3_fee'] == 'NULL':
                    r['V3_fee'] = 0
                # calc symbol base
                V1_tSymbol_base_price = (
                    r['V1_bid_one_price_base'] / r['V1_bid_one_price'] +
                    r['V1_ask_one_price_base'] / r['V1_ask_one_price']) / 2
                V2_tSymbol_base_price = (
                    r['V2_bid_one_price_base'] / r['V2_bid_one_price'] +
                    r['V2_ask_one_price_base'] / r['V2_ask_one_price']) / 2
                V3_tSymbol_base_price = (
                    r['V3_bid_one_price_base'] / r['V3_bid_one_price'] +
                    r['V3_ask_one_price_base'] / r['V3_ask_one_price']) / 2
                # Begin Calc Gain
                if r['C3_symbol'] == r['V3_fSymbol']:
                    # Type clockwise: sell->buy->sell
                    # calc symbol size
                    temp = min(r['V3_one_size'],
                               r['V1_one_size'] / C3_C1_one_price)
                    temp_size = min(r['V2_one_size'], temp)
                    r['V1_one_size'] = temp_size * C3_C1_one_price
                    r['V2_one_size'] = temp_size
                    r['V3_one_size'] = temp_size
                    # calc gain_base
                    r['gain_base'] = (C1_C2_one_price * C3_C1_one_price *
                                      (1 - r['V1_fee']) *
                                      (1 - r['V3_fee']) - 1 / C2_C3_one_price -
                                      1 / C2_C3_one_price * r['V2_fee']
                                      ) * temp_size * V2_tSymbol_base_price
                    # calc gain_ratio
                    r['gain_ratio'] = (
                        C1_C2_one_price * C3_C1_one_price * (1 - r['V1_fee']) *
                        (1 - r['V3_fee']) - 1 / C2_C3_one_price - 1 /
                        C2_C3_one_price * r['V2_fee']) / (1 / C2_C3_one_price)
                else:
                    # Type anti-clockwise: sell->buy->buy
                    # calc symbol size
                    temp = min(r['V2_one_size'],
                               r['V3_one_size'] / C2_C3_one_price)
                    temp_size = min(r['V1_one_size'], temp)
                    r['V1_one_size'] = temp_size
                    r['V2_one_size'] = temp_size
                    r['V3_one_size'] = temp_size * C2_C3_one_price
                    # calc gain_base
                    r['gain_base'] = (
                        C1_C2_one_price * (1 - r['V1_fee']) -
                        (1 / (C2_C3_one_price * C3_C1_one_price)) -
                        (1 / (C2_C3_one_price * C3_C1_one_price)) *
                        (r['V2_fee'] + r['V3_fee'] - r['V2_fee'] * r['V3_fee'])
                    ) * temp_size * V1_tSymbol_base_price
                    # calc gain_ratio
                    r['gain_ratio'] = (
                        C1_C2_one_price * (1 - r['V1_fee']) -
                        (1 / (C2_C3_one_price * C3_C1_one_price)) -
                        (1 / (C2_C3_one_price * C3_C1_one_price)) *
                        (r['V2_fee'] + r['V3_fee'] - r['V2_fee'] * r['V3_fee'])
                    ) / (1 / (C2_C3_one_price * C3_C1_one_price))
                # calc signal
                if r['gain_ratio'] > threshold:
                    signal.append(r)
            # return signal
            return signal
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcJudgeSignalTickerPair(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeSignalTickerPair: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, resInfoSymbol))
        try:
            db = DB()
            signal = []
            # calc pair type
            for server, server_pair in combinations(exchange, 2):
                res = db.getViewMarketTickerCurrentPairServer(
                    server, server_pair)
                # calc gains with fee
                for r in res:
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
                    if r['C1_symbol'] == r['V1_fSymbol']:  # fSymbol -> tSymbol
                        r['J1_V1_one_price'] = r['J1_V1_bid_one_price']
                        r['J1_V1_one_side'] = CCAT_ORDER_SIDE_SELL
                        r['J1_V1_one_size'] = r['J1_V1_bid_one_size']
                        r['J2_V1_one_price'] = r['J2_V1_ask_one_price']
                        r['J2_V1_one_side'] = CCAT_ORDER_SIDE_BUY
                        r['J2_V1_one_size'] = r['J2_V1_ask_one_size']
                    else:  # tSymbol -> fSymbol
                        r['J1_V1_one_price'] = r['J1_V1_ask_one_price']
                        r['J1_V1_one_side'] = CCAT_ORDER_SIDE_BUY
                        r['J1_V1_one_size'] = r['J1_V1_ask_one_size']
                        r['J2_V1_one_price'] = r['J2_V1_bid_one_price']
                        r['J2_V1_one_side'] = CCAT_ORDER_SIDE_SELL
                        r['J2_V1_one_size'] = r['J2_V1_bid_one_size']
                    # calc J1_V2, J2_V2
                    if r['C2_symbol'] == r['V2_fSymbol']:  # fSymbol -> tSymbol
                        r['J1_V2_one_price'] = r['J1_V2_bid_one_price']
                        r['J1_V2_one_side'] = CCAT_ORDER_SIDE_SELL
                        r['J1_V2_one_size'] = r['J1_V2_bid_one_size']
                        r['J2_V2_one_price'] = r['J2_V2_ask_one_price']
                        r['J2_V2_one_side'] = CCAT_ORDER_SIDE_BUY
                        r['J2_V2_one_size'] = r['J2_V2_ask_one_size']
                    else:  # tSymbol -> fSymbol
                        r['J1_V2_one_price'] = r['J1_V2_ask_one_price']
                        r['J1_V2_one_side'] = CCAT_ORDER_SIDE_BUY
                        r['J1_V2_one_size'] = r['J1_V2_ask_one_size']
                        r['J2_V2_one_price'] = r['J2_V2_bid_one_price']
                        r['J2_V2_one_side'] = CCAT_ORDER_SIDE_SELL
                        r['J2_V2_one_size'] = r['J2_V2_bid_one_size']
                    # calc J1_V3, J2_V3
                    if r['C3_symbol'] == r['V3_fSymbol']:  # fSymbol -> tSymbol
                        r['J1_V3_one_price'] = r['J1_V3_bid_one_price']
                        r['J1_V3_one_side'] = CCAT_ORDER_SIDE_SELL
                        r['J1_V3_one_size'] = r['J1_V3_bid_one_size']
                        r['J2_V3_one_price'] = r['J2_V3_ask_one_price']
                        r['J2_V3_one_side'] = CCAT_ORDER_SIDE_BUY
                        r['J2_V3_one_size'] = r['J2_V3_ask_one_size']
                    else:  # tSymbol -> fSymbol
                        r['J1_V3_one_price'] = r['J1_V3_ask_one_price']
                        r['J1_V3_one_side'] = CCAT_ORDER_SIDE_BUY
                        r['J1_V3_one_size'] = r['J1_V3_ask_one_size']
                        r['J2_V3_one_price'] = r['J2_V3_bid_one_price']
                        r['J2_V3_one_side'] = CCAT_ORDER_SIDE_SELL
                        r['J2_V3_one_size'] = r['J2_V3_bid_one_size']
                    # calc symbol one price ratio
                    if r['C3_symbol'] == r['V3_fSymbol']:
                        # Type J1 = clockwise, J2 = anti-clockwise
                        # calc J1
                        J1_C1_C2_one_price = r['J1_V1_one_price']
                        J1_C2_C3_one_price = 1 / r['J1_V2_one_price']
                        J1_C3_C1_one_price = r['J1_V3_one_price']
                        # calc J2
                        J2_C1_C2_one_price = r['J2_V1_one_price']
                        J2_C2_C3_one_price = 1 / r['J2_V2_one_price']
                        J2_C3_C1_one_price = 1 / r['J2_V3_one_price']
                    else:
                        # Type J1 = anti-clockwise, J2 = clockwise
                        # calc J1
                        J1_C1_C2_one_price = r['J1_V1_one_price']
                        J1_C2_C3_one_price = 1 / r['J1_V2_one_price']
                        J1_C3_C1_one_price = 1 / r['J1_V3_one_price']
                        # calc J2
                        J2_C1_C2_one_price = r['J2_V1_one_price']
                        J2_C2_C3_one_price = 1 / r['J2_V2_one_price']
                        J2_C3_C1_one_price = r['J2_V3_one_price']
                    # calc tra result
                    if not J1_C1_C2_one_price * J1_C2_C3_one_price * J1_C3_C1_one_price > J2_C1_C2_one_price * J2_C2_C3_one_price * J2_C3_C1_one_price:
                        continue
                    # calc fees
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
                    if r['J1_V1_fee'] == 'NULL':
                        r['J1_V1_fee'] = 0
                    if r['J1_V2_fee'] == 'NULL':
                        r['J1_V2_fee'] = 0
                    if r['J1_V3_fee'] == 'NULL':
                        r['J1_V3_fee'] = 0
                    if r['J2_V1_fee'] == 'NULL':
                        r['J2_V1_fee'] = 0
                    if r['J2_V2_fee'] == 'NULL':
                        r['J2_V2_fee'] = 0
                    if r['J2_V3_fee'] == 'NULL':
                        r['J2_V3_fee'] = 0
                    # calc symbol size
                    if r['C3_symbol'] == r['V3_fSymbol']:
                        # Type J1 = clockwise: sell->buy->sell, J2 = anti-clockwise: sell->buy->buy
                        # calc J1 symbol size
                        temp = min(r['J1_V3_one_size'],
                                   r['J1_V1_one_size'] / J1_C3_C1_one_price)
                        temp_size = min(r['J1_V2_one_size'], temp)
                        r['J1_V1_one_size'] = temp_size * J1_C3_C1_one_price
                        r['J1_V2_one_size'] = temp_size
                        r['J1_V3_one_size'] = temp_size
                        # calc J2 symbol size
                        temp = min(r['J2_V2_one_size'],
                                   r['J2_V3_one_size'] / J2_C2_C3_one_price)
                        temp_size = min(r['J2_V1_one_size'], temp)
                        r['J2_V1_one_size'] = temp_size
                        r['J2_V2_one_size'] = temp_size
                        r['J2_V3_one_size'] = temp_size * J2_C2_C3_one_price
                    else:
                        # Type J1 = anti-clockwise: sell->buy->buy, J2 = clockwise: sell->buy->sell
                        # calc J1 symbol size
                        temp = min(r['J1_V2_one_size'],
                                   r['J1_V3_one_size'] / J1_C2_C3_one_price)
                        temp_size = min(r['J1_V1_one_size'], temp)
                        r['J1_V1_one_size'] = temp_size
                        r['J1_V2_one_size'] = temp_size
                        r['J1_V3_one_size'] = temp_size * J1_C2_C3_one_price
                        # calc J2 symbol size
                        temp = min(r['J2_V3_one_size'],
                                   r['J2_V1_one_size'] / J2_C3_C1_one_price)
                        temp_size = min(r['J2_V2_one_size'], temp)
                        r['J2_V1_one_size'] = temp_size * J2_C3_C1_one_price
                        r['J2_V2_one_size'] = temp_size
                        r['J2_V3_one_size'] = temp_size
                    # calc symbol size
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
                    # calc base price
                    # calc J1
                    J1_V1_tSymbol_base_price = (r['J1_V1_bid_one_price_base'] /
                                                r['J1_V1_bid_one_price'] +
                                                r['J1_V1_ask_one_price_base'] /
                                                r['J1_V1_ask_one_price']) / 2
                    J1_V2_tSymbol_base_price = (r['J1_V2_bid_one_price_base'] /
                                                r['J1_V2_bid_one_price'] +
                                                r['J1_V2_ask_one_price_base'] /
                                                r['J1_V2_ask_one_price']) / 2
                    J1_V3_tSymbol_base_price = (r['J1_V3_bid_one_price_base'] /
                                                r['J1_V3_bid_one_price'] +
                                                r['J1_V3_ask_one_price_base'] /
                                                r['J1_V3_ask_one_price']) / 2
                    # calc J2
                    J2_V1_tSymbol_base_price = (r['J2_V1_bid_one_price_base'] /
                                                r['J2_V1_bid_one_price'] +
                                                r['J2_V1_ask_one_price_base'] /
                                                r['J2_V1_ask_one_price']) / 2
                    J2_V2_tSymbol_base_price = (r['J2_V2_bid_one_price_base'] /
                                                r['J2_V2_bid_one_price'] +
                                                r['J2_V2_ask_one_price_base'] /
                                                r['J2_V2_ask_one_price']) / 2
                    J2_V3_tSymbol_base_price = (r['J2_V3_bid_one_price_base'] /
                                                r['J2_V3_bid_one_price'] +
                                                r['J2_V3_ask_one_price_base'] /
                                                r['J2_V3_ask_one_price']) / 2
                    tSymbol_base_price = (
                        (J1_V1_tSymbol_base_price + J2_V1_tSymbol_base_price) *
                        (r['J1_V1_one_size'] + r['J2_V1_one_size']) +
                        (J1_V2_tSymbol_base_price + J2_V2_tSymbol_base_price) *
                        (r['J1_V2_one_size'] + r['J2_V2_one_size']) +
                        (J1_V3_tSymbol_base_price + J2_V3_tSymbol_base_price) *
                        (r['J1_V3_one_size'] + r['J2_V3_one_size'])) / (
                            r['J1_V1_one_size'] + r['J2_V1_one_size'] +
                            r['J1_V2_one_size'] + r['J2_V2_one_size'] +
                            r['J1_V3_one_size'] + r['J2_V3_one_size'])
                    # Begin Calc Gain
                    C1_symbol_gain_ratio_up = (
                        r['J1_V1_one_price'] - r['J2_V1_one_price'] -
                        r['J1_V1_one_price'] * r['J1_V1_fee'] -
                        r['J2_V1_one_price'] * r['J2_V1_fee']) * (
                            r['J1_V1_one_size'] + r['J2_V1_one_size']) / 2
                    C1_symbol_gain_ratio_dn = r['J2_V1_one_price'] * (
                        r['J1_V1_one_size'] + r['J2_V1_one_size']) / 2
                    C2_symbol_gain_ratio_up = (
                        r['J1_V2_one_price'] - r['J2_V2_one_price'] -
                        r['J1_V2_one_price'] * r['J1_V2_fee'] -
                        r['J2_V2_one_price'] * r['J2_V2_fee']) * (
                            r['J1_V2_one_size'] + r['J2_V2_one_size']) / 2
                    C2_symbol_gain_ratio_dn = r['J2_V2_one_price'] * (
                        r['J1_V2_one_size'] + r['J2_V2_one_size']) / 2
                    C3_symbol_gain_ratio_up = (
                        r['J1_V3_one_price'] - r['J2_V3_one_price'] -
                        r['J1_V3_one_price'] * r['J1_V3_fee'] -
                        r['J2_V3_one_price'] * r['J2_V3_fee']) * (
                            r['J1_V3_one_size'] + r['J2_V3_one_size']) / 2
                    C3_symbol_gain_ratio_dn = r['J2_V3_one_price'] * (
                        r['J1_V3_one_size'] + r['J2_V3_one_size']) / 2
                    # calc gain_base
                    r['gain_base'] = (
                        C1_symbol_gain_ratio_up + C2_symbol_gain_ratio_up +
                        C3_symbol_gain_ratio_up) * tSymbol_base_price
                    # calc gain_ratio
                    r['gain_ratio'] = (
                        C1_symbol_gain_ratio_up + C2_symbol_gain_ratio_up +
                        C3_symbol_gain_ratio_up) / (
                            C1_symbol_gain_ratio_dn + C2_symbol_gain_ratio_dn +
                            C3_symbol_gain_ratio_dn)
                    # calc signal
                    if r['gain_ratio'] > threshold:
                        signal.append(r)
            # return signal
            return signal
        except (DBException, Exception) as err:
            raise CalcException(err)
