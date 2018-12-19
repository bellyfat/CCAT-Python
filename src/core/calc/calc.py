# -*- coding: utf-8 -*-

from itertools import combinations

import pandas as pd
from src.core.coin.enums import CCAT_ORDER_SIDE_BUY, CCAT_ORDER_SIDE_SELL
from src.core.db.db import DB
from src.core.util.exceptions import CalcException, DBException
from src.core.util.log import Logger


class Calc(object):
    def __init__(self):
        # logger
        self._logger = Logger()

    def statisticSignalTickerDis(self, exchange):
        self._logger.debug(
            "src.core.calc.calc.Calc.statisticSignalTickerDis: {exchange=%s}" %
            exchange)
        try:
            statistic = []
            db = DB()
            # statistic dis type
            for server, server_pair in combinations(exchange, 2):
                signal = db.getViewSignalTickerDisCurrentServer(
                    server, server_pair)
                signal = db.getSignalTickerDis()  # test only
                if not signal == []:
                    df = pd.DataFrame(signal)
                    for (fSymbol,
                         tSymbol), group in df.groupby(['fSymbol', 'tSymbol']):

                        print((fSymbol, tSymbol))
                        print(group.describe())
                        statistic.append({
                            "server": server,
                            "server_pair": server_pair,
                            "fSymbol": fSymbol,
                            "tSymbol": tSymbol,
                            "group": group
                        })
            print(statistic)
            return statistic
        except (DBException, Exception) as err:
            raise CalcException(err)

    def statisticSignalTickerTra(self, exchange):
        self._logger.debug(
            "src.core.calc.calc.Calc.statisticSignalTickerTra: {exchange=%s}" %
            exchange)
        return ['Tra']

    def statisticSignalTickerPair(self, exchange):
        self._logger.debug(
            "src.core.calc.calc.Calc.statisticSignalTickerPair: {exchange=%s}"
            % exchange)
        return ['Pair']

    def calcSignalTickerDis(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalTickerDis: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
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

    def calcSignalTickerTra(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalTickerTra: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
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
                # Begin Calc
                if r['C3_symbol'] == r['V3_fSymbol']:
                    # Type clockwise: sell->buy->sell
                    # calc symbol size
                    temp = min(r['V3_one_size'],
                               r['V1_one_size'] / C3_C1_one_price)
                    temp_size = min(r['V2_one_size'], temp)
                    r['V1_one_size'] = temp_size * C3_C1_one_price
                    r['V2_one_size'] = temp_size
                    r['V3_one_size'] = temp_size
                    # tra symbol
                    r['gain_symbol'] = r['C2_symbol']
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
                    # tra symbol
                    r['gain_symbol'] = r['C1_symbol']
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

    def calcSignalTickerPair(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalTickerPair: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
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
                    if r['C1_symbol'] == r['V1_fSymbol']:  # fSymbol -> tSymbol
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
                    if r['C2_symbol'] == r['V2_fSymbol']:  # fSymbol -> tSymbol
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
                    if r['C3_symbol'] == r['V3_fSymbol']:  # fSymbol -> tSymbol
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
                        r['J1_V3_one_price_base'] * r['J1_V3_one_size'],
                        r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                        r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                        r['J2_V3_one_price_base'] *
                        r['J2_V3_one_size']) / r['J1_V1_one_price_base']
                    r['J1_V2_one_size'] = min(
                        r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                        r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                        r['J1_V3_one_price_base'] * r['J1_V3_one_size'],
                        r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                        r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                        r['J2_V3_one_price_base'] *
                        r['J2_V3_one_size']) / r['J1_V2_one_price_base']
                    r['J1_V3_one_size'] = min(
                        r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                        r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                        r['J1_V3_one_price_base'] * r['J1_V3_one_size'],
                        r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                        r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                        r['J2_V3_one_price_base'] *
                        r['J2_V3_one_size']) / r['J1_V3_one_price_base']
                    r['J2_V1_one_size'] = min(
                        r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                        r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                        r['J1_V3_one_price_base'] * r['J1_V3_one_size'],
                        r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                        r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                        r['J2_V3_one_price_base'] *
                        r['J2_V3_one_size']) / r['J2_V1_one_price_base']
                    r['J2_V2_one_size'] = min(
                        r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                        r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                        r['J1_V3_one_price_base'] * r['J1_V3_one_size'],
                        r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                        r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                        r['J2_V3_one_price_base'] *
                        r['J2_V3_one_size']) / r['J2_V2_one_price_base']
                    r['J2_V3_one_size'] = min(
                        r['J1_V1_one_price_base'] * r['J1_V1_one_size'],
                        r['J1_V2_one_price_base'] * r['J1_V2_one_size'],
                        r['J1_V3_one_price_base'] * r['J1_V3_one_size'],
                        r['J2_V1_one_price_base'] * r['J2_V1_one_size'],
                        r['J2_V2_one_price_base'] * r['J2_V2_one_size'],
                        r['J2_V3_one_price_base'] *
                        r['J2_V3_one_size']) / r['J2_V3_one_price_base']
                    # calc base price
                    C1_symbol_base_price = (
                        r['J1_V1_one_price_base'] / r['J1_V1_one_price'] +
                        r['J2_V1_one_price_base'] / r['J2_V1_one_price']) / 2
                    C2_symbol_base_price = (
                        r['J1_V2_one_price_base'] / r['J1_V2_one_price'] +
                        r['J2_V2_one_price_base'] / r['J2_V2_one_price']) / 2
                    C3_symbol_base_price = (
                        r['J1_V3_one_price_base'] / r['J1_V3_one_price'] +
                        r['J2_V3_one_price_base'] / r['J2_V3_one_price']) / 2
                    # calc gain_base
                    C1_symbol_gain_base = (
                        r['J1_V1_one_price'] * r['J1_V1_one_size'] -
                        r['J2_V1_one_price'] * r['J2_V1_one_size'] -
                        r['J1_V1_one_price'] * r['J1_V1_one_size'] *
                        r['J1_V1_fee'] -
                        r['J2_V1_one_price'] * r['J2_V1_one_size'] *
                        r['J2_V1_fee']) * C1_symbol_base_price
                    C2_symbol_gain_base = (
                        r['J1_V2_one_price'] * r['J1_V2_one_size'] -
                        r['J2_V2_one_price'] * r['J2_V2_one_size'] -
                        r['J1_V2_one_price'] * r['J1_V2_one_size'] *
                        r['J1_V2_fee'] -
                        r['J2_V2_one_price'] * r['J2_V2_one_size'] *
                        r['J2_V2_fee']) * C2_symbol_base_price
                    C3_symbol_gain_base = (
                        r['J1_V3_one_price'] * r['J1_V3_one_size'] -
                        r['J2_V3_one_price'] * r['J2_V3_one_size'] -
                        r['J1_V3_one_price'] * r['J1_V3_one_size'] *
                        r['J1_V3_fee'] -
                        r['J2_V3_one_price'] * r['J2_V3_one_size'] *
                        r['J2_V3_fee']) * C3_symbol_base_price
                    r['gain_base'] = C1_symbol_gain_base + C2_symbol_gain_base + C3_symbol_gain_base
                    # calc gain_ratio
                    C1_symbol_gain_ratio_up = r['J1_V1_one_price'] - r[
                        'J2_V1_one_price'] - r['J1_V1_one_price'] * r[
                            'J1_V1_fee'] - r['J2_V1_one_price'] * r['J2_V1_fee']
                    C1_symbol_gain_ratio_dn = r['J1_V1_one_price'] + r[
                        'J2_V1_one_price']
                    C2_symbol_gain_ratio_up = r['J1_V2_one_price'] - r[
                        'J2_V2_one_price'] - r['J1_V2_one_price'] * r[
                            'J1_V2_fee'] - r['J2_V2_one_price'] * r['J2_V2_fee']
                    C2_symbol_gain_ratio_dn = r['J1_V2_one_price'] + r[
                        'J2_V2_one_price']
                    C3_symbol_gain_ratio_up = r['J1_V3_one_price'] - r[
                        'J2_V3_one_price'] - r['J1_V3_one_price'] * r[
                            'J1_V3_fee'] - r['J2_V3_one_price'] * r['J2_V3_fee']
                    C3_symbol_gain_ratio_dn = r['J1_V3_one_price'] + r[
                        'J2_V3_one_price']
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
