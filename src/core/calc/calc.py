# -*- coding: utf-8 -*-

from itertools import combinations

import pandas as pd
from src.core.db.db import DB
from src.core.util.exceptions import CalcException, DBException
from src.core.util.log import Logger


class Calc(object):
    def __init__(self):
        # logger
        self._logger = Logger()

    def calcSignalTickerDis(self, exchanges, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalTickerDis: {exchanges=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchanges, threshold, resInfoSymbol))
        try:
            db = DB()
            signal = []
            # calc dis type
            for item in combinations(exchanges, 2):
                res = db.getViewMarketTickerCurrentDisServer(item[0], item[1])
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
                    r['gain_base'] = r['bid_price_base'] * r['bid_size'] - r[
                        'ask_price_base'] * r['ask_size'] - r[
                            'bid_price_base'] * r['bid_size'] * r[
                                'bid_fee'] - r['ask_price_base'] * r[
                                    'ask_size'] * r['ask_fee']
                    # calc gain_ratio
                    r['gain_ratio'] = (r['bid_price'] - r['ask_price'] -
                                       r['bid_price'] * r['bid_fee'] -
                                       r['ask_price'] * r['ask_fee']) / (
                                           r['bid_price'] + r['ask_price'])
                    # calc signal
                    if r['gain_ratio'] > threshold:
                        signal.append(r)
            # return signal
            return signal
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcSignalTickerTra(self, exchanges, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalTickerTra: {exchanges=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchanges, threshold, resInfoSymbol))
        try:
            db = DB()
            signal = []
            # calc tra type
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
                    r['C1_symbol_base'] = r['V1_bid_one_price_base']
                else:  # tSymbol -> fSymbol
                    r['V1_one_price'] = r['V1_ask_one_price']
                    r['V1_one_price_base'] = r['V1_ask_one_price_base']
                    r['V1_one_size'] = r['V1_ask_one_size']
                    r['C1_symbol_base'] = r['V1_ask_one_price_base'] / r[
                        'V1_ask_one_price']
                # calc V2
                if r['C2_symbol'] == r['V2_fSymbol']:  # fSymbol -> tSymbol
                    r['V2_one_price'] = r['V2_bid_one_price']
                    r['V2_one_price_base'] = r['V2_bid_one_price_base']
                    r['V2_one_size'] = r['V2_bid_one_size']
                    r['C2_symbol_base'] = r['V2_bid_one_price_base']
                else:  # tSymbol -> fSymbol
                    r['V2_one_price'] = r['V2_ask_one_price']
                    r['V2_one_price_base'] = r['V2_ask_one_price_base']
                    r['V2_one_size'] = r['V2_ask_one_size']
                    r['C2_symbol_base'] = r['V2_ask_one_price_base'] / r[
                        'V2_ask_one_price']
                # calc V3
                if r['C3_symbol'] == r['V3_fSymbol']:  # fSymbol -> tSymbol
                    r['V3_one_price'] = r['V3_bid_one_price']
                    r['V3_one_price_base'] = r['V3_bid_one_price_base']
                    r['V3_one_size'] = r['V3_bid_one_size']
                    r['C3_symbol_base'] = r['V3_bid_one_price_base']
                else:  # tSymbol -> fSymbol
                    r['V3_one_price'] = r['V3_ask_one_price']
                    r['V3_one_price_base'] = r['V3_ask_one_price_base']
                    r['V3_one_size'] = r['V3_ask_one_size']
                    r['C3_symbol_base'] = r['V3_ask_one_price_base'] / r[
                        'V3_ask_one_price']
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
                if C2_symbol_price * C3_symbol_price > 1 / C1_symbol_price:  # tra C2_symbol -> C1_symbol
                    before = r['V1_one_size'] * r['C1_symbol_base']
                    after = C1_symbol_price * C2_symbol_price * C3_symbol_price * (
                        1 - r['V1_fee']) * (1 - r['V2_fee']) * (
                            1 - r['V3_fee']
                        ) * r['V1_one_size'] * r['C1_symbol_base']
                    # calc gain_symbol
                    r['gain_symbol'] = r['C1_symbol']
                    # calc gain_base
                    r['gain_base'] = after - before
                    # calc gain_ratio
                    r['gain_ratio'] = (after - before) / (before + after)
                    # change candy
                    candy = True
                # Type II
                if C1_symbol_price * C3_symbol_price > 1 / C2_symbol_price:  # tra C3_symbol -> C2_symbol
                    before = r['V2_one_size'] * r['C2_symbol_base']
                    after = C1_symbol_price * C2_symbol_price * C3_symbol_price * (
                        1 - r['V1_fee']) * (1 - r['V2_fee']) * (
                            1 - r['V3_fee']
                        ) * r['V2_one_size'] * r['C2_symbol_base']
                    if not candy:
                        # calc gain_symbol
                        r['gain_symbol'] = r['C2_symbol']
                        # calc gain_base
                        r['gain_base'] = after - before
                        # calc gain_ratio
                        r['gain_ratio'] = (after - before) / (before + after)
                    else:
                        if (after - before) / (
                                before + after) > r['gain_ratio']:
                            # calc gain_symbol
                            r['gain_symbol'] = r['C2_symbol']
                            # calc gain_base
                            r['gain_base'] = after - before
                            # calc gain_ratio
                            r['gain_ratio'] = (after - before) / (
                                before + after)
                    # change candy
                    candy = True
                # Type III
                if C1_symbol_price * C2_symbol_price > 1 / C3_symbol_price:  # tra C1_symbol -> C3_symbol
                    before = r['V3_one_size'] * r['C3_symbol_base']
                    after = C1_symbol_price * C2_symbol_price * C3_symbol_price * (
                        1 - r['V1_fee']) * (1 - r['V2_fee']) * (
                            1 - r['V3_fee']
                        ) * r['V3_one_size'] * r['C3_symbol_base']
                    if not candy:
                        # calc gain_symbol
                        r['gain_symbol'] = r['C3_symbol']
                        # calc gain_base
                        r['gain_base'] = after - before
                        # calc gain_ratio
                        r['gain_ratio'] = (after - before) / (before + after)
                    else:
                        if (after - before) / (
                                before + after) > r['gain_ratio']:
                            # calc gain_symbol
                            r['gain_symbol'] = r['C3_symbol']
                            # calc gain_base
                            r['gain_base'] = after - before
                            # calc gain_ratio
                            r['gain_ratio'] = (after - before) / (
                                before + after)
                    # change candy
                    candy = True
                # calc signal
                if candy:
                    if r['gain_ratio'] > threshold:
                        signal.append(r)
            # return signal
            return signal
        except (DBException, Exception) as err:
            raise CalcException(err)

    def calcSignalTickerPair(self, exchanges, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalTickerPair: {exchanges=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchanges, threshold, resInfoSymbol))
        try:
            db = DB()
            signal = []
            # calc pair type
            for item in combinations(exchanges, 2):
                res = db.getViewMarketTickerCurrentPairServer(item[0], item[1])
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
                    # calc gain_base
                    C1_symbol_gain_base = r['J1_V1_one_price_base'] * r[
                        'J1_V1_one_size'] - r['J2_V1_one_price_base'] * r[
                            'J2_V1_one_size'] - r['J1_V1_one_price_base'] * r[
                                'J1_V1_one_size'] * r['J1_V1_fee'] - r[
                                    'J2_V1_one_price_base'] * r[
                                        'J2_V1_one_size'] * r['J2_V1_fee']
                    C2_symbol_gain_base = r['J1_V2_one_price_base'] * r[
                        'J1_V2_one_size'] - r['J2_V2_one_price_base'] * r[
                            'J2_V2_one_size'] - r['J1_V2_one_price_base'] * r[
                                'J1_V2_one_size'] * r['J1_V2_fee'] - r[
                                    'J2_V2_one_price_base'] * r[
                                        'J2_V2_one_size'] * r['J2_V2_fee']
                    C3_symbol_gain_base = r['J1_V3_one_price_base'] * r[
                        'J1_V3_one_size'] - r['J2_V3_one_price_base'] * r[
                            'J2_V3_one_size'] - r['J1_V3_one_price_base'] * r[
                                'J1_V3_one_size'] * r['J1_V3_fee'] - r[
                                    'J2_V3_one_price_base'] * r[
                                        'J2_V3_one_size'] * r['J2_V3_fee']
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
