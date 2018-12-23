# -*- coding: utf-8 -*-

from decimal import ROUND_DOWN, ROUND_HALF_UP, ROUND_UP
from itertools import combinations

import pandas as pd

from src.core.coin.binance import Binance
from src.core.coin.enums import (CCAT_ORDER_SIDE_BUY, CCAT_ORDER_SIDE_SELL,
                                 CCAT_ORDER_TYPE_LIMIT)
from src.core.coin.huobi import Huobi
from src.core.coin.okex import Okex
from src.core.config import Config
from src.core.db.db import DB
from src.core.engine.enums import TYPE_DIS, TYPE_PAIR, TYPE_TRA
from src.core.util.exceptions import (BinanceException, CalcException,
                                      HuobiException, OkexException)
from src.core.util.helper import num_to_precision, utcnow_timestamp
from src.core.util.log import Logger


class Calc(object):
    def __init__(self):
        # config init
        # proxies
        self._proxies = Config()._Proxies_url if Config(
        )._Proxies_proxies else None
        # Okex
        self._Okex_exchange = Config()._Okex_exchange
        self._Okex_api_key = Config()._Okex_api_key
        self._Okex_api_secret = Config()._Okex_api_secret
        self._Okex_passphrase = Config()._Okex_passphrase
        # Binance
        self._Binance_exchange = Config()._Binance_exchange
        self._Binance_api_key = Config()._Binance_api_key
        self._Binance_api_secret = Config()._Binance_api_secret
        # Huobi
        self._Huobi_exchange = Config()._Huobi_exchange
        self._Huobi_api_key = Config()._Huobi_api_key
        self._Huobi_api_secret = Config()._Huobi_api_secret
        self._Huobi_acct_id = Config()._Huobi_acct_id
        # Coin API init
        self._Okex = Okex(self._Okex_exchange, self._Okex_api_key,
                          self._Okex_api_secret, self._Okex_passphrase,
                          self._proxies)
        self._Binance = Binance(self._Binance_exchange, self._Binance_api_key,
                                self._Binance_api_secret, self._proxies)
        self._Huobi = Huobi(self._Huobi_exchange, self._Huobi_api_key,
                            self._Huobi_api_secret, self._Huobi_acct_id,
                            self._proxies)
        # logger
        self._logger = Logger()

    def _calcSymbolTransOrders(self):
        self._logger.debug("src.core.calc.calc.Calc._calcSymbolTransOrders:")
        try:
            pass
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolTransOrders: exception err=" % err
            raise CalcException(errStr)

    def _calcSymbolPreTransOrders(self, server, fSymbol, tSymbol, fSymbol_base,
                                  tSymbol_base, resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolPreTransOrders:")
        try:
            print('in here')
            orders = []
            price_precision = 0
            size_precision = 0
            size_min = 0
            fee_ratio = 0
            # type I
            # handle fSymbol
            if fSymbol_base > 0:
                # de: direct trans
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server) & (resInfoSymbol['fSymbol']==fSymbol) & (resInfoSymbol['tSymbol']== baseCoin)]
                if not isDe.empty:
                    # baseCoin -> fSymbol
                    if not isDe['limit_price_precision'].values[0] == 'NULL':
                        price_precision =  isDe['limit_price_precision'].values[0]
                    if not isDe['limit_size_precision'].values[0] == 'NULL':
                        size_precision =  isDe['limit_size_precision'].values[0]
                    if not isDe['limit_size_min'].values[0] == 'NULL':
                        size_min =  isDe['limit_size_min'].values[0]
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if sever == self._Okex_exchange:
                        res = self._Okex.getMarketOrderbookDepth(fSymbol, baseCoin)
                    if sever == self._Binance_exchange:
                        res = self._Binance.getMarketOrderbookDepth(fSymbol, baseCoin)
                    if sever == self._Huobi_exchange:
                        res = self._Huobi.getMarketOrderbookDepth(fSymbol, baseCoin)
                    # calc orders
                    nowPrice = float(res['bid_price_size'][0][0])
                    deTradeSize = fSymbol_base/nowPrice
                    sum = 0
                    deTrade = []
                    for r in res['ask_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        if not sum < deTradeSize:
                            break
                        deSize = min(deTradeSize-sum, rSize)
                        if deSize > 0:
                            if deSize >= size_min:
                                sum = sum + deSize
                                deTrade.append({'price': rprice, 'size': deSize})
                    for trade in deTrade:
                        price = num_to_precision(
                            trade['price'],
                            price_precision,
                            rounding=ROUND_HALF_UP)
                        quantity = num_to_precision(
                            trade['size'],
                            size_precision,
                            rounding=ROUND_DOWN)
                        orders.append({"exchange":server, "fSymbol":fSymbol, "tSymbol":baseCoin, "ask_or_bid":CCAT_ORDER_SIDE_BUY, "price":price, "quantity":quantity, "ratio":fee_ratio, "type":CCAT_ORDER_TYPE_LIMIT})
                    # return
                    return orders
                # tra: trangle trans
                if isDe.empty:
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server) & (resInfoSymbol['fSymbol']==fSymbol) & (resInfoSymbol['tSymbol']==tSymbol)]
                isTra = resInfoSymbol[(resInfoSymbol['server'] == server) & (resInfoSymbol['fSymbol']==tSymbol) & (resInfoSymbol['tSymbol']== baseCoin)]
                    if not isDe.empty and not isTra.empty:
                        # baseCoin -> tSymbol
                        if not isTra['limit_price_precision'].values[0] == 'NULL':
                            price_precision =  isTra['limit_price_precision'].values[0]
                        if not isTra['limit_size_precision'].values[0] == 'NULL':
                            size_precision =  isTra['limit_size_precision'].values[0]
                        if not isTra['limit_size_min'].values[0] == 'NULL':
                            size_min =  isTra['limit_size_min'].values[0]
                        if not isTra['fee_taker'].values[0] == 'NULL':
                            fee_ratio = isTra['fee_taker'].values[0]
                        if sever == self._Okex_exchange:
                            res = self._Okex.getMarketOrderbookDepth(tSymbol, baseCoin)
                        if sever == self._Binance_exchange:
                            res = self._Binance.getMarketOrderbookDepth(tSymbol, baseCoin)
                        if sever == self._Huobi_exchange:
                            res = self._Huobi.getMarketOrderbookDepth(tSymbol, baseCoin)
                        # calc orders
                        nowPrice = float(res['bid_price_size'][0][0])
                        traTradeSize = fSymbol_base/nowPrice
                        sum = 0
                        traTrade = []
                        for r in res['ask_price_size']:
                            rprice = float(r[0])
                            rSize = float(r[1])
                            if not sum < traTradeSize:
                                break
                            traSize = min(traTradeSize-sum, rSize)
                            if traSize > 0:
                                if traSize >= size_min:
                                    sum = sum + traSize
                                    traTrade.append({'price': rprice, 'size': traSize})
                        for trade in traTrade:
                            price = num_to_precision(
                                trade['price'],
                                price_precision,
                                rounding=ROUND_HALF_UP)
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({"exchange":server, "fSymbol":fSymbol, "tSymbol":baseCoin, "ask_or_bid":CCAT_ORDER_SIDE_BUY, "price":price, "quantity":quantity, "ratio":fee_ratio, "type":CCAT_ORDER_TYPE_LIMIT})
                        # tSymbol -> fSymbol
                        sum_base = sum*(1-fee_ratio)
                        if not isDe['limit_price_precision'].values[0] == 'NULL':
                            price_precision =  isDe['limit_price_precision'].values[0]
                        if not isDe['limit_size_precision'].values[0] == 'NULL':
                            size_precision =  isDe['limit_size_precision'].values[0]
                        if not isDe['limit_size_min'].values[0] == 'NULL':
                            size_min =  isDe['limit_size_min'].values[0]
                        if not isDe['fee_taker'].values[0] == 'NULL':
                            fee_ratio = isDe['fee_taker'].values[0]
                        if sever == self._Okex_exchange:
                            res = self._Okex.getMarketOrderbookDepth(fSymbol, tSymbol)
                        if sever == self._Binance_exchange:
                            res = self._Binance.getMarketOrderbookDepth(fSymbol, tSymbol)
                        if sever == self._Huobi_exchange:
                            res = self._Huobi.getMarketOrderbookDepth(fSymbol, tSymbol)
                        # calc orders
                        nowPrice = float(res['bid_price_size'][0][0])
                        deTradeSize = sum_base/nowPrice
                        sum = 0
                        deTrade = []
                        for r in res['ask_price_size']:
                            rprice = float(r[0])
                            rSize = float(r[1])
                            if not sum < deTradeSize:
                                break
                            deSize = min(deTradeSize-sum, rSize)
                            if deSize > 0:
                                if deSize >= size_min:
                                    sum = sum + deSize
                                    deTrade.append({'price': rprice, 'size': deSize})
                        for trade in deTrade:
                            price = num_to_precision(
                                trade['price'],
                                price_precision,
                                rounding=ROUND_HALF_UP)
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({"exchange":server, "fSymbol":fSymbol, "tSymbol":baseCoin, "ask_or_bid":CCAT_ORDER_SIDE_BUY, "price":price, "quantity":quantity, "ratio":fee_ratio, "type":CCAT_ORDER_TYPE_LIMIT})
                        # return
                        return orders
            # type II
            # handle tSymbol
            if tSymbol_base >0:
                # need no trans
                if tSymbol == baseCoin:
                    # return []
                    return orders
                # direct trans
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server) & (resInfoSymbol['tSymbol']==fSymbol) & (resInfoSymbol['tSymbol']== baseCoin)]
                if not isDe.empty:
                    # baseCoin -> tSymbol
                    if not isDe['limit_price_precision'].values[0] == 'NULL':
                        price_precision =  isDe['limit_price_precision'].values[0]
                    if not isDe['limit_size_precision'].values[0] == 'NULL':
                        size_precision =  isDe['limit_size_precision'].values[0]
                    if not isDe['limit_size_min'].values[0] == 'NULL':
                        size_min =  isDe['limit_size_min'].values[0]
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if sever == self._Okex_exchange:
                        res = self._Okex.getMarketOrderbookDepth(tSymbol, baseCoin)
                    if sever == self._Binance_exchange:
                        res = self._Binance.getMarketOrderbookDepth(tSymbol, baseCoin)
                    if sever == self._Huobi_exchange:
                        res = self._Huobi.getMarketOrderbookDepth(tSymbol, baseCoin)
                    # calc orders
                    nowPrice = float(res['bid_price_size'][0][0])
                    deTradeSize = tSymbol_base/nowPrice
                    sum = 0
                    deTrade = []
                    for r in res['ask_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        if not sum < deTradeSize:
                            break
                        deSize = min(deTradeSize-sum, rSize)
                        if deSize > 0:
                            if deSize >= size_min:
                                sum = sum + deSize
                                deTrade.append({'price': rprice, 'size': deSize})
                    for trade in deTrade:
                        price = num_to_precision(
                            trade['price'],
                            price_precision,
                            rounding=ROUND_HALF_UP)
                        quantity = num_to_precision(
                            trade['size'],
                            size_precision,
                            rounding=ROUND_DOWN)
                        orders.append({"exchange":server, "fSymbol":fSymbol, "tSymbol":baseCoin, "ask_or_bid":CCAT_ORDER_SIDE_BUY, "price":price, "quantity":quantity, "ratio":fee_ratio, "type":CCAT_ORDER_TYPE_LIMIT})
                    # return
                    return orders
            # type III
            # not found, return []
            return orders
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolPreTransOrders: exception err=" % err
            raise CalcException(errStr)


    def _calcSymbolRunTransOrders(self):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolRunTransOrders:")
        try:
            pass
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolRunTransOrders: exception err=" % err
            raise CalcException(errStr)

    def _calcSymbolAfterTransOrders(self):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolAfterTransOrders:")
        try:
            pass
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolAfterTransOrders: exception err=" % err
            raise CalcException(errStr)

    def calcSignalPreTransOrders(self, signal, resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalPreTransOrders: {signal=%s, resInfoSymbol=%s, baseCoin=%s}"
            % (signal, 'resInfoSymbol', baseCoin))
        try:
            res = []
            type = signal['type']
            if type == TYPE_DIS:
                bid_order = self._calcSymbolPreTransOrders(
                    signal['bid_server'], signal['fSymbol'], signal['tSymbol'],
                    signal['base_start'], 0, resInfoSymbol, baseCoin)
                ask_order = self._calcSymbolPreTransOrders(
                    signal['ask_server'], signal['fSymbol'], signal['tSymbol'],
                    0, signal['base_start'], resInfoSymbol, baseCoin)
                res.append(bid_server)
                res.append(ask_server)

            return res
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcSignalPreTransOrders: {self, signal=%s, resInfoSymbol=%s, baseCoin=%s}, exception err=" % (
                signal, 'resInfoSymbol', baseCoin, err)
            raise CalcException(errStr)

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
                            group['gain_base'].values.std(),
                            "gain_ratio_max":
                            group['gain_ratio'].max(),
                            "gain_ratio_min":
                            group['gain_ratio'].min(),
                            "gain_ratio_mean":
                            group['gain_ratio'].mean(),
                            "gain_ratio_std":
                            group['gain_ratio'].values.std()
                        }
                        # update statistic
                        statistic.append(sta)
            return statistic
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcStatisticSignalTickerDis: {exchange=%s, timeWindow=%s}, exception err=%s" % (
                exchange, timeWindow, err)
            raise CalcException(errStr)

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
                    symbol_pair = [(s['V1_fSymbol'], s['V1_tSymbol']),
                                   (s['V2_fSymbol'], s['V2_tSymbol']),
                                   (s['V3_fSymbol'], s['V3_tSymbol'])]
                    symbol_pair.sort()
                    s['symbol_pair'] = str(symbol_pair)
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
                        group[(group['C3_symbol'] == group['V3_fSymbol']
                               )].shape[0],
                        "count_backward":
                        group[(group['C3_symbol'] == group['V3_tSymbol']
                               )].shape[0],
                        "gain_base_max":
                        group['gain_base'].max(),
                        "gain_base_min":
                        group['gain_base'].min(),
                        "gain_base_mean":
                        group['gain_base'].mean(),
                        "gain_base_std":
                        group['gain_base'].values.std(),
                        "gain_ratio_max":
                        group['gain_ratio'].max(),
                        "gain_ratio_min":
                        group['gain_ratio'].min(),
                        "gain_ratio_mean":
                        group['gain_ratio'].mean(),
                        "gain_ratio_std":
                        group['gain_ratio'].values.std()
                    }
                    # update statistic
                    statistic.append(sta)
            return statistic
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcStatisticSignalTickerTra: {exchange=%s, timeWindow=%s}, exception err=%s" % (
                exchange, timeWindow, err)
            raise CalcException(errStr)

    def calcStatisticSignalTickerPair(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticSignalTickerPair: {exchange=%s, timeWindow=%s}"
            % (exchange, timeWindow))
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
                        symbol_pair = [(s['V1_fSymbol'], s['V1_tSymbol']),
                                       (s['V2_fSymbol'], s['V2_tSymbol']),
                                       (s['V3_fSymbol'], s['V3_tSymbol'])]
                        symbol_pair.sort()
                        s['symbol_pair'] = str(symbol_pair)
                        df.append(s)
                    df = pd.DataFrame(signal)
                    # calc
                    for symbol_pair, group in df.groupby(['symbol_pair']):
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
                            group[(group['C3_symbol'] == group['V3_fSymbol']
                                   )].shape[0],
                            "count_backward":
                            group[(group['C3_symbol'] == group['V3_tSymbol']
                                   )].shape[0],
                            "gain_base_max":
                            group['gain_base'].max(),
                            "gain_base_min":
                            group['gain_base'].min(),
                            "gain_base_mean":
                            group['gain_base'].mean(),
                            "gain_base_std":
                            group['gain_base'].values.std(),
                            "gain_ratio_max":
                            group['gain_ratio'].max(),
                            "gain_ratio_min":
                            group['gain_ratio'].min(),
                            "gain_ratio_mean":
                            group['gain_ratio'].mean(),
                            "gain_ratio_std":
                            group['gain_ratio'].values.std()
                        }
                        # update statistic
                        statistic.append(sta)
            return statistic
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcStatisticSignalTickerPair: {exchange=%s, timeWindow=%s}, exception err=%s" % (
                exchange, timeWindow, err)
            raise CalcException(errStr)

    def calcJudgeSignalTickerDis(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeSignalTickerDis: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, 'resInfoSymbol'))
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
                    r['bid_fee'] = 0
                    bid_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['bid_server'])
                        & (resInfoSymbol['fSymbol'] == r['fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['tSymbol']
                           )]['fee_taker']
                    r['ask_fee'] = 0
                    ask_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['ask_server'])
                        & (resInfoSymbol['fSymbol'] == r['fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['tSymbol']
                           )]['fee_taker']
                    if not bid_fee.empty:
                        if not bid_fee.values[0] == 'NULL':
                            r['bid_fee'] = bid_fee.values[0]
                    if not ask_fee.empty:
                        if not ask_fee.values[0] == 'NULL':
                            r['ask_fee'] = ask_fee.values[0]
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
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcJudgeSignalTickerDis: {exchange=%s, threshold=%s, resInfoSymbol=%s}, exception err=%s" % (
                exchange, threshold, 'resInfoSymbol', err)
            raise CalcException(errStr)

    def calcJudgeSignalTickerTra(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeSignalTickerTra: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, 'resInfoSymbol'))
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
                r['V1_fee'] = 0
                V1_fee = resInfoSymbol[
                    (resInfoSymbol['server'] == r['server'])
                    & (resInfoSymbol['fSymbol'] == r['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                       )]['fee_taker']
                r['V2_fee'] = 0
                V2_fee = resInfoSymbol[
                    (resInfoSymbol['server'] == r['server'])
                    & (resInfoSymbol['fSymbol'] == r['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                       )]['fee_taker']
                r['V3_fee'] = 0
                V3_fee = resInfoSymbol[
                    (resInfoSymbol['server'] == r['server'])
                    & (resInfoSymbol['fSymbol'] == r['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                       )]['fee_taker']
                if not V1_fee.empty:
                    if not V1_fee.values[0] == 'NULL':
                        r['V1_fee'] = V1_fee.values[0]
                if not V2_fee.empty:
                    if not V2_fee.values[0] == 'NULL':
                        r['V2_fee'] = V2_fee.values[0]
                if not V3_fee.empty:
                    if not V3_fee.values[0] == 'NULL':
                        r['V3_fee'] = V3_fee.values[0]
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
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcJudgeSignalTickerTra: {exchange=%s, threshold=%s, resInfoSymbol=%s}, exception err=%s" % (
                exchange, threshold, 'resInfoSymbol', err)
            raise CalcException(errStr)

    def calcJudgeSignalTickerPair(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeSignalTickerPair: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, 'resInfoSymbol'))
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
                    r['J1_V1_fee'] = 0
                    J1_V1_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J1_server'])
                        & (resInfoSymbol['fSymbol'] == r['V1_fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                           )]['fee_taker']
                    r['J1_V2_fee'] = 0
                    J1_V2_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J1_server'])
                        & (resInfoSymbol['fSymbol'] == r['V2_fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                           )]['fee_taker']
                    r['J1_V3_fee'] = 0
                    J1_V3_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J1_server'])
                        & (resInfoSymbol['fSymbol'] == r['V3_fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                           )]['fee_taker']
                    r['J2_V1_fee'] = 0
                    J2_V1_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J2_server'])
                        & (resInfoSymbol['fSymbol'] == r['V1_fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                           )]['fee_taker'].values[0]
                    r['J2_V2_fee'] = 0
                    J2_V2_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J2_server'])
                        & (resInfoSymbol['fSymbol'] == r['V2_fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                           )]['fee_taker'].values[0]
                    r['J2_V3_fee'] = 0
                    J2_V3_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J2_server'])
                        & (resInfoSymbol['fSymbol'] == r['V3_fSymbol'])
                        & (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                           )]['fee_taker'].values[0]
                    if not J1_V1_fee.empty:
                        if not J1_V1_fee.values[0] == 'NULL':
                            r['J1_V1_fee'] = J1_V1_fee.values[0]
                    if not J1_V2_fee.empty:
                        if not J1_V2_fee.values[0] == 'NULL':
                            r['J1_V2_fee'] = J1_V2_fee.values[0]
                    if not J1_V3_fee.empty:
                        if not J1_V3_fee.values[0] == 'NULL':
                            r['J1_V3_fee'] = J1_V3_fee.values[0]
                     if not J2_V1_fee.empty:
                         if not J2_V1_fee.values[0] == 'NULL':
                             r['J2_V1_fee'] = J2_V1_fee.values[0]
                     if not J2_V2_fee.empty:
                         if not J2_V2_fee.values[0] == 'NULL':
                             r['J2_V2_fee'] = J2_V2_fee.values[0]
                     if not J2_V3_fee.empty:
                         if not J2_V3_fee.values[0] == 'NULL':
                             r['J2_V3_fee'] = J2_V3_fee.values[0]
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
        except (BinanceException, HuobiException, OkexException, Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcJudgeSignalTickerPair: {exchange=%s, threshold=%s, resInfoSymbol=%s}, exception err=%s" % (
                exchange, threshold, 'resInfoSymbol', err)
            raise CalcException(errStr)
