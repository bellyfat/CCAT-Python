# -*- coding: utf-8 -*-

import uuid
from decimal import ROUND_DOWN
from itertools import combinations

import pandas as pd
from src.core.calc.enums import CALC_ZERO_NUMBER
from src.core.coin.binance import Binance
from src.core.coin.enums import *
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

    def _calcStatusAssetByBaseCoin(self, assets, resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcStatusAssetByBaseCoin:")
        try:
            assets_base = 0
            for asset in assets:
                # base: do nothing
                if asset['asset'] == baseCoin:
                    assets_base = assets_base + asset['balance']
                    continue
                # de: direct trans: asset -> baseCoin
                isDe = resInfoSymbol[
                    (resInfoSymbol['server'] == asset['server'])
                    & (resInfoSymbol['fSymbol'] == asset['asset'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                if not isDe.empty:
                    # asset -> baseCoin
                    fee_ratio = 0
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if asset['server'] == self._Okex_exchange:
                        ticker = self._Okex.getMarketOrderbookTicker(
                            asset['asset'], baseCoin, aggDepth=0)
                    if asset['server'] == self._Binance_exchange:
                        ticker = self._Binance.getMarketOrderbookTicker(
                            asset['asset'], baseCoin, aggDepth=0)
                    if asset['server'] == self._Huobi_exchange:
                        ticker = self._Huobi.getMarketOrderbookTicker(
                            asset['asset'], baseCoin, aggDepth=0)
                    assets_base = assets_base + ticker['bid_one_price'] * (
                        1 - fee_ratio) * asset['balance']
                    continue
                # tra: trangle trans: asset -> tSymbol -> baseCoin
                if isDe.empty:
                    isTra = resInfoSymbol[
                        (resInfoSymbol['server'] == asset['server']) &
                        (resInfoSymbol['fSymbol'] == asset['asset'])]
                    if not isTra.empty:
                        candy = False
                        for i in range(isTra.shape[0]):
                            tSymbol = isTra['tSymbol'].values[i]
                            isTraDe = resInfoSymbol[
                                (resInfoSymbol['server'] == asset['server'])
                                & (resInfoSymbol['fSymbol'] == tSymbol)
                                & (resInfoSymbol['tSymbol'] == baseCoin)]
                            if not isTraDe.empty:
                                candy = True
                                break
                        if not candy:
                            raise Exception(
                                "TRADE PAIRS NOT FOUND ERROR, asset to baseCoin trade pairs not found."
                            )
                        fee_ratio = 0
                        fee1_ratio = 0
                        if not isTra['fee_taker'].values[0] == 'NULL':
                            fee_ratio = isTra['fee_taker'].values[0]
                        if not isTraDe['fee_taker'].values[0] == 'NULL':
                            fee1_ratio = isTraDe['fee_taker'].values[0]

                        # asset -> tSymbol -> baseCoin
                        if asset['server'] == self._Okex_exchange:
                            ticker = self._Okex.getMarketOrderbookTicker(
                                asset['asset'], tSymbol, aggDepth=0)
                            ticker1 = self._Okex.getMarketOrderbookTicker(
                                tSymbol, baseCoin, aggDepth=0)
                        if asset['server'] == self._Binance_exchange:
                            ticker = self._Binance.getMarketOrderbookTicker(
                                asset['asset'], tSymbol, aggDepth=0)
                            ticker1 = self._Binance.getMarketOrderbookTicker(
                                tSymbol, baseCoin, aggDepth=0)
                        if asset['server'] == self._Huobi_exchange:
                            ticker = self._Huobi.getMarketOrderbookTicker(
                                asset['asset'], tSymbol, aggDepth=0)
                            ticker1 = self._Huobi.getMarketOrderbookTicker(
                                tSymbol, baseCoin, aggDepth=0)
                        assets_base = assets_base + ticker1['bid_one_price'] * (
                            1 - fee1_ratio) * ticker['bid_one_price'] * (
                                1 - fee_ratio) * asset['balance']
            # return
            return assets_base
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcStatusAssetByBaseCoin: exception err=%s" % err
            raise CalcException(errStr)

    def calcSignalStatusByOrders(self, signal, infoOrders, resInfoSymbol,
                                 baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalStatusByOrders: {signal=%s, infoOrders=%s, resInfoSymbol=%s, baseCoin=%s}"
            % (signal, 'infoOrders', 'resInfoSymbol', baseCoin))
        try:
            status = []
            # check for sure
            orders = infoOrders[(infoOrders['group_id'] == signal['group_id'])]
            if not orders.empty:
                # calc fee_ratio
                for index, order in orders.iterrows():
                    orders.loc[index, 'fee_ratio'] = 0
                    fee_ratio = resInfoSymbol[
                        (resInfoSymbol['server'] == order['server']) &
                        (resInfoSymbol['fSymbol'] == order['fSymbol']) &
                        (resInfoSymbol['tSymbol'] == order['tSymbol']
                           )]['fee_taker']
                    if not fee_ratio.empty:
                        if not fee_ratio.values[0] == 'NULL':
                            orders.loc[index, 'fee_ratio'] = fee_ratio.values[
                                0]
                # calc fSymbol, tSymbol
                fSymbol_assets = []
                tSymbol_assets = []
                for (server, fSymbol, tSymbol), group in orders.groupby(
                        ['server', 'fSymbol', 'tSymbol']):
                    fBalance = 0
                    fFree = 0
                    fLocked = 0
                    tBalance = 0
                    tFree = 0
                    tLocked = 0
                    # type: buy
                    g = group[(group['server'] == server) &
                              (group['ask_or_bid'] == CCAT_ORDER_SIDE_BUY)]
                    if not g.empty:
                        # fSymbol
                        fBalance = fBalance + g['filled_size'].sum()
                        fFree = fFree + g['filled_size'].sum()
                        # tSymbol
                        tBalance = tBalance - g.apply(
                            lambda x: x['filled_price'] * x['filled_size'],
                            axis=1).sum() - g['fee'].sum()
                        tLocked = tLocked + g.apply(
                            lambda x: x['ask_bid_price'] * x['ask_bid_size'] * (
                                1 + x['fee_ratio']) - x['filled_price'] * x['filled_size'] - x['fee'],
                            axis=1).sum()
                        tFree = tFree - g.apply(
                            lambda x: x['ask_bid_price'] * x['ask_bid_size'] * (
                                1 + x['fee_ratio']) - x['filled_price'] * x['filled_size'] - x['fee'],
                            axis=1).sum() - g.apply(
                                lambda x: x['filled_price'] * x['filled_size'],
                                axis=1).sum() - g['fee'].sum()
                    # type sell
                    g = group[(group['server'] == server) &
                              (group['ask_or_bid'] == CCAT_ORDER_SIDE_SELL)]
                    if not g.empty:
                        # fSymbol
                        fBalance = fBalance - g['filled_size'].sum()
                        fLocked = fLocked + g.apply(
                            lambda x: x['ask_bid_size'] - x['filled_size'],
                            axis=1).sum()
                        fFree = fFree - g.apply(
                            lambda x: x['ask_bid_size'] - x['filled_size'],
                            axis=1).sum() - g['filled_size'].sum()
                        # tSymbol
                        tBalance = tBalance + g.apply(
                            lambda x: x['filled_price'] * x['filled_size'],
                            axis=1).sum() - g['fee'].sum()
                        tFree = tFree + g.apply(
                            lambda x: x['filled_price'] * x['filled_size'],
                            axis=1).sum() - g['fee'].sum()
                    fSymbol_assets.append({
                        "server": server,
                        "asset": fSymbol,
                        "balance": fBalance,
                        "free": fFree,
                        "locked": fLocked
                    })
                    tSymbol_assets.append({
                        "server": server,
                        "asset": tSymbol,
                        "balance": tBalance,
                        "free": tFree,
                        "locked": tLocked
                    })
                # update status_asset
                status_assets = []
                signal_assets = pd.DataFrame(signal['status_assets'])
                fSymbol_assets = pd.DataFrame(fSymbol_assets)
                tSymbol_assets = pd.DataFrame(tSymbol_assets)
                assets = signal_assets.append(fSymbol_assets).append(
                    tSymbol_assets)
                for (server,
                     asset), group in assets.groupby(['server', 'asset']):
                    status_assets.append({
                        "server": server,
                        "asset": asset,
                        "balance": group['balance'].sum(),
                        "free": group["free"].sum(),
                        "locked": group['locked'].sum()
                    })
                # update status_gain
                status_assets_base = self._calcStatusAssetByBaseCoin(
                    status_assets, resInfoSymbol, baseCoin)
                status_gain = (status_assets_base
                               - signal['base_start']) / signal['base_start']
                # udpate status_done
                status_done = status_gain >= signal['base_gain']
                status = {
                    "status_done": status_done,
                    "status_assets": status_assets,
                    "status_gain": status_gain
                }
            # return
            return status
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcSignalStatusByOrders: {signal=%s, infoOrders=%s, resInfoSymbol=%s, baseCoin=%s}, exception err=%s" % (
                signal, 'infoOrders', 'resInfoSymbol', baseCoin, err)
            raise CalcException(errStr)

    def _calcSymbolPreTradeOrders(self, server, fSymbol, tSymbol, fSymbol_base,
                                  tSymbol_base, group_id, resInfoSymbol,
                                  baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolPreTradeOrders:")
        try:
            orders = []
            # type I
            # handle fSymbol
            if fSymbol_base > 0:
                # print('in type I')
                # de: direct trans
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server)
                                     & (resInfoSymbol['fSymbol'] == fSymbol)
                                     & (resInfoSymbol['tSymbol'] == baseCoin)]
                if not isDe.empty:
                    # print('in Type I: de')
                    # baseCoin -> fSymbol
                    price_precision = 0
                    size_precision = 0
                    size_min = 0
                    min_notional = 0
                    fee_ratio = 0
                    if not isDe['limit_price_precision'].values[0] == 'NULL':
                        price_precision = isDe['limit_price_precision'].values[
                            0]
                    if not isDe['limit_size_precision'].values[0] == 'NULL':
                        size_precision = isDe['limit_size_precision'].values[0]
                    if not isDe['limit_size_min'].values[0] == 'NULL':
                        size_min = isDe['limit_size_min'].values[0]
                    if not isDe['limit_min_notional'].values[0] == 'NULL':
                        min_notional = isDe['limit_min_notional'].values[0]
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if server == self._Okex_exchange:
                        res = self._Okex.getMarketOrderbookDepth(
                            fSymbol, baseCoin)
                    if server == self._Binance_exchange:
                        res = self._Binance.getMarketOrderbookDepth(
                            fSymbol, baseCoin)
                    if server == self._Huobi_exchange:
                        res = self._Huobi.getMarketOrderbookDepth(
                            fSymbol, baseCoin)
                    # calc orders
                    deTradeNotional = fSymbol_base * (1 - fee_ratio)
                    deTradeSize = deTradeNotional / float(
                        res['ask_price_size'][0][0])
                    # print('in Type I: de, deTradeNotional=%s, min_notional=%s' % (deTradeNotional, min_notional))
                    # print('in Type I: de, deTradeSize=%s, size_min=%s' %  (deTradeSize, size_min))
                    if deTradeNotional < min_notional - CALC_ZERO_NUMBER or deTradeSize < size_min - CALC_ZERO_NUMBER:
                        raise Exception(
                            "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                            % (server, baseCoin, fSymbol, deTradeSize))
                    sum = 0
                    deTrade = []
                    for r in res['ask_price_size'][
                            0:10]:  # ask 1 to ask 10, no more
                        if not sum < deTradeNotional:
                            break
                        rPrice = float(r[0])
                        rSize = float(r[1])
                        deTradeSize = (deTradeNotional - sum) / rPrice
                        deSize = min(deTradeSize, rSize)
                        if deSize > 0:
                            if deSize >= size_min:
                                if not deSize * rPrice >= min_notional:
                                    continue
                                sum = sum + deSize * rPrice
                                if sum <= deTradeNotional + CALC_ZERO_NUMBER:
                                    deTrade.append({
                                        'price': rPrice,
                                        'size': deSize
                                    })
                    # print('in Type I: de, server=%s, res=%s' % (server, res['ask_price_size'][0:10]))
                    # print('in Type I: de, deTradeNotional=%s' % deTradeNotional)
                    # print('in Type I: de, sum=%s' % sum)
                    if sum < deTradeNotional - min_notional - CALC_ZERO_NUMBER:
                        raise Exception(
                            "TRANS TOO MUCH ERROR，amount is not enough with ask 1 to ask 10: {server=%s, trade=(%s -> %s), amount=%s}"
                            % (server, baseCoin, fSymbol, deTradeSize))
                    for trade in deTrade:
                        price = num_to_precision(
                            trade['price'],
                            price_precision,
                            rounding=ROUND_DOWN)
                        quantity = num_to_precision(
                            trade['size'], size_precision, rounding=ROUND_DOWN)
                        orders.append({
                            "server": server,
                            "fSymbol": fSymbol,
                            "tSymbol": baseCoin,
                            "ask_or_bid": CCAT_ORDER_SIDE_BUY,
                            "price": price,
                            "quantity": quantity,
                            "ratio": fee_ratio,
                            "type": CCAT_ORDER_TYPE_LIMIT,
                            "group_id": group_id
                        })
                    # type I: de done
                    # print('out type I: de done')
                # tra: trangle trans
                if isDe.empty:
                    # print('in type I: tra')
                    isDe = resInfoSymbol[(resInfoSymbol['server'] == server)
                                         & (resInfoSymbol['fSymbol'] == fSymbol)

                                         & (resInfoSymbol['tSymbol'] == tSymbol)]
                    isTra = resInfoSymbol[
                        (resInfoSymbol['server'] == server)
                        & (resInfoSymbol['fSymbol'] == tSymbol)
                        & (resInfoSymbol['tSymbol'] == baseCoin)]
                    if isDe.empty or isTra.empty:
                        raise Exception(
                            "TRADE PAIRS NOT FOUND ERROR, tSymbol to fSymbol trade pairs not found."
                        )
                    if not isTra.empty:
                        # baseCoin -> tSymbol
                        price_precision = 0
                        size_precision = 0
                        size_min = 0
                        min_notional = 0
                        fee_ratio = 0
                        if not isTra['limit_price_precision'].values[
                                0] == 'NULL':
                            price_precision = isTra[
                                'limit_price_precision'].values[0]
                        if not isTra['limit_size_precision'].values[
                                0] == 'NULL':
                            size_precision = isTra[
                                'limit_size_precision'].values[0]
                        if not isTra['limit_size_min'].values[0] == 'NULL':
                            size_min = isTra['limit_size_min'].values[0]
                        if not isTra['limit_min_notional'].values[0] == 'NULL':
                            min_notional = isTra['limit_min_notional'].values[
                                0]
                        if not isTra['fee_taker'].values[0] == 'NULL':
                            fee_ratio = isTra['fee_taker'].values[0]
                        if server == self._Okex_exchange:
                            res = self._Okex.getMarketOrderbookDepth(
                                tSymbol, baseCoin)
                        if server == self._Binance_exchange:
                            res = self._Binance.getMarketOrderbookDepth(
                                tSymbol, baseCoin)
                        if server == self._Huobi_exchange:
                            res = self._Huobi.getMarketOrderbookDepth(
                                tSymbol, baseCoin)
                        # calc orders
                        traTradeNotional = fSymbol_base * (1 - fee_ratio)
                        traTradeSize = traTradeNotional / float(
                            res['ask_price_size'][0][0])
                        # print('in type I: tra, traTradeNotional=%s, min_notional=%s' % (traTradeNotional, min_notional))
                        # print('in type I: tra, traTradeSize=%s, size_min=%s' % (traTradeSize, size_min))
                        if traTradeNotional < min_notional - CALC_ZERO_NUMBER or traTradeSize < size_min - CALC_ZERO_NUMBER:
                            raise Exception(
                                "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, baseCoin, tSymbol, traTradeSize))
                        sum = 0
                        traTrade = []
                        for r in res['ask_price_size'][
                                0:10]:  # ask 1 to ask 10, no more
                            if not sum < traTradeNotional:
                                break
                            rPrice = float(r[0])
                            rSize = float(r[1])
                            traTradeSize = (traTradeNotional - sum) / rPrice
                            traSize = min(traTradeSize, rSize)
                            if traSize > 0:
                                if traSize >= size_min:
                                    if not traSize * rPrice >= min_notional:
                                        continue
                                    sum = sum + traSize * rPrice
                                    if sum <= traTradeNotional + CALC_ZERO_NUMBER:
                                        traTrade.append({
                                            'price': rPrice,
                                            'size': traSize
                                        })
                        # print('in type I: tra, server=%s, res=%s' % (server, res['ask_price_size'][0:10]))
                        # print('in type I: tra, traTradeNotional=%s' % traTradeNotional)
                        # print('in type I: tra, sum=%s' % sum)
                        if sum < traTradeNotional - min_notional - CALC_ZERO_NUMBER:
                            raise Exception(
                                "TRANS TOO MUCH ERROR，amount is not enough with ask 1 to ask 10: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, baseCoin, tSymbol, traTradeSize))
                        for trade in traTrade:
                            price = num_to_precision(
                                trade['price'],
                                price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": tSymbol,
                                "tSymbol": baseCoin,
                                "ask_or_bid": CCAT_ORDER_SIDE_BUY,
                                "price": price,
                                "quantity": quantity,
                                "ratio": fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                        # tSymbol -> fSymbol
                        # print('in type I: tra, traTrade=%s' % traTrade)
                        sum_base = 0
                        for trade in traTrade:
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            sum_base = sum_base + float(quantity)
                        price_precision = 0
                        size_precision = 0
                        size_min = 0
                        min_notional = 0
                        fee_ratio = 0
                        if not isDe['limit_price_precision'].values[
                                0] == 'NULL':
                            price_precision = isDe[
                                'limit_price_precision'].values[0]
                        if not isDe['limit_size_precision'].values[0] == 'NULL':
                            size_precision = isDe[
                                'limit_size_precision'].values[0]
                        if not isDe['limit_size_min'].values[0] == 'NULL':
                            size_min = isDe['limit_size_min'].values[0]
                        if not isDe['limit_min_notional'].values[0] == 'NULL':
                            min_notional = isDe['limit_min_notional'].values[0]
                        if not isDe['fee_taker'].values[0] == 'NULL':
                            fee_ratio = isDe['fee_taker'].values[0]
                        if server == self._Okex_exchange:
                            res = self._Okex.getMarketOrderbookDepth(
                                fSymbol, tSymbol)
                        if server == self._Binance_exchange:
                            res = self._Binance.getMarketOrderbookDepth(
                                fSymbol, tSymbol)
                        if server == self._Huobi_exchange:
                            res = self._Huobi.getMarketOrderbookDepth(
                                fSymbol, tSymbol)
                        # calc orders
                        deTradeNotional = sum_base * (1 - fee_ratio)
                        deTradeSize = deTradeNotional / float(
                            res['ask_price_size'][0][0])
                        # print('in type I: tra, deTradeNotional=%s, min_notional=%s' % (deTradeNotional, min_notional))
                        # print('in type I: tra, deTradeSize=%s, size_min=%s' % (deTradeSize, size_min))
                        if deTradeNotional < min_notional - CALC_ZERO_NUMBER or deTradeSize < size_min - CALC_ZERO_NUMBER:
                            raise Exception(
                                "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, tSymbol, fSymbol, deTradeSize))
                        sum = 0
                        deTrade = []
                        for r in res['ask_price_size'][
                                0:10]:  # ask 1 to ask 10, no more
                            if not sum < deTradeNotional:
                                break
                            rPrice = float(r[0])
                            rSize = float(r[1])
                            deTradeSize = (deTradeNotional - sum) / rPrice
                            deSize = min(deTradeSize, rSize)
                            if deSize > 0:
                                if deSize >= size_min:
                                    if not deSize * rPrice >= min_notional:
                                        continue
                                    sum = sum + deSize * rPrice
                                    if sum <= deTradeNotional + CALC_ZERO_NUMBER:
                                        deTrade.append({
                                            'price': rPrice,
                                            'size': deSize
                                        })
                        # print('in type I: tra, server=%s, res=%s' % (server, res['ask_price_size'][0:10]))
                        # print('in type I: tra, deTradeNotional=%s' % deTradeNotional)
                        # print('in type I: tra, sum=%s' % sum)
                        if sum < deTradeNotional - min_notional - CALC_ZERO_NUMBER:
                            raise Exception(
                                "TRANS TOO MUCH ERROR，amount is not enough with ask 1 to ask 10: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, tSymbol, fSymbol, deTradeSize))
                        for trade in deTrade:
                            price = num_to_precision(
                                trade['price'],
                                price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": fSymbol,
                                "tSymbol": tSymbol,
                                "ask_or_bid": CCAT_ORDER_SIDE_BUY,
                                "price": price,
                                "quantity": quantity,
                                "ratio": fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                        # done type I: tra
                        # print('out type I: tra done')
            # type II
            # handle tSymbol
            if tSymbol_base > 0:
                # print('in type II')
                # need no trans
                if tSymbol == baseCoin:
                    # print('in type II: need no trans')
                    # done type II: need no trans
                    pass
                    # print('out type II: need no trans done')
                # direct trans
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server)
                                     & (resInfoSymbol['fSymbol'] == tSymbol)
                                     & (resInfoSymbol['tSymbol'] == baseCoin)]
                if not isDe.empty:
                    # print('in type II: de')
                    # baseCoin -> tSymbol
                    price_precision = 0
                    size_precision = 0
                    size_min = 0
                    min_notional = 0
                    fee_ratio = 0
                    if not isDe['limit_price_precision'].values[0] == 'NULL':
                        price_precision = isDe['limit_price_precision'].values[
                            0]
                    if not isDe['limit_size_precision'].values[0] == 'NULL':
                        size_precision = isDe['limit_size_precision'].values[0]
                    if not isDe['limit_size_min'].values[0] == 'NULL':
                        size_min = isDe['limit_size_min'].values[0]
                    if not isDe['limit_min_notional'].values[0] == 'NULL':
                        min_notional = isDe['limit_min_notional'].values[0]
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if server == self._Okex_exchange:
                        res = self._Okex.getMarketOrderbookDepth(
                            tSymbol, baseCoin)
                    if server == self._Binance_exchange:
                        res = self._Binance.getMarketOrderbookDepth(
                            tSymbol, baseCoin)
                    if server == self._Huobi_exchange:
                        res = self._Huobi.getMarketOrderbookDepth(
                            tSymbol, baseCoin)
                    # calc orders
                    # print('in type II: de, tSymbol_base=%s, fee_ratio=%s' % (tSymbol_base, fee_ratio))
                    deTradeNotional = tSymbol_base * (1 - fee_ratio)
                    deTradeSize = deTradeNotional / float(
                        res['ask_price_size'][0][0])
                    # print('in type II: de, deTradeNotional=%s, min_notional=%s' % (deTradeNotional, min_notional))
                    # print('in type II: de, deTradeSize=%s, size_min=%s' % (deTradeSize, size_min))
                    if deTradeNotional < min_notional - CALC_ZERO_NUMBER or deTradeSize < size_min - CALC_ZERO_NUMBER:
                        raise Exception(
                            "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                            % (server, baseCoin, tSymbol, deTradeSize))
                    sum = 0
                    deTrade = []
                    for r in res['ask_price_size'][
                            0:10]:  # ask 1 to ask 10, no more
                        if not sum < deTradeNotional:
                            break
                        rPrice = float(r[0])
                        rSize = float(r[1])
                        deTradeSize = (deTradeNotional - sum) / rPrice
                        deSize = min(deTradeSize, rSize)
                        if deSize > 0:
                            if deSize >= size_min:
                                if not deSize * rPrice >= min_notional:
                                    continue
                                sum = sum + deSize * rPrice
                                if sum <= deTradeNotional + CALC_ZERO_NUMBER:
                                    deTrade.append({
                                        'price': rPrice,
                                        'size': deSize
                                    })
                    # print('in type II: de, server=%s, res=%s' % (server, res['ask_price_size'][0:10]))
                    # print('in type II: de, deTradeNotional=%s' % deTradeNotional)
                    # print('in type II: de, sum=%s' % sum)
                    if sum < deTradeNotional - min_notional - CALC_ZERO_NUMBER:
                        raise Exception(
                            "TRANS TOO MUCH ERROR，amount is not enough with ask 1 to ask 10: {server=%s, trade=(%s -> %s), amount=%s}"
                            % (server, baseCoin, tSymbol, deTradeSize))
                    for trade in deTrade:
                        price = num_to_precision(
                            trade['price'],
                            price_precision,
                            rounding=ROUND_DOWN)
                        quantity = num_to_precision(
                            trade['size'], size_precision, rounding=ROUND_DOWN)
                        orders.append({
                            "server": server,
                            "fSymbol": tSymbol,
                            "tSymbol": baseCoin,
                            "ask_or_bid": CCAT_ORDER_SIDE_BUY,
                            "price": price,
                            "quantity": quantity,
                            "ratio": fee_ratio,
                            "type": CCAT_ORDER_TYPE_LIMIT,
                            "group_id": group_id
                        })
                    # done type II: de
                    # print('out type II: de done')
            # return
            # print('return orders:%s' % orders)
            return orders
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolPreTradeOrders: exception err=%s" % err
            raise CalcException(errStr)

    def _calcSymbolRunTradeOrdersTypeDis(
            self, bid_server, ask_server, fSymbol, tSymbol, status_assets,
            forward_ratio, backward_ratio, group_id, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolRunTradeOrdersTypeDis:")
        try:
            orders = []
            # calc symbol pair info
            isBid = resInfoSymbol[(resInfoSymbol['server'] == bid_server)
                                  & (resInfoSymbol['fSymbol'] == fSymbol)
                                  & (resInfoSymbol['tSymbol'] == tSymbol)]
            isAsk = resInfoSymbol[(resInfoSymbol['server'] == ask_server)
                                  & (resInfoSymbol['fSymbol'] == fSymbol)
                                  & (resInfoSymbol['tSymbol'] == tSymbol)]
            if isBid.empty or isAsk.empty:
                return orders
            # bid server limit and fee
            bid_price_precision = 0
            bid_price_step = 0
            bid_size_precision = 0
            bid_size_min = 0
            bid_min_notional = 0
            bid_fee_ratio = 0
            if not isBid['limit_price_precision'].values[0] == 'NULL':
                bid_price_precision = isBid['limit_price_precision'].values[0]
            if not isBid['limit_price_step'].values[0] == 'NULL':
                bid_price_step = isBid['limit_price_step'].values[0]
            if not isBid['limit_size_precision'].values[0] == 'NULL':
                bid_size_precision = isBid['limit_size_precision'].values[0]
            if not isBid['limit_size_min'].values[0] == 'NULL':
                bid_size_min = isBid['limit_size_min'].values[0]
            if not isBid['limit_min_notional'].values[0] == 'NULL':
                bid_min_notional = isBid['limit_min_notional'].values[0]
            if not isBid['fee_taker'].values[0] == 'NULL':
                bid_fee_ratio = isBid['fee_taker'].values[0]
            # ask server limit and fee
            ask_price_precision = 0
            ask_price_step = 0
            ask_size_precision = 0
            ask_size_min = 0
            ask_min_notional = 0
            ask_fee_ratio = 0
            if not isAsk['limit_price_precision'].values[0] == 'NULL':
                ask_price_precision = isAsk['limit_price_precision'].values[0]
            if not isAsk['limit_price_step'].values[0] == 'NULL':
                ask_price_step = isAsk['limit_price_step'].values[0]
            if not isAsk['limit_size_precision'].values[0] == 'NULL':
                ask_size_precision = isAsk['limit_size_precision'].values[0]
            if not isAsk['limit_size_min'].values[0] == 'NULL':
                ask_size_min = isAsk['limit_size_min'].values[0]
            if not isAsk['limit_min_notional'].values[0] == 'NULL':
                ask_min_notional = isAsk['limit_min_notional'].values[0]
            if not isAsk['fee_taker'].values[0] == 'NULL':
                ask_fee_ratio = isAsk['fee_taker'].values[0]
            # aggDepth
            aggDepth = max(bid_price_step, ask_price_step)
            # calc balance
            bid_fSymbol_free = 0
            bid_tSymbol_free = 0
            ask_fSymbol_free = 0
            ask_tSymbol_free = 0
            for status in status_assets:
                if status['server'] == bid_server:
                    if status['asset'] == fSymbol:
                        bid_fSymbol_free = status['free']
                    if status['asset'] == tSymbol:
                        bid_tSymbol_free = status['free']
                if status['server'] == ask_server:
                    if status['asset'] == fSymbol:
                        ask_fSymbol_free = status['free']
                    if status['asset'] == tSymbol:
                        ask_tSymbol_free = status['free']
            # bid server market order book ticker
            if bid_server == self._Okex_exchange:
                bid_res = self._Okex.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
            if bid_server == self._Binance_exchange:
                bid_res = self._Binance.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
            if bid_server == self._Huobi_exchange:
                bid_res = self._Huobi.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
            # ask server market order book ticker
            if ask_server == self._Okex_exchange:
                ask_res = self._Okex.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
            if ask_server == self._Binance_exchange:
                ask_res = self._Binance.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
            if ask_server == self._Huobi_exchange:
                ask_res = self._Huobi.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
            # forward
            # calc type dis price and size
            bid_price = float(bid_res['bid_one_price'])
            bid_size = float(bid_res['bid_one_size'])
            ask_price = float(ask_res['ask_one_price'])
            ask_size = float(ask_res['ask_one_size'])
            gain_ratio = (bid_price - ask_price - bid_price * bid_fee_ratio
                          - ask_price * ask_fee_ratio) / ask_price
            # print('dis forward gain_ratio: %s' % gain_ratio)
            if gain_ratio > forward_ratio:
                bid_size = min(bid_fSymbol_free, bid_size)
                ask_size = min(
                    ask_tSymbol_free * (1 - ask_fee_ratio) / ask_price,
                    ask_size)
                order_size = min(bid_size, ask_size)
                # print('dis forward bid_fSymbol_free: %s' % bid_fSymbol_free)
                # print('dis forward ask_tSymbol_free: %s' % ask_tSymbol_free)
                # print('dis forward bid_price: %s' % bid_price)
                # print('dis forward ask_price: %s' % ask_price)
                # print('dis forward order_size: %s' % order_size)
                # print('dis forward bid_size_min: %s' % bid_size_min)
                # print('dis forward ask_size_min: %s' % ask_size_min)
                # print('dis forward bid_min_notional: %s' % bid_min_notional)
                # print('dis forward ask_min_notional: %s' % ask_min_notional)
                if order_size > 0:
                    if order_size >= bid_size_min and order_size >= ask_size_min:
                        if bid_price * order_size > bid_min_notional and ask_price * order_size > ask_min_notional:
                            price = num_to_precision(
                                bid_price,
                                bid_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                order_size,
                                bid_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": bid_server,
                                "fSymbol": fSymbol,
                                "tSymbol": tSymbol,
                                "ask_or_bid": CCAT_ORDER_SIDE_SELL,
                                "price": price,
                                "quantity": quantity,
                                "ratio": bid_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                ask_price,
                                ask_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                order_size,
                                ask_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": ask_server,
                                "fSymbol": fSymbol,
                                "tSymbol": tSymbol,
                                "ask_or_bid": CCAT_ORDER_SIDE_BUY,
                                "price": price,
                                "quantity": quantity,
                                "ratio": ask_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
            # backward
            # calc type dis price and size
            bid_price = float(bid_res['ask_one_price'])
            bid_size = float(bid_res['ask_one_size'])
            ask_price = float(ask_res['bid_one_price'])
            ask_size = float(ask_res['bid_one_size'])
            gain_ratio = (ask_price - bid_price - bid_price * bid_fee_ratio
                          - ask_price * ask_fee_ratio) / bid_price
            # print('dis backward gain_ratio: %s' % gain_ratio)
            if gain_ratio < backward_ratio:
                bid_size = min(
                    bid_tSymbol_free * (1 - bid_fee_ratio) / bid_price,
                    bid_size)
                ask_size = min(ask_fSymbol_free, ask_size)
                order_size = min(bid_size, ask_size)
                # print('dis backward bid_tSymbol_free: %s' % bid_tSymbol_free)
                # print('dis backward ask_fSymbol_free: %s' % ask_fSymbol_free)
                # print('dis backward bid_price: %s' % bid_price)
                # print('dis backward ask_price: %s' % ask_price)
                # print('dis backward order_size: %s' % order_size)
                # print('dis backward bid_size_min: %s' % bid_size_min)
                # print('dis backward ask_size_min: %s' % ask_size_min)
                # print('dis backward bid_min_notional: %s' % bid_min_notional)
                # print('dis backward ask_min_notional: %s' % ask_min_notional)
                if order_size > 0:
                    if order_size >= bid_size_min and order_size >= ask_size_min:
                        if bid_price * order_size >= bid_min_notional and ask_price * order_size >= ask_min_notional:
                            price = num_to_precision(
                                bid_price,
                                bid_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                order_size,
                                bid_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": bid_server,
                                "fSymbol": fSymbol,
                                "tSymbol": tSymbol,
                                "ask_or_bid": CCAT_ORDER_SIDE_BUY,
                                "price": price,
                                "quantity": quantity,
                                "ratio": bid_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                ask_price,
                                ask_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                order_size,
                                ask_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": ask_server,
                                "fSymbol": fSymbol,
                                "tSymbol": tSymbol,
                                "ask_or_bid": CCAT_ORDER_SIDE_SELL,
                                "price": price,
                                "quantity": quantity,
                                "ratio": ask_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
            # return
            return orders
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolRunTradeOrdersTypeDis: exception err=%s" % err
            raise CalcException(errStr)

    def _calcSymbolRunTradeOrdersTypeTra(
            self, server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol,
            V3_fSymbol, V3_tSymbol, status_assets, forward_ratio, group_id,
            resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolRunTradeOrdersTypeTra:")
        try:
            orders = []
            # calc symbol pair info
            is_V1 = resInfoSymbol[(resInfoSymbol['server'] == server)
                                  & (resInfoSymbol['fSymbol'] == V1_fSymbol)
                                  & (resInfoSymbol['tSymbol'] == V1_tSymbol)]
            is_V2 = resInfoSymbol[(resInfoSymbol['server'] == server)
                                  & (resInfoSymbol['fSymbol'] == V2_fSymbol)
                                  & (resInfoSymbol['tSymbol'] == V2_tSymbol)]
            is_V3 = resInfoSymbol[(resInfoSymbol['server'] == server)
                                  & (resInfoSymbol['fSymbol'] == V3_fSymbol)
                                  & (resInfoSymbol['tSymbol'] == V3_tSymbol)]
            if is_V1.empty or is_V2.empty or is_V3.empty:
                # print('is_V1, is_V2 or is_V3 is empty.')
                return orders
            # server limit and fee
            V1_price_precision = 0
            V1_price_step = 0
            V1_size_precision = 0
            V1_size_min = 0
            V1_min_notional = 0
            V1_fee_ratio = 0
            if not is_V1['limit_price_precision'].values[0] == 'NULL':
                V1_price_precision = is_V1['limit_price_precision'].values[0]
            if not is_V1['limit_price_step'].values[0] == 'NULL':
                V1_price_step = is_V1['limit_price_step'].values[0]
            if not is_V1['limit_size_precision'].values[0] == 'NULL':
                V1_size_precision = is_V1['limit_size_precision'].values[0]
            if not is_V1['limit_size_min'].values[0] == 'NULL':
                V1_size_min = is_V1['limit_size_min'].values[0]
            if not is_V1['limit_min_notional'].values[0] == 'NULL':
                V1_min_notional = is_V1['limit_min_notional'].values[0]
            if not is_V1['fee_taker'].values[0] == 'NULL':
                V1_fee_ratio = is_V1['fee_taker'].values[0]
            V2_price_precision = 0
            V2_price_step = 0
            V2_size_precision = 0
            V2_size_min = 0
            V2_min_notional = 0
            V2_fee_ratio = 0
            if not is_V2['limit_price_precision'].values[0] == 'NULL':
                V2_price_precision = is_V2['limit_price_precision'].values[0]
            if not is_V2['limit_price_step'].values[0] == 'NULL':
                V2_price_step = is_V2['limit_price_step'].values[0]
            if not is_V2['limit_size_precision'].values[0] == 'NULL':
                V2_size_precision = is_V2['limit_size_precision'].values[0]
            if not is_V2['limit_size_min'].values[0] == 'NULL':
                V2_size_min = is_V2['limit_size_min'].values[0]
            if not is_V2['limit_min_notional'].values[0] == 'NULL':
                V2_min_notional = is_V2['limit_min_notional'].values[0]
            if not is_V2['fee_taker'].values[0] == 'NULL':
                V2_fee_ratio = is_V2['fee_taker'].values[0]
            V3_price_precision = 0
            V3_price_step = 0
            V3_size_precision = 0
            V3_size_min = 0
            V3_min_notional = 0
            V3_fee_ratio = 0
            if not is_V3['limit_price_precision'].values[0] == 'NULL':
                V3_price_precision = is_V3['limit_price_precision'].values[0]
            if not is_V3['limit_price_step'].values[0] == 'NULL':
                V3_price_step = is_V3['limit_price_step'].values[0]
            if not is_V3['limit_size_precision'].values[0] == 'NULL':
                V3_size_precision = is_V3['limit_size_precision'].values[0]
            if not is_V3['limit_size_min'].values[0] == 'NULL':
                V3_size_min = is_V3['limit_size_min'].values[0]
            if not is_V3['limit_min_notional'].values[0] == 'NULL':
                V3_min_notional = is_V3['limit_min_notional'].values[0]
            if not is_V3['fee_taker'].values[0] == 'NULL':
                V3_fee_ratio = is_V3['fee_taker'].values[0]
            # aggDepth
            V1_aggDepth = V1_price_step
            V2_aggDepth = V2_price_step
            V3_aggDepth = V3_price_step
            # calc common symbol
            C1_symbol = [
                i for i in [V1_fSymbol, V1_tSymbol]
                if i in [V3_fSymbol, V3_tSymbol]
            ][0]
            C2_symbol = [
                i for i in [V1_fSymbol, V1_tSymbol]
                if i in [V2_fSymbol, V2_tSymbol]
            ][0]
            C3_symbol = [
                i for i in [V2_fSymbol, V2_tSymbol]
                if i in [V3_fSymbol, V3_tSymbol]
            ][0]
            # calc balance
            C1_symbol_balance = 0
            C2_symbol_balance = 0
            C3_symbol_balance = 0
            for sa in status_assets:
                if sa['server'] == server:
                    if sa['asset'] == C1_symbol:
                        C1_symbol_balance = sa['free']
                    if sa['asset'] == C2_symbol:
                        C2_symbol_balance = sa['free']
                    if sa['asset'] == C3_symbol:
                        C3_symbol_balance = sa['free']
            # print('C1_symbol=%s, C1_symbol_balance=%s' % (C1_symbol, C1_symbol_balance))
            # print('C2_symbol=%s, C2_symbol_balance=%s' % (C2_symbol, C2_symbol_balance))
            # print('C3_symbol=%s, C3_symbol_balance=%s' % (C3_symbol, C3_symbol_balance))
            # server market order book ticker
            if server == self._Okex_exchange:
                V1_res = self._Okex.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                V2_res = self._Okex.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V1_aggDepth)
                V3_res = self._Okex.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V1_aggDepth)
            if server == self._Binance_exchange:
                V1_res = self._Binance.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V2_aggDepth)
                V2_res = self._Binance.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                V3_res = self._Binance.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V2_aggDepth)
            if server == self._Huobi_exchange:
                V1_res = self._Huobi.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V3_aggDepth)
                V2_res = self._Huobi.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V3_aggDepth)
                V3_res = self._Huobi.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            # print('V1_res=%s' % V1_res)
            # print('V2_res=%s' % V2_res)
            # print('V3_res=%s' % V3_res)
            # calc type tra price and size
            # calc V1
            if C1_symbol == V1_fSymbol:  # fSymbol -> tSymbol
                V1_one_price = float(V1_res['bid_one_price'])
                V1_one_side = CCAT_ORDER_SIDE_SELL
                V1_one_size = float(V1_res['bid_one_size'])
                V1_one_size = min(V1_one_size, C1_symbol_balance)
            else:  # tSymbol -> fSymbol
                V1_one_price = float(V1_res['ask_one_price'])
                V1_one_side = CCAT_ORDER_SIDE_BUY
                V1_one_size = float(V1_res['ask_one_size'])
                V1_one_size = min(V1_one_size,
                                  C1_symbol_balance / V1_one_price)
            # calc V2
            if C2_symbol == V2_fSymbol:  # fSymbol -> tSymbol
                V2_one_price = float(V2_res['bid_one_price'])
                V2_one_side = CCAT_ORDER_SIDE_SELL
                V2_one_size = float(V2_res['bid_one_size'])
                V2_one_size = min(V2_one_size, C2_symbol_balance)
            else:  # tSymbol -> fSymbol
                V2_one_price = float(V2_res['ask_one_price'])
                V2_one_side = CCAT_ORDER_SIDE_BUY
                V2_one_size = float(V2_res['ask_one_size'])
                V2_one_size = min(V2_one_size,
                                  C2_symbol_balance / V2_one_price)
            # calc V3
            if C3_symbol == V3_fSymbol:  # fSymbol -> tSymbol
                V3_one_price = float(V3_res['bid_one_price'])
                V3_one_side = CCAT_ORDER_SIDE_SELL
                V3_one_size = float(V3_res['bid_one_size'])
                V3_one_size = min(V3_one_size, C3_symbol_balance)
            else:  # tSymbol -> fSymbol
                V3_one_price = float(V3_res['ask_one_price'])
                V3_one_side = CCAT_ORDER_SIDE_BUY
                V3_one_size = float(V3_res['ask_one_size'])
                V3_one_size = min(V3_one_size,
                                  C3_symbol_balance / V3_one_price)
            # print('V1_one_price=%s, V1_one_size=%s' % (V1_one_price, V1_one_size))
            # print('V2_one_price=%s, V2_one_size=%s' % (V2_one_price, V2_one_size))
            # print('V3_one_price=%s, V3_one_size=%s' % (V3_one_price, V3_one_size))
            # calc symbol one price ratio
            if C3_symbol == V3_fSymbol:
                # Type clockwise
                C1_C2_one_price = V1_one_price
                C2_C3_one_price = 1 / V2_one_price
                C3_C1_one_price = V3_one_price
            else:
                # Type anti-clockwise
                C1_C2_one_price = V1_one_price
                C2_C3_one_price = 1 / V2_one_price
                C3_C1_one_price = 1 / V3_one_price
            # print('C1_C2_one_price=%s' % C1_C2_one_price)
            # print('C2_C3_one_price=%s' % C2_C3_one_price)
            # print('C3_C1_one_price=%s' % C3_C1_one_price)
            # calc tra result
            if not C1_C2_one_price * C2_C3_one_price * C3_C1_one_price > 1:
                # print('tra check result not exist, return')
                return orders
            # Begin Calc Gain: Gain V2 tSymbol
            if C3_symbol == V3_fSymbol:
                # Type clockwise: sell->buy->sell
                # calc symbol size
                temp_C3 = min(
                    V3_one_size,
                    V2_one_size * C2_C3_one_price * (1 - V2_fee_ratio))
                temp_C1 = min(V1_one_size,
                              temp_C3 * C3_C1_one_price * (1 - V3_fee_ratio))
                temp_C3 = temp_C1 / C3_C1_one_price / (1 - V3_fee_ratio)
                temp_C2 = temp_C3 / C2_C3_one_price / (1 - V2_fee_ratio)
                V2_one_size = temp_C2 * (1 - V2_fee_ratio) / V2_one_price
                V3_one_size = V2_one_size
                V1_one_size = V3_one_size * V3_one_price * (1 - V3_fee_ratio)
            else:
                # Type anti-clockwise: sell->buy->buy
                # calc symbol size
                temp_C3 = min(
                    V3_one_size,
                    V2_one_size * C2_C3_one_price * (1 - V2_fee_ratio))
                temp_C1 = min(V1_one_size,
                              temp_C3 * C3_C1_one_price * (1 - V3_fee_ratio))
                temp_C3 = temp_C1 / C3_C1_one_price / (1 - V3_fee_ratio)
                temp_C2 = temp_C3 / C2_C3_one_price / (1 - V2_fee_ratio)
                V2_one_size = temp_C2 * (1 - V2_fee_ratio) / V2_one_price
                V3_one_size = V2_one_size * (1 - V3_fee_ratio) / V3_one_price
                V1_one_size = V3_one_size
            # calc gain_ratio
            gain_ratio = (
                C1_C2_one_price * C3_C1_one_price * (1 - V1_fee_ratio)
                * (1 - V3_fee_ratio) - 1 / C2_C3_one_price
                - 1 / C2_C3_one_price * V2_fee_ratio) / (1 / C2_C3_one_price)
            # forward
            # print('tra forward gain_ratio: %s' % gain_ratio)
            if gain_ratio > forward_ratio:
                # print('tra forward C1_symbol_balance: %s' % C1_symbol_balance)
                # print('tra forward C2_symbol_balance: %s' % C2_symbol_balance)
                # print('tra forward C3_symbol_balance: %s' % C3_symbol_balance)
                # print('tra forward V1_one_price: %s' % V1_one_price)
                # print('tra forward V2_one_price: %s' % V2_one_price)
                # print('tra forward V3_one_price: %s' % V3_one_price)
                # print('tra forward V1_one_size: %s' % V1_one_size)
                # print('tra forward V2_one_size: %s' % V2_one_size)
                # print('tra forward V3_one_size: %s' % V3_one_size)
                # print('tra forward V1_one_side: %s' % V1_one_side)
                # print('tra forward V2_one_side: %s' % V2_one_side)
                # print('tra forward V3_one_side: %s' % V3_one_side)
                # print('tra forward V1_size_min: %s' % V1_size_min)
                # print('tra forward V2_size_min: %s' % V2_size_min)
                # print('tra forward V3_size_min: %s' % V3_size_min)
                # print('tra forward V1_min_notional: %s' % V1_min_notional)
                # print('tra forward V2_min_notional: %s' % V2_min_notional)
                # print('tra forward V3_min_notional: %s' % V3_min_notional)
                if V1_one_size > 0 and V2_one_size > 0 and V3_one_size > 0:
                    if V1_one_size >= V1_size_min and V2_one_size >= V2_size_min and V3_one_size >= V3_size_min:
                        if V1_one_price * V1_one_size >= V1_min_notional and V2_one_price * V2_one_size >= V2_min_notional and V3_one_price * V3_one_size >= V3_min_notional:
                            # print('tra forward result exist: add orders')
                            price = num_to_precision(
                                V1_one_price,
                                V1_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                V1_one_size,
                                V1_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": V1_fSymbol,
                                "tSymbol": V1_tSymbol,
                                "ask_or_bid": V1_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": V1_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                V2_one_price,
                                V2_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                V2_one_size,
                                V2_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": V2_fSymbol,
                                "tSymbol": V2_tSymbol,
                                "ask_or_bid": V2_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": V2_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                V3_one_price,
                                V3_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                V3_one_size,
                                V3_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": V3_fSymbol,
                                "tSymbol": V3_tSymbol,
                                "ask_or_bid": V3_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": V3_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
            # return
            return orders
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolRunTradeOrdersTypeTra: exception err=%s" % err
            raise CalcException(errStr)

    def _calcSymbolRunTradeOrdersTypePair(
            self, J1_server, J2_server, V1_fSymbol, V1_tSymbol, V2_fSymbol,
            V2_tSymbol, V3_fSymbol, V3_tSymbol, status_assets, forward_ratio,
            group_id, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolRunTradeOrdersTypePair:")
        try:
            orders = []
            # calc symbol pair info
            is_J1_V1 = resInfoSymbol[(resInfoSymbol['server'] == J1_server) &
                                     (resInfoSymbol['fSymbol'] == V1_fSymbol)

                                     & (resInfoSymbol['tSymbol'] == V1_tSymbol)]
            is_J1_V2 = resInfoSymbol[(resInfoSymbol['server'] == J1_server) &
                                     (resInfoSymbol['fSymbol'] == V2_fSymbol)

                                     & (resInfoSymbol['tSymbol'] == V2_tSymbol)]
            is_J1_V3 = resInfoSymbol[(resInfoSymbol['server'] == J1_server) &
                                     (resInfoSymbol['fSymbol'] == V3_fSymbol)

                                     & (resInfoSymbol['tSymbol'] == V3_tSymbol)]
            is_J2_V1 = resInfoSymbol[(resInfoSymbol['server'] == J2_server) &
                                     (resInfoSymbol['fSymbol'] == V1_fSymbol)

                                     & (resInfoSymbol['tSymbol'] == V1_tSymbol)]
            is_J2_V2 = resInfoSymbol[(resInfoSymbol['server'] == J2_server) &
                                     (resInfoSymbol['fSymbol'] == V2_fSymbol)

                                     & (resInfoSymbol['tSymbol'] == V2_tSymbol)]
            is_J2_V3 = resInfoSymbol[(resInfoSymbol['server'] == J2_server) &
                                     (resInfoSymbol['fSymbol'] == V3_fSymbol)

                                     & (resInfoSymbol['tSymbol'] == V3_tSymbol)]
            if is_J1_V1.empty or is_J1_V2.empty or is_J1_V3.empty or is_J2_V1.empty or is_J2_V2.empty or is_J2_V3.empty:
                # print('is_J1_V1, is_J1_V2, is_J1_V3, is_J1_V1, is_J1_V2, is_J1_V3 is empty.')
                return orders
            # server limit and fee
            J1_V1_price_precision = 0
            J1_V1_price_step = 0
            J1_V1_size_precision = 0
            J1_V1_size_min = 0
            J1_V1_min_notional = 0
            J1_V1_fee_ratio = 0
            if not is_J1_V1['limit_price_precision'].values[0] == 'NULL':
                J1_V1_price_precision = is_J1_V1[
                    'limit_price_precision'].values[0]
            if not is_J1_V1['limit_price_step'].values[0] == 'NULL':
                J1_V1_price_step = is_J1_V1['limit_price_step'].values[0]
            if not is_J1_V1['limit_size_precision'].values[0] == 'NULL':
                J1_V1_size_precision = is_J1_V1['limit_size_precision'].values[
                    0]
            if not is_J1_V1['limit_size_min'].values[0] == 'NULL':
                J1_V1_size_min = is_J1_V1['limit_size_min'].values[0]
            if not is_J1_V1['limit_min_notional'].values[0] == 'NULL':
                J1_V1_min_notional = is_J1_V1['limit_min_notional'].values[0]
            if not is_J1_V1['fee_taker'].values[0] == 'NULL':
                J1_V1_fee_ratio = is_J1_V1['fee_taker'].values[0]
            J1_V2_price_precision = 0
            J1_V2_price_step = 0
            J1_V2_size_precision = 0
            J1_V2_size_min = 0
            J1_V2_min_notional = 0
            J1_V2_fee_ratio = 0
            if not is_J1_V2['limit_price_precision'].values[0] == 'NULL':
                J1_V2_price_precision = is_J1_V2[
                    'limit_price_precision'].values[0]
            if not is_J1_V2['limit_price_step'].values[0] == 'NULL':
                J1_V2_price_step = is_J1_V2['limit_price_step'].values[0]
            if not is_J1_V2['limit_size_precision'].values[0] == 'NULL':
                J1_V2_size_precision = is_J1_V2['limit_size_precision'].values[
                    0]
            if not is_J1_V2['limit_size_min'].values[0] == 'NULL':
                J1_V2_size_min = is_J1_V2['limit_size_min'].values[0]
            if not is_J1_V2['limit_min_notional'].values[0] == 'NULL':
                J1_V2_min_notional = is_J1_V2['limit_min_notional'].values[0]
            if not is_J1_V2['fee_taker'].values[0] == 'NULL':
                J1_V2_fee_ratio = is_J1_V2['fee_taker'].values[0]
            J1_V3_price_precision = 0
            J1_V3_price_step = 0
            J1_V3_size_precision = 0
            J1_V3_size_min = 0
            J1_V3_min_notional = 0
            J1_V3_fee_ratio = 0
            if not is_J1_V3['limit_price_precision'].values[0] == 'NULL':
                J1_V3_price_precision = is_J1_V3[
                    'limit_price_precision'].values[0]
            if not is_J1_V3['limit_price_step'].values[0] == 'NULL':
                J1_V3_price_step = is_J1_V3['limit_price_step'].values[0]
            if not is_J1_V3['limit_size_precision'].values[0] == 'NULL':
                J1_V3_size_precision = is_J1_V3['limit_size_precision'].values[
                    0]
            if not is_J1_V3['limit_size_min'].values[0] == 'NULL':
                J1_V3_size_min = is_J1_V3['limit_size_min'].values[0]
            if not is_J1_V3['limit_min_notional'].values[0] == 'NULL':
                J1_V3_min_notional = is_J1_V3['limit_min_notional'].values[0]
            if not is_J1_V3['fee_taker'].values[0] == 'NULL':
                J1_V3_fee_ratio = is_J1_V3['fee_taker'].values[0]
            J2_V1_price_precision = 0
            J2_V1_price_step = 0
            J2_V1_size_precision = 0
            J2_V1_size_min = 0
            J2_V1_min_notional = 0
            J2_V1_fee_ratio = 0
            if not is_J2_V1['limit_price_precision'].values[0] == 'NULL':
                J2_V1_price_precision = is_J2_V1[
                    'limit_price_precision'].values[0]
            if not is_J2_V1['limit_price_step'].values[0] == 'NULL':
                J2_V1_price_step = is_J2_V1['limit_price_step'].values[0]
            if not is_J2_V1['limit_size_precision'].values[0] == 'NULL':
                J2_V1_size_precision = is_J2_V1['limit_size_precision'].values[
                    0]
            if not is_J2_V1['limit_size_min'].values[0] == 'NULL':
                J2_V1_size_min = is_J2_V1['limit_size_min'].values[0]
            if not is_J2_V1['limit_min_notional'].values[0] == 'NULL':
                J2_V1_min_notional = is_J2_V1['limit_min_notional'].values[0]
            if not is_J2_V1['fee_taker'].values[0] == 'NULL':
                J2_V1_fee_ratio = is_J2_V1['fee_taker'].values[0]
            J2_V2_price_precision = 0
            J2_V2_price_step = 0
            J2_V2_size_precision = 0
            J2_V2_size_min = 0
            J2_V2_min_notional = 0
            J2_V2_fee_ratio = 0
            if not is_J2_V2['limit_price_precision'].values[0] == 'NULL':
                J2_V2_price_precision = is_J2_V2[
                    'limit_price_precision'].values[0]
            if not is_J2_V2['limit_price_step'].values[0] == 'NULL':
                J2_V2_price_step = is_J2_V2['limit_price_step'].values[0]
            if not is_J2_V2['limit_size_precision'].values[0] == 'NULL':
                J2_V2_size_precision = is_J2_V2['limit_size_precision'].values[
                    0]
            if not is_J2_V2['limit_size_min'].values[0] == 'NULL':
                J2_V2_size_min = is_J2_V2['limit_size_min'].values[0]
            if not is_J2_V2['limit_min_notional'].values[0] == 'NULL':
                J2_V2_min_notional = is_J2_V2['limit_min_notional'].values[0]
            if not is_J2_V2['fee_taker'].values[0] == 'NULL':
                J2_V2_fee_ratio = is_J2_V2['fee_taker'].values[0]
            J2_V3_price_precision = 0
            J2_V3_price_step = 0
            J2_V3_size_precision = 0
            J2_V3_size_min = 0
            J2_V3_min_notional = 0
            J2_V3_fee_ratio = 0
            if not is_J2_V3['limit_price_precision'].values[0] == 'NULL':
                J2_V3_price_precision = is_J2_V3[
                    'limit_price_precision'].values[0]
            if not is_J2_V3['limit_price_step'].values[0] == 'NULL':
                J2_V3_price_step = is_J2_V3['limit_price_step'].values[0]
            if not is_J2_V3['limit_size_precision'].values[0] == 'NULL':
                J2_V3_size_precision = is_J2_V3['limit_size_precision'].values[
                    0]
            if not is_J2_V3['limit_size_min'].values[0] == 'NULL':
                J2_V3_size_min = is_J2_V3['limit_size_min'].values[0]
            if not is_J2_V3['limit_min_notional'].values[0] == 'NULL':
                J2_V3_min_notional = is_J2_V3['limit_min_notional'].values[0]
            if not is_J2_V3['fee_taker'].values[0] == 'NULL':
                J2_V3_fee_ratio = is_J2_V3['fee_taker'].values[0]
            # aggDepth
            V1_aggDepth = max(J1_V1_price_step, J2_V1_price_step)
            V2_aggDepth = max(J1_V2_price_step, J2_V2_price_step)
            V3_aggDepth = max(J1_V3_price_step, J2_V3_price_step)
            # calc common symbol
            C1_symbol = [
                i for i in [V1_fSymbol, V1_tSymbol]
                if i in [V3_fSymbol, V3_tSymbol]
            ][0]
            C2_symbol = [
                i for i in [V1_fSymbol, V1_tSymbol]
                if i in [V2_fSymbol, V2_tSymbol]
            ][0]
            C3_symbol = [
                i for i in [V2_fSymbol, V2_tSymbol]
                if i in [V3_fSymbol, V3_tSymbol]
            ][0]
            # calc balance
            J1_C1_symbol_balance = 0
            J1_C2_symbol_balance = 0
            J1_C3_symbol_balance = 0
            J2_C1_symbol_balance = 0
            J2_C2_symbol_balance = 0
            J2_C3_symbol_balance = 0
            for sa in status_assets:
                if sa['server'] == J1_server:
                    if sa['asset'] == C1_symbol:
                        J1_C1_symbol_balance = sa['free']
                    if sa['asset'] == C2_symbol:
                        J1_C2_symbol_balance = sa['free']
                    if sa['asset'] == C3_symbol:
                        J1_C3_symbol_balance = sa['free']
                if sa['server'] == J2_server:
                    if sa['asset'] == C1_symbol:
                        J2_C1_symbol_balance = sa['free']
                    if sa['asset'] == C2_symbol:
                        J2_C2_symbol_balance = sa['free']
                    if sa['asset'] == C3_symbol:
                        J2_C3_symbol_balance = sa['free']
            # print('J1_C1_symbol=%s, J1_C1_symbol_balance=%s' % (C1_symbol, J1_C1_symbol_balance))
            # print('J1_C2_symbol=%s, J1_C2_symbol_balance=%s' % (C2_symbol, J1_C2_symbol_balance))
            # print('J1_C3_symbol=%s, J1_C3_symbol_balance=%s' % (C3_symbol, J1_C3_symbol_balance))
            # print('J2_C1_symbol=%s, J2_C1_symbol_balance=%s' % (C1_symbol, J2_C1_symbol_balance))
            # print('J2_C2_symbol=%s, J2_C2_symbol_balance=%s' % (C2_symbol, J2_C2_symbol_balance))
            # print('J2_C3_symbol=%s, J2_C3_symbol_balance=%s' % (C3_symbol, J2_C3_symbol_balance))
            # server market order book ticker
            if J1_server == self._Okex_exchange:
                J1_V1_res = self._Okex.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                J1_V2_res = self._Okex.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                J1_V3_res = self._Okex.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            if J1_server == self._Binance_exchange:
                J1_V1_res = self._Binance.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                J1_V2_res = self._Binance.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                J1_V3_res = self._Binance.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            if J1_server == self._Huobi_exchange:
                J1_V1_res = self._Huobi.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                J1_V2_res = self._Huobi.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                J1_V3_res = self._Huobi.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            if J2_server == self._Okex_exchange:
                J2_V1_res = self._Okex.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                J2_V2_res = self._Okex.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                J2_V3_res = self._Okex.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            if J2_server == self._Binance_exchange:
                J2_V1_res = self._Binance.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                J2_V2_res = self._Binance.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                J2_V3_res = self._Binance.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            if J2_server == self._Huobi_exchange:
                J2_V1_res = self._Huobi.getMarketOrderbookTicker(
                    V1_fSymbol, V1_tSymbol, V1_aggDepth)
                J2_V2_res = self._Huobi.getMarketOrderbookTicker(
                    V2_fSymbol, V2_tSymbol, V2_aggDepth)
                J2_V3_res = self._Huobi.getMarketOrderbookTicker(
                    V3_fSymbol, V3_tSymbol, V3_aggDepth)
            # print('J1_V1_res=%s' % J1_V1_res)
            # print('J1_V2_res=%s' % J1_V2_res)
            # print('J1_V3_res=%s' % J1_V3_res)
            # print('J2_V1_res=%s' % J2_V1_res)
            # print('J2_V2_res=%s' % J2_V2_res)
            # print('J2_V3_res=%s' % J2_V3_res)
            # calc type tra price and size
            # calc J1_V1, J2_V1
            if C1_symbol == V1_fSymbol:  # fSymbol -> tSymbol
                J1_V1_one_price = float(J1_V1_res['bid_one_price'])
                J1_V1_one_side = CCAT_ORDER_SIDE_SELL
                J1_V1_one_size = float(J1_V1_res['bid_one_size'])
                J1_V1_one_size = min(J1_V1_one_size, J1_C1_symbol_balance)
                J2_V1_one_price = float(J2_V1_res['ask_one_price'])
                J2_V1_one_side = CCAT_ORDER_SIDE_BUY
                J2_V1_one_size = float(J2_V1_res['ask_one_size'])
                J2_V1_one_size = min(J2_V1_one_size, J2_C1_symbol_balance)
            else:  # tSymbol -> fSymbol
                J1_V1_one_price = float(J1_V1_res['ask_one_price'])
                J1_V1_one_side = CCAT_ORDER_SIDE_BUY
                J1_V1_one_size = float(J1_V1_res['ask_one_size'])
                J1_V1_one_size = min(J1_V1_one_size,
                                     J1_C1_symbol_balance / J1_V1_one_price)
                J2_V1_one_price = float(J1_V1_res['bid_one_price'])
                J2_V1_one_side = CCAT_ORDER_SIDE_SELL
                J2_V1_one_size = float(J1_V1_res['bid_one_size'])
                J2_V1_one_size = min(J2_V1_one_size,
                                     J2_C1_symbol_balance / J2_V1_one_price)
            # calc J1_V2, J2_V2
            if C2_symbol == V2_fSymbol:  # fSymbol -> tSymbol
                J1_V2_one_price = float(J1_V2_res['bid_one_price'])
                J1_V2_one_side = CCAT_ORDER_SIDE_SELL
                J1_V2_one_size = float(J1_V2_res['bid_one_size'])
                J1_V2_one_size = min(J1_V2_one_size, J1_C2_symbol_balance)
                J2_V2_one_price = float(J2_V2_res['ask_one_price'])
                J2_V2_one_side = CCAT_ORDER_SIDE_BUY
                J2_V2_one_size = float(J2_V2_res['ask_one_size'])
                J2_V2_one_size = min(J2_V2_one_size, J2_C2_symbol_balance)
            else:  # tSymbol -> fSymbol
                J1_V2_one_price = float(J1_V2_res['ask_one_price'])
                J1_V2_one_side = CCAT_ORDER_SIDE_BUY
                J1_V2_one_size = float(J1_V2_res['ask_one_size'])
                J1_V2_one_size = min(J1_V2_one_size,
                                     J1_C2_symbol_balance / J1_V2_one_price)
                J2_V2_one_price = float(J2_V2_res['bid_one_price'])
                J2_V2_one_side = CCAT_ORDER_SIDE_SELL
                J2_V2_one_size = float(J2_V2_res['bid_one_size'])
                J2_V2_one_size = min(J2_V2_one_size,
                                     J2_C2_symbol_balance / J2_V2_one_price)
            # calc V3
            if C3_symbol == V3_fSymbol:  # fSymbol -> tSymbol
                J1_V3_one_price = float(J1_V3_res['bid_one_price'])
                J1_V3_one_side = CCAT_ORDER_SIDE_SELL
                J1_V3_one_size = float(J1_V3_res['bid_one_size'])
                J1_V3_one_size = min(J1_V3_one_size, J1_C3_symbol_balance)
                J2_V3_one_price = float(J2_V3_res['ask_one_price'])
                J2_V3_one_side = CCAT_ORDER_SIDE_BUY
                J2_V3_one_size = float(J2_V3_res['ask_one_size'])
                J2_V3_one_size = min(J2_V3_one_size, J2_C3_symbol_balance)
            else:  # tSymbol -> fSymbol
                J1_V3_one_price = float(J1_V3_res['ask_one_price'])
                J1_V3_one_side = CCAT_ORDER_SIDE_BUY
                J1_V3_one_size = float(J1_V3_res['ask_one_size'])
                J1_V3_one_size = min(J1_V3_one_size,
                                     J1_C3_symbol_balance / J1_V3_one_price)
                J2_V3_one_price = float(J2_V3_res['bid_one_price'])
                J2_V3_one_side = CCAT_ORDER_SIDE_SELL
                J2_V3_one_size = float(J2_V3_res['bid_one_size'])
                J2_V3_one_size = min(J2_V3_one_size,
                                     J2_C3_symbol_balance / J2_V3_one_price)
            # print('J1_V1_one_price=%s, J1_V1_one_size=%s' % (J1_V1_one_price, J1_V1_one_size))
            # print('J1_V2_one_price=%s, J1_V2_one_size=%s' % (J1_V2_one_price, J1_V2_one_size))
            # print('J1_V3_one_price=%s, J1_V3_one_size=%s' % (J1_V3_one_price, J1_V3_one_size))
            # print('J2_V1_one_price=%s, J2_V1_one_size=%s' % (J2_V1_one_price, J2_V1_one_size))
            # print('J2_V2_one_price=%s, J2_V2_one_size=%s' % (J2_V2_one_price, J2_V2_one_size))
            # print('J2_V3_one_price=%s, J2_V3_one_size=%s' % (J2_V3_one_price, J2_V3_one_size))
            # calc one price ratio
            if C3_symbol == V3_fSymbol:
                # Type J1 = clockwise, J2 = anti-clockwise
                # calc J1
                J1_C1_C2_one_price = J1_V1_one_price
                J1_C2_C3_one_price = 1 / J1_V2_one_price
                J1_C3_C1_one_price = J1_V3_one_price
                # calc J2
                J2_C1_C2_one_price = 1 / J2_V1_one_price
                J2_C2_C3_one_price = J2_V2_one_price
                J2_C3_C1_one_price = 1 / J2_V3_one_price
            else:
                # Type J1 = anti-clockwise, J2 = clockwise
                # calc J1
                J1_C1_C2_one_price = J1_V1_one_price
                J1_C2_C3_one_price = 1 / J1_V2_one_price
                J1_C3_C1_one_price = 1 / J1_V3_one_price
                # calc J2
                J2_C1_C2_one_price = 1 / J2_V1_one_price
                J2_C2_C3_one_price = J2_V2_one_price
                J2_C3_C1_one_price = J2_V3_one_price
            # print('J1_C1_C2_one_price=%s' % J1_C1_C2_one_price)
            # print('J1_C2_C3_one_price=%s' % J1_C2_C3_one_price)
            # print('J1_C3_C1_one_price=%s' % J1_C3_C1_one_price)
            # print('J2_C1_C2_one_price=%s' % J2_C1_C2_one_price)
            # print('J2_C2_C3_one_price=%s' % J2_C2_C3_one_price)
            # print('J2_C3_C1_one_price=%s' % J2_C3_C1_one_price)
            # calc tra result
            # if not J1_C1_C2_one_price * J1_C2_C3_one_price * J1_C3_C1_one_price > J2_C1_C2_one_price * J2_C2_C3_one_price * J2_C3_C1_one_price:
            #     # print('pair check result not exist, return')
            #     return orders
            # Begin Calc Gain: Gain V2 tSymbol
            if C3_symbol == V3_fSymbol:
                # Type J1 = clockwise: sell->buy->sell, J2 = anti-clockwise: sell->buy->buy
                # calc J1 symbol size
                temp_J1_C3 = min(
                    J1_V3_one_size,
                    J1_V2_one_size * J1_C2_C3_one_price
                    * (1 - J1_V2_fee_ratio))
                temp_J1_C1 = min(
                    J1_V1_one_size,
                    temp_J1_C3 * J1_C3_C1_one_price * (1 - J1_V3_fee_ratio))
                temp_J1_C3 = temp_J1_C1 / J1_C3_C1_one_price / (
                    1 - J1_V3_fee_ratio)
                temp_J1_C2 = temp_J1_C3 / J1_C2_C3_one_price / (
                    1 - J1_V2_fee_ratio)
                J1_V2_one_size = temp_J1_C2 * (
                    1 - J1_V2_fee_ratio) / J1_V2_one_price
                J1_V3_one_size = J1_V2_one_size
                J1_V1_one_size = J1_V3_one_size * J1_V3_one_price * (
                    1 - J1_V3_fee_ratio)
                # calc J2 symbol size
                temp_J2_C3 = min(
                    J2_V3_one_size,
                    J2_V2_one_size * J2_C2_C3_one_price
                    * (1 - J2_V2_fee_ratio))
                temp_J2_C1 = min(
                    J2_V1_one_size,
                    temp_J2_C3 * J2_C3_C1_one_price * (1 - J2_V3_fee_ratio))
                temp_J2_C3 = temp_J2_C1 / J2_C3_C1_one_price / (
                    1 - J2_V3_fee_ratio)
                temp_J2_C2 = temp_J2_C3 / J2_C2_C3_one_price / (
                    1 - J2_V2_fee_ratio)
                J2_V2_one_size = temp_J2_C2 * (
                    1 - J2_V2_fee_ratio) / J2_V2_one_price
                J2_V3_one_size = J2_V2_one_size * (
                    1 - J2_V3_fee_ratio) / J2_V3_one_price
                J2_V1_one_size = J2_V3_one_size
            else:
                # Type J1 = anti-clockwise: sell->buy->buy, J2 = clockwise: sell->buy->sell
                # calc J1 symbol size
                temp_J1_C3 = min(
                    J1_V3_one_size,
                    J1_V2_one_size * J1_C2_C3_one_price
                    * (1 - J1_V2_fee_ratio))
                temp_J1_C1 = min(
                    J1_V1_one_size,
                    temp_J1_C3 * J1_C3_C1_one_price * (1 - J1_V3_fee_ratio))
                temp_J1_C3 = temp_J1_C1 / J1_C3_C1_one_price / (
                    1 - J1_V3_fee_ratio)
                temp_J1_C2 = temp_J1_C3 / J1_C2_C3_one_price / (
                    1 - J1_V2_fee_ratio)
                J1_V2_one_size = temp_J1_C2 * (
                    1 - J1_V2_fee_ratio) / J1_V2_one_price
                J1_V3_one_size = J1_V2_one_size * (
                    1 - J1_V3_fee_ratio) / J1_V3_one_price
                J1_V1_one_size = J1_V3_one_size
                # calc J2 symbol size
                temp_J2_C3 = min(
                    J2_V3_one_size,
                    J2_V2_one_size * J2_C2_C3_one_price
                    * (1 - J2_V2_fee_ratio))
                temp_J2_C1 = min(
                    J2_V1_one_size,
                    temp_J2_C3 * J2_C3_C1_one_price * (1 - J2_V3_fee_ratio))
                temp_J2_C3 = temp_J2_C1 / J2_C3_C1_one_price / (
                    1 - J2_V3_fee_ratio)
                temp_J2_C2 = temp_J2_C3 / J2_C2_C3_one_price / (
                    1 - J2_V2_fee_ratio)
                J2_V2_one_size = temp_J2_C2 * (
                    1 - J2_V2_fee_ratio) / J2_V2_one_price
                J2_V3_one_size = J2_V2_one_size
                J2_V1_one_size = J2_V3_one_size * J2_V3_one_price * (
                    1 - J2_V3_fee_ratio)
            # calc symbol size
            J1_V1_one_size = min(J1_V1_one_size, J2_V1_one_size)
            J1_V2_one_size = min(J1_V2_one_size, J2_V2_one_size)
            J1_V3_one_size = min(J1_V3_one_size, J2_V3_one_size)
            J2_V1_one_size = min(J1_V1_one_size, J2_V1_one_size)
            J2_V2_one_size = min(J1_V2_one_size, J2_V2_one_size)
            J2_V3_one_size = min(J1_V3_one_size, J2_V3_one_size)
            # Begin Calc Gain
            C1_symbol_gain_ratio_up = (J1_V1_one_price - J2_V1_one_price
                                       - J1_V1_one_price * J1_V1_fee_ratio
                                       - J2_V1_one_price * J2_V1_fee_ratio) * (
                                           J1_V1_one_size + J2_V1_one_size) / 2
            C1_symbol_gain_ratio_dn = J2_V1_one_price * (
                J1_V1_one_size + J2_V1_one_size) / 2
            C2_symbol_gain_ratio_up = (J1_V2_one_price - J2_V2_one_price
                                       - J1_V2_one_price * J1_V2_fee_ratio
                                       - J2_V2_one_price * J2_V2_fee_ratio) * (
                                           J1_V2_one_size + J2_V2_one_size) / 2
            C2_symbol_gain_ratio_dn = J2_V2_one_price * (
                J1_V2_one_size + J2_V2_one_size) / 2
            C3_symbol_gain_ratio_up = (J1_V3_one_price - J2_V3_one_price
                                       - J1_V3_one_price * J1_V3_fee_ratio
                                       - J2_V3_one_price * J2_V3_fee_ratio) * (
                                           J1_V3_one_size + J2_V3_one_size) / 2
            C3_symbol_gain_ratio_dn = J2_V3_one_price * (
                J1_V3_one_size + J2_V3_one_size) / 2
            # calc gain_ratio
            gain_ratio = (C1_symbol_gain_ratio_up + C2_symbol_gain_ratio_up
                          + C3_symbol_gain_ratio_up) / (
                              C1_symbol_gain_ratio_dn + C2_symbol_gain_ratio_dn +
                              C3_symbol_gain_ratio_dn)
            # forward
            # print('pair froward gain_ratio: %s' % gain_ratio)
            if gain_ratio > forward_ratio:
                # print('pair forward J1_C1_symbol_balance: %s' % J1_C1_symbol_balance)
                # print('pair forward J1_C2_symbol_balance: %s' % J1_C2_symbol_balance)
                # print('pair forward J1_C3_symbol_balance: %s' % J1_C3_symbol_balance)
                # print('pair forward J1_V1_one_price: %s' % J1_V1_one_price)
                # print('pair forward J1_V2_one_price: %s' % J1_V2_one_price)
                # print('pair forward J1_V3_one_price: %s' % J1_V3_one_price)
                # print('pair forward J1_V1_one_size: %s' % J1_V1_one_size)
                # print('pair forward J1_V2_one_size: %s' % J1_V2_one_size)
                # print('pair forward J1_V3_one_size: %s' % J1_V3_one_size)
                # print('pair forward J1_V1_one_side: %s' % J1_V1_one_side)
                # print('pair forward J1_V2_one_side: %s' % J1_V2_one_side)
                # print('pair forward J1_V3_one_side: %s' % J1_V3_one_side)
                # print('pair forward J1_V1_size_min: %s' % J1_V1_size_min)
                # print('pair forward J1_V2_size_min: %s' % J1_V2_size_min)
                # print('pair forward J1_V3_size_min: %s' % J1_V3_size_min)
                # print('pair forward J1_V1_min_notional: %s' % J1_V1_min_notional)
                # print('pair forward J1_V2_min_notional: %s' % J1_V2_min_notional)
                # print('pair forward J1_V3_min_notional: %s' % J1_V3_min_notional)
                # print('pair forward J2_C1_symbol_balance: %s' % J2_C1_symbol_balance)
                # print('pair forward J2_C2_symbol_balance: %s' % J2_C2_symbol_balance)
                # print('pair forward J2_C3_symbol_balance: %s' % J2_C3_symbol_balance)
                # print('pair forward J2_V1_one_price: %s' % J2_V1_one_price)
                # print('pair forward J2_V2_one_price: %s' % J2_V2_one_price)
                # print('pair forward J2_V3_one_price: %s' % J2_V3_one_price)
                # print('pair forward J2_V1_one_size: %s' % J2_V1_one_size)
                # print('pair forward J2_V2_one_size: %s' % J2_V2_one_size)
                # print('pair forward J2_V3_one_size: %s' % J2_V3_one_size)
                # print('pair forward J2_V1_one_side: %s' % J2_V1_one_side)
                # print('pair forward J2_V2_one_side: %s' % J2_V2_one_side)
                # print('pair forward J2_V3_one_side: %s' % J2_V3_one_side)
                # print('pair forward J2_V1_size_min: %s' % J2_V1_size_min)
                # print('pair forward J2_V2_size_min: %s' % J2_V2_size_min)
                # print('pair forward J2_V3_size_min: %s' % J2_V3_size_min)
                # print('pair forward J2_V1_min_notional: %s' % J2_V1_min_notional)
                # print('pair forward J2_V2_min_notional: %s' % J2_V2_min_notional)
                # print('pair forward J2_V3_min_notional: %s' % J2_V3_min_notional)
                if J1_V1_one_size > 0 and J1_V2_one_size > 0 and J1_V3_one_size > 0 and J2_V1_one_size > 0 and J2_V2_one_size > 0 and J2_V3_one_size > 0:
                    if J1_V1_one_size >= J1_V1_size_min and J1_V2_one_size >= J1_V2_size_min and J1_V3_one_size >= J1_V3_size_min and J2_V1_one_size >= J2_V1_size_min and J2_V2_one_size >= J2_V2_size_min and J2_V3_one_size >= J2_V3_size_min:
                        if J1_V1_one_price * J1_V1_one_size >= J1_V1_min_notional and J1_V2_one_price * J1_V2_one_size >= J1_V2_min_notional and J1_V3_one_price * J1_V3_one_size >= J1_V3_min_notional and J2_V1_one_price * J2_V1_one_size >= J2_V1_min_notional and J2_V2_one_price * J2_V2_one_size >= J2_V2_min_notional and J2_V3_one_price * J2_V3_one_size >= J2_V3_min_notional:
                            # print('pair forward result exist: add orders')
                            price = num_to_precision(
                                J1_V1_one_price,
                                J1_V1_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                J1_V1_one_size,
                                J1_V1_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": J1_server,
                                "fSymbol": V1_fSymbol,
                                "tSymbol": V1_tSymbol,
                                "ask_or_bid": J1_V1_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": J1_V1_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                J1_V2_one_price,
                                J1_V2_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                J1_V2_one_size,
                                J1_V2_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": J1_server,
                                "fSymbol": V2_fSymbol,
                                "tSymbol": V2_tSymbol,
                                "ask_or_bid": J1_V2_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": J1_V2_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                J1_V3_one_price,
                                J1_V3_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                J1_V3_one_size,
                                J1_V3_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": J1_server,
                                "fSymbol": V3_fSymbol,
                                "tSymbol": V3_tSymbol,
                                "ask_or_bid": J1_V3_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": J1_V3_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                J2_V1_one_price,
                                J2_V1_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                J2_V1_one_size,
                                J2_V1_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": J2_server,
                                "fSymbol": V1_fSymbol,
                                "tSymbol": V1_tSymbol,
                                "ask_or_bid": J2_V1_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": J2_V1_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                J2_V2_one_price,
                                J2_V2_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                J2_V2_one_size,
                                J2_V2_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": J2_server,
                                "fSymbol": V2_fSymbol,
                                "tSymbol": V2_tSymbol,
                                "ask_or_bid": J2_V2_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": J2_V2_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                            price = num_to_precision(
                                J2_V3_one_price,
                                J2_V3_price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                J2_V3_one_size,
                                J2_V3_size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": J2_server,
                                "fSymbol": V3_fSymbol,
                                "tSymbol": V3_tSymbol,
                                "ask_or_bid": J2_V3_one_side,
                                "price": price,
                                "quantity": quantity,
                                "ratio": J2_V3_fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
            # return
            return orders
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolRunTradeOrdersTypePair: exception err=%s" % err
            raise CalcException(errStr)

    def _calcSymbolAfterTradeOrders(self, server, fSymbol, tSymbol,
                                    fSymbol_to_base, tSymbol_to_base, group_id,
                                    resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc._calcSymbolAfterTradeOrders:")
        try:
            orders = []
            # type I
            # handle fSymbol
            if fSymbol_to_base > 0:
                # print('in type I')
                # de: direct trans
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server)
                                     & (resInfoSymbol['fSymbol'] == fSymbol)
                                     & (resInfoSymbol['tSymbol'] == baseCoin)]
                if not isDe.empty:
                    # print('in Type I: de')
                    # fSymbol -> baseCoin
                    price_precision = 0
                    size_precision = 0
                    size_min = 0
                    min_notional = 0
                    fee_ratio = 0
                    if not isDe['limit_price_precision'].values[0] == 'NULL':
                        price_precision = isDe['limit_price_precision'].values[
                            0]
                    if not isDe['limit_size_precision'].values[0] == 'NULL':
                        size_precision = isDe['limit_size_precision'].values[0]
                    if not isDe['limit_size_min'].values[0] == 'NULL':
                        size_min = isDe['limit_size_min'].values[0]
                    if not isDe['limit_min_notional'].values[0] == 'NULL':
                        min_notional = isDe['limit_min_notional'].values[0]
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if server == self._Okex_exchange:
                        res = self._Okex.getMarketOrderbookDepth(
                            fSymbol, baseCoin)
                    if server == self._Binance_exchange:
                        res = self._Binance.getMarketOrderbookDepth(
                            fSymbol, baseCoin)
                    if server == self._Huobi_exchange:
                        res = self._Huobi.getMarketOrderbookDepth(
                            fSymbol, baseCoin)
                    # calc orders
                    deTradeSize = fSymbol_to_base
                    deTradeNotional = fSymbol_to_base * float(
                        res['bid_price_size'][0][0])
                    # print('in Type I: de, deTradeSize=%s, size_min=%s' % (deTradeSize, size_min))
                    # print('in Type I: de, deTradeNotional=%s, min_notional=%s' % (deTradeNotional, min_notional))
                    if deTradeNotional < min_notional - CALC_ZERO_NUMBER or deTradeSize < size_min - CALC_ZERO_NUMBER:
                        self._logger.warn(
                            "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                            % (server, fSymbol, baseCoin, deTradeSize))
                    else:
                        sum = 0
                        deTrade = []
                        for r in res['bid_price_size'][
                                0:10]:  # bid 1 to bid 10, no more
                            if not sum < deTradeSize:
                                break
                            rPrice = float(r[0])
                            rSize = float(r[1])
                            deSize = min(deTradeSize - sum, rSize)
                            if deSize > 0:
                                if deSize >= size_min:
                                    if not deSize * rPrice >= min_notional:
                                        continue
                                    sum = sum + deSize
                                    if sum <= deTradeSize + CALC_ZERO_NUMBER:
                                        deTrade.append({
                                            'price': rPrice,
                                            'size': deSize
                                        })
                        # print('in Type I: de, server=%s, res=%s' % (server, res['bid_price_size'][0:10]))
                        # print('in Type I: de, deTradeSize=%s' % deTradeSize)
                        # print('in Type I: de, sum=%s' % sum)
                        if sum < deTradeSize - CALC_ZERO_NUMBER:
                            raise Exception(
                                "TRANS TOO MUCH ERROR，amount is not enough with bid 1 to bid 10: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, fSymbol, baseCoin, deTradeSize))
                        for trade in deTrade:
                            price = num_to_precision(
                                trade['price'],
                                price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": fSymbol,
                                "tSymbol": baseCoin,
                                "ask_or_bid": CCAT_ORDER_SIDE_SELL,
                                "price": price,
                                "quantity": quantity,
                                "ratio": fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                    # type I: de done
                    # print('out type I: de done')
                # tra: trangle trans
                if isDe.empty:
                    # print('in type I: tra')
                    isDe = resInfoSymbol[
                        (resInfoSymbol['server'] == server) &
                        (resInfoSymbol['fSymbol'] == tSymbol) &
                        (resInfoSymbol['tSymbol'] == baseCoin)]
                    isTra = resInfoSymbol[
                        (resInfoSymbol['server'] == server)
                        & (resInfoSymbol['fSymbol'] == fSymbol)
                        & (resInfoSymbol['tSymbol'] == tSymbol)]
                    if isDe.empty or isTra.empty:
                        raise Exception(
                            "TRADE PAIRS NOT FOUND ERROR, tSymbol to fSymbol trade pairs not found."
                        )
                    if not isTra.empty:
                        # fSymbol -> tSymbol
                        price_precision = 0
                        size_precision = 0
                        size_min = 0
                        min_notional = 0
                        fee_ratio = 0
                        if not isTra['limit_price_precision'].values[
                                0] == 'NULL':
                            price_precision = isTra[
                                'limit_price_precision'].values[0]
                        if not isTra['limit_size_precision'].values[
                                0] == 'NULL':
                            size_precision = isTra[
                                'limit_size_precision'].values[0]
                        if not isTra['limit_size_min'].values[0] == 'NULL':
                            size_min = isTra['limit_size_min'].values[0]
                        if not isTra['limit_min_notional'].values[0] == 'NULL':
                            min_notional = isTra['limit_min_notional'].values[
                                0]
                        if not isTra['fee_taker'].values[0] == 'NULL':
                            fee_ratio = isTra['fee_taker'].values[0]
                        if server == self._Okex_exchange:
                            res = self._Okex.getMarketOrderbookDepth(
                                fSymbol, tSymbol)
                        if server == self._Binance_exchange:
                            res = self._Binance.getMarketOrderbookDepth(
                                fSymbol, tSymbol)
                        if server == self._Huobi_exchange:
                            res = self._Huobi.getMarketOrderbookDepth(
                                fSymbol, tSymbol)
                        # calc orders
                        traTradeSize = fSymbol_to_base
                        traTradeNotional = fSymbol_to_base * float(
                            res['bid_price_size'][0][0])
                        # print('in type I: tra, traTradeSize=%s, size_min=%s' % (traTradeSize, size_min))
                        # print('in type I: tra, traTradeNotional=%s, min_notional=%s' % (traTradeNotional, min_notional))
                        if traTradeNotional < min_notional - CALC_ZERO_NUMBER or traTradeSize < size_min - CALC_ZERO_NUMBER:
                            self._logger.warn(
                                "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, fSymbol, tSymbol, traTradeSize))
                        else:
                            sum = 0
                            traTrade = []
                            for r in res['bid_price_size'][
                                    0:10]:  # bid 1 to bid 10, no more
                                if not sum < traTradeSize:
                                    break
                                rPrice = float(r[0])
                                rSize = float(r[1])
                                traSize = min(traTradeSize - sum, rSize)
                                if traSize > 0:
                                    if traSize >= size_min:
                                        if not traSize * rPrice >= min_notional:
                                            continue
                                        sum = sum + traSize
                                        if sum <= traTradeSize + CALC_ZERO_NUMBER:
                                            traTrade.append({
                                                'price': rPrice,
                                                'size': traSize
                                            })
                            # print('in type I: tra, server=%s, res=%s' % (server, res['bid_price_size'][0:10]))
                            # print('in type I: tra, traTradeSize=%s' % traTradeSize)
                            # print('in type I: tra, sum=%s' % sum)
                            if sum < traTradeSize - CALC_ZERO_NUMBER:
                                raise Exception(
                                    "TRANS TOO MUCH ERROR，amount is not enough with bid 1 to bid 10: {server=%s, trade=(%s -> %s), amount=%s}"
                                    % (server, fSymbol, tSymbol, traTradeSize))
                            for trade in traTrade:
                                price = num_to_precision(
                                    trade['price'],
                                    price_precision,
                                    rounding=ROUND_DOWN)
                                quantity = num_to_precision(
                                    trade['size'],
                                    size_precision,
                                    rounding=ROUND_DOWN)
                                orders.append({
                                    "server":
                                    server,
                                    "fSymbol":
                                    fSymbol,
                                    "tSymbol":
                                    tSymbol,
                                    "ask_or_bid":
                                    CCAT_ORDER_SIDE_SELL,
                                    "price":
                                    price,
                                    "quantity":
                                    quantity,
                                    "ratio":
                                    fee_ratio,
                                    "type":
                                    CCAT_ORDER_TYPE_LIMIT,
                                    "group_id":
                                    group_id
                                })
                            # tSymbol -> baseCoin
                            # print('in type I: tra, traTrade=%s' % traTrade)
                            sum_base = 0
                            for trade in traTrade:
                                price = num_to_precision(
                                    trade['price'],
                                    price_precision,
                                    rounding=ROUND_DOWN)
                                quantity = num_to_precision(
                                    trade['size'],
                                    size_precision,
                                    rounding=ROUND_DOWN)
                                sum_base = sum_base + float(price) * float(
                                    quantity) * (1 - fee_ratio)
                            price_precision = 0
                            size_precision = 0
                            size_min = 0
                            min_notional = 0
                            fee_ratio = 0
                            if not isDe['limit_price_precision'].values[
                                    0] == 'NULL':
                                price_precision = isDe[
                                    'limit_price_precision'].values[0]
                            if not isDe['limit_size_precision'].values[
                                    0] == 'NULL':
                                size_precision = isDe[
                                    'limit_size_precision'].values[0]
                            if not isDe['limit_size_min'].values[0] == 'NULL':
                                size_min = isDe['limit_size_min'].values[0]
                            if not isDe['limit_min_notional'].values[
                                    0] == 'NULL':
                                min_notional = isDe[
                                    'limit_min_notional'].values[0]
                            if not isDe['fee_taker'].values[0] == 'NULL':
                                fee_ratio = isDe['fee_taker'].values[0]
                            if server == self._Okex_exchange:
                                res = self._Okex.getMarketOrderbookDepth(
                                    tSymbol, baseCoin)
                            if server == self._Binance_exchange:
                                res = self._Binance.getMarketOrderbookDepth(
                                    tSymbol, baseCoin)
                            if server == self._Huobi_exchange:
                                res = self._Huobi.getMarketOrderbookDepth(
                                    tSymbol, baseCoin)
                            # calc orders
                            deTradeSize = sum_base
                            deTradeNotional = sum_base * float(
                                res['bid_price_size'][0][0])
                            # print('in type I: tra, deTradeNotional=%s, min_notional=%s' % (deTradeNotional, min_notional))
                            # print('in type I: tra, deTradeSize=%s, size_min=%s' % (deTradeSize, size_min))
                            if deTradeNotional < min_notional - CALC_ZERO_NUMBER or deTradeSize < size_min - CALC_ZERO_NUMBER:
                                self._logger.warn(
                                    "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                                    % (server, tSymbol, baseCoin, deTradeSize))
                            else:
                                sum = 0
                                deTrade = []
                                for r in res['bid_price_size'][
                                        0:10]:  # bid 1 to bid 10, no more
                                    if not sum < deTradeNotional:
                                        break
                                    rPrice = float(r[0])
                                    rSize = float(r[1])
                                    deSize = min(deTradeSize - sum, rSize)
                                    if deSize > 0:
                                        if deSize >= size_min:
                                            if not deSize * rPrice >= min_notional:
                                                continue
                                            sum = sum + deSize
                                            if sum <= deTradeSize + CALC_ZERO_NUMBER:
                                                deTrade.append({
                                                    'price':
                                                    rPrice,
                                                    'size':
                                                    deSize
                                                })
                                # print('in type I: tra, server=%s, res=%s' % (server, res['bid_price_size'][0:10]))
                                # print('in type I: tra, deTradeSize=%s' % deTradeSize)
                                # print('in type I: tra, sum=%s' % sum)
                                if sum < deTradeSize - CALC_ZERO_NUMBER:
                                    raise Exception(
                                        "TRANS TOO MUCH ERROR，amount is not enough with bid 1 to bid 10: {server=%s, trade=(%s -> %s), amount=%s}"
                                        % (server, tSymbol, baseCoin,
                                           deTradeSize))
                                for trade in deTrade:
                                    price = num_to_precision(
                                        trade['price'],
                                        price_precision,
                                        rounding=ROUND_DOWN)
                                    quantity = num_to_precision(
                                        trade['size'],
                                        size_precision,
                                        rounding=ROUND_DOWN)
                                    orders.append({
                                        "server":
                                        server,
                                        "fSymbol":
                                        tSymbol,
                                        "tSymbol":
                                        baseCoin,
                                        "ask_or_bid":
                                        CCAT_ORDER_SIDE_SELL,
                                        "price":
                                        price,
                                        "quantity":
                                        quantity,
                                        "ratio":
                                        fee_ratio,
                                        "type":
                                        CCAT_ORDER_TYPE_LIMIT,
                                        "group_id":
                                        group_id
                                    })
                        # done type I: tra
                        # print('out type I: tra done')
            # type II
            # handle tSymbol
            if tSymbol_to_base > 0:
                # print('in type II')
                # need no trans
                if tSymbol == baseCoin:
                    # print('in type II: need no trans')
                    # done type II: need no trans
                    pass
                    # print('out type II: need no trans done')
                # direct trans
                isDe = resInfoSymbol[(resInfoSymbol['server'] == server)
                                     & (resInfoSymbol['fSymbol'] == tSymbol)
                                     & (resInfoSymbol['tSymbol'] == baseCoin)]
                if not isDe.empty:
                    # print('in type II: de')
                    # tSymbol -> baseCoin
                    price_precision = 0
                    size_precision = 0
                    size_min = 0
                    min_notional = 0
                    fee_ratio = 0
                    if not isDe['limit_price_precision'].values[0] == 'NULL':
                        price_precision = isDe['limit_price_precision'].values[
                            0]
                    if not isDe['limit_size_precision'].values[0] == 'NULL':
                        size_precision = isDe['limit_size_precision'].values[0]
                    if not isDe['limit_size_min'].values[0] == 'NULL':
                        size_min = isDe['limit_size_min'].values[0]
                    if not isDe['limit_min_notional'].values[0] == 'NULL':
                        min_notional = isDe['limit_min_notional'].values[0]
                    if not isDe['fee_taker'].values[0] == 'NULL':
                        fee_ratio = isDe['fee_taker'].values[0]
                    if server == self._Okex_exchange:
                        res = self._Okex.getMarketOrderbookDepth(
                            tSymbol, baseCoin)
                    if server == self._Binance_exchange:
                        res = self._Binance.getMarketOrderbookDepth(
                            tSymbol, baseCoin)
                    if server == self._Huobi_exchange:
                        res = self._Huobi.getMarketOrderbookDepth(
                            tSymbol, baseCoin)
                    # calc orders
                    # print('in type II: de, tSymbol_to_base=%s, fee_ratio=%s' % (tSymbol_to_base, fee_ratio))
                    deTradeSize = tSymbol_to_base
                    deTradeNotional = tSymbol_to_base * float(
                        res['bid_price_size'][0][0])
                    # print('in type II: de, deTradeSize=%s, size_min=%s' % (deTradeSize, size_min))
                    # print('in type II: de, deTradeNotional=%s, min_notional=%s' % (deTradeNotional, min_notional))
                    if deTradeNotional < min_notional - CALC_ZERO_NUMBER or deTradeSize < size_min - CALC_ZERO_NUMBER:
                        self._logger.warn(
                            "TRANS TOO SMALL ERROR, amount is smaller than the min limit: {server=%s, trade=(%s -> %s), amount=%s}"
                            % (server, tSymbol, baseCoin, deTradeSize))
                    else:
                        sum = 0
                        deTrade = []
                        for r in res['bid_price_size'][
                                0:10]:  # bid 1 to bid 10, no more
                            if not sum < deTradeSize:
                                break
                            rPrice = float(r[0])
                            rSize = float(r[1])
                            deSize = min(deTradeSize - sum, rSize)
                            if deSize > 0:
                                if deSize >= size_min:
                                    if not deSize * rPrice >= min_notional:
                                        continue
                                    sum = sum + deSize
                                    if sum <= deTradeSize + CALC_ZERO_NUMBER:
                                        deTrade.append({
                                            'price': rPrice,
                                            'size': deSize
                                        })
                        # print('in type II: de, server=%s, res=%s' % (server, res['bid_price_size'][0:10]))
                        # print('in type II: de, deTradeSize=%s' % deTradeSize)
                        # print('in type II: de, sum=%s' % sum)
                        if sum < deTradeSize - CALC_ZERO_NUMBER:
                            raise Exception(
                                "TRANS TOO MUCH ERROR，amount is not enough with bid 1 to bid 10: {server=%s, trade=(%s -> %s), amount=%s}"
                                % (server, tSymbol, baseCoin, deTradeSize))
                        for trade in deTrade:
                            price = num_to_precision(
                                trade['price'],
                                price_precision,
                                rounding=ROUND_DOWN)
                            quantity = num_to_precision(
                                trade['size'],
                                size_precision,
                                rounding=ROUND_DOWN)
                            orders.append({
                                "server": server,
                                "fSymbol": tSymbol,
                                "tSymbol": baseCoin,
                                "ask_or_bid": CCAT_ORDER_SIDE_SELL,
                                "price": price,
                                "quantity": quantity,
                                "ratio": fee_ratio,
                                "type": CCAT_ORDER_TYPE_LIMIT,
                                "group_id": group_id
                            })
                    # done type II: de
                    # print('out type II: de done')
            # return
            # print('return orders:%s' % orders)
            return orders
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc._calcSymbolAfterTradeOrders: exception err=%s" % err
            raise CalcException(errStr)

    def calcSignalPreTradeOrders(self, signal, resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalPreTradeOrders: {signal=%s, resInfoSymbol=%s, baseCoin=%s}"
            % (signal, 'resInfoSymbol', baseCoin))
        try:
            if not signal['base_start'] > 0:
                return []
            res = []
            # calc orders
            if signal['type'] == TYPE_DIS:
                orders = self._calcSymbolPreTradeOrders(
                    signal['bid_server'], signal['fSymbol'], signal['tSymbol'],
                    signal['base_start'] / 2, 0, signal['group_id'],
                    resInfoSymbol, baseCoin)
                if not orders == []:
                    res.extend(orders)
                orders = self._calcSymbolPreTradeOrders(
                    signal['ask_server'], signal['fSymbol'], signal['tSymbol'],
                    0, signal['base_start'] / 2, signal['group_id'],
                    resInfoSymbol, baseCoin)
                if not orders == []:
                    res.extend(orders)
            if signal['type'] == TYPE_TRA:
                # find target unique tSymbol
                C1_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                C2_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                ][0]
                C3_symbol = [
                    i for i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                if C1_symbol == signal['V1_fSymbol']:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['base_start'] / 3, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], 0, signal['base_start'] / 3,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C2_symbol == signal['V2_fSymbol']:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['base_start'] / 3, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], 0, signal['base_start'] / 3,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C3_symbol == signal['V3_fSymbol']:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['base_start'] / 3, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], 0, signal['base_start'] / 3,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
            if signal['type'] == TYPE_PAIR:
                # find target unique tSymbol
                C1_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                C2_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                ][0]
                C3_symbol = [
                    i for i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                if C1_symbol == signal['V1_fSymbol']:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J1_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['base_start'] / 6, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J2_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['base_start'] / 6, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J1_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], 0, signal['base_start'] / 6,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J2_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], 0, signal['base_start'] / 6,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C2_symbol == signal['V2_fSymbol']:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J1_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['base_start'] / 6, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J2_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['base_start'] / 6, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J1_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], 0, signal['base_start'] / 6,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J2_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], 0, signal['base_start'] / 6,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C3_symbol == signal['V3_fSymbol']:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J1_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['base_start'] / 6, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J2_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['base_start'] / 6, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J1_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], 0, signal['base_start'] / 6,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolPreTradeOrders(
                        signal['J2_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], 0, signal['base_start'] / 6,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
            # return
            return res
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcSignalPreTradeOrders: {signal=%s, resInfoSymbol=%s, baseCoin=%s}, exception err=%s" % (
                signal, 'resInfoSymbol', baseCoin, err)
            raise CalcException(errStr)

    def calcSignalRunTradeOrders(self, signal, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalRunTradeOrders: {signal=%s, resInfoSymbol=%s}"
            % (signal, 'resInfoSymbol'))
        try:
            res = []
            # calc orders
            if signal['type'] == TYPE_DIS:
                orders = self._calcSymbolRunTradeOrdersTypeDis(
                    signal['bid_server'], signal['ask_server'],
                    signal['fSymbol'], signal['tSymbol'],
                    signal['status_assets'], signal['forward_ratio'],
                    signal['backward_ratio'], signal['group_id'],
                    resInfoSymbol)
                if not orders == []:
                    res.extend(orders)
            if signal['type'] == TYPE_TRA:
                # find target unique tSymbol
                isV1 = (signal['V1_tSymbol'] != signal['V2_tSymbol'] and
                        signal['V1_tSymbol'] != signal['V3_tSymbol'])
                isV2 = (signal['V2_tSymbol'] != signal['V1_tSymbol'] and
                        signal['V2_tSymbol'] != signal['V3_tSymbol'])
                isV3 = (signal['V3_tSymbol'] != signal['V1_tSymbol'] and
                        signal['V3_tSymbol'] != signal['V2_tSymbol'])
                # print(isV1, isV2, isV3)
                if isV1:
                    orders = self._calcSymbolRunTradeOrdersTypeTra(
                        signal['server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['status_assets'],
                        signal['forward_ratio'], signal['group_id'],
                        resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolRunTradeOrdersTypeTra(
                        signal['server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['status_assets'],
                        signal['forward_ratio'], signal['group_id'],
                        resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                if isV2:
                    orders = self._calcSymbolRunTradeOrdersTypeTra(
                        signal['server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['status_assets'],
                        signal['forward_ratio'], signal['group_id'],
                        resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolRunTradeOrdersTypeTra(
                        signal['server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['status_assets'],
                        signal['forward_ratio'], signal['group_id'],
                        resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                if isV3:
                    orders = self._calcSymbolRunTradeOrdersTypeTra(
                        signal['server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['status_assets'],
                        signal['forward_ratio'], signal['group_id'],
                        resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolRunTradeOrdersTypeTra(
                        signal['server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], signal['status_assets'],
                        signal['forward_ratio'], signal['group_id'],
                        resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
            if signal['type'] == TYPE_PAIR:
                # find target unique tSymbol
                isV1 = (signal['V1_tSymbol'] != signal['V2_tSymbol'] and
                        signal['V1_tSymbol'] != signal['V3_tSymbol'])
                isV2 = (signal['V2_tSymbol'] != signal['V1_tSymbol'] and
                        signal['V2_tSymbol'] != signal['V3_tSymbol'])
                isV3 = (signal['V3_tSymbol'] != signal['V1_tSymbol'] and
                        signal['V3_tSymbol'] != signal['V2_tSymbol'])
                # print(isV1, isV2, isV3)
                if isV1:
                    orders = self._calcSymbolRunTradeOrdersTypePair(
                        signal['J1_server'], signal['J2_server'],
                        signal['V2_fSymbol'], signal['V2_tSymbol'],
                        signal['V3_fSymbol'], signal['V3_tSymbol'],
                        signal['V1_fSymbol'], signal['V1_tSymbol'],
                        signal['status_assets'], signal['forward_ratio'],
                        signal['group_id'], resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolRunTradeOrdersTypePair(
                        signal['J1_server'], signal['J2_server'],
                        signal['V3_fSymbol'], signal['V3_tSymbol'],
                        signal['V2_fSymbol'], signal['V2_tSymbol'],
                        signal['V1_fSymbol'], signal['V1_tSymbol'],
                        signal['status_assets'], signal['forward_ratio'],
                        signal['group_id'], resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                if isV2:
                    orders = self._calcSymbolRunTradeOrdersTypePair(
                        signal['J1_server'], signal['J2_server'],
                        signal['V1_fSymbol'], signal['V1_tSymbol'],
                        signal['V3_fSymbol'], signal['V3_tSymbol'],
                        signal['V2_fSymbol'], signal['V2_tSymbol'],
                        signal['status_assets'], signal['forward_ratio'],
                        signal['group_id'], resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolRunTradeOrdersTypePair(
                        signal['J1_server'], signal['J2_server'],
                        signal['V3_fSymbol'], signal['V3_tSymbol'],
                        signal['V1_fSymbol'], signal['V1_tSymbol'],
                        signal['V2_fSymbol'], signal['V2_tSymbol'],
                        signal['status_assets'], signal['forward_ratio'],
                        signal['group_id'], resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                if isV3:
                    orders = self._calcSymbolRunTradeOrdersTypePair(
                        signal['J1_server'], signal['J2_server'],
                        signal['V1_fSymbol'], signal['V1_tSymbol'],
                        signal['V2_fSymbol'], signal['V2_tSymbol'],
                        signal['V3_fSymbol'], signal['V3_tSymbol'],
                        signal['status_assets'], signal['forward_ratio'],
                        signal['group_id'], resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolRunTradeOrdersTypePair(
                        signal['J1_server'], signal['J2_server'],
                        signal['V2_fSymbol'], signal['V2_tSymbol'],
                        signal['V1_fSymbol'], signal['V1_tSymbol'],
                        signal['V3_fSymbol'], signal['V3_tSymbol'],
                        signal['status_assets'], signal['forward_ratio'],
                        signal['group_id'], resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
            # return
            return res
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcSignalRunTradeOrders: {signal=%s, resInfoSymbol=%s}, exception err=%s" % (
                signal, 'resInfoSymbol', err)
            raise CalcException(errStr)

    def calcSignalAfterTradeOrders(self, signal, resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalAfterTradeOrders: {signal=%s, resInfoSymbol=%s, baseCoin=%s}"
            % (signal, 'resInfoSymbol', baseCoin))
        try:
            res = []
            # calc orders
            if signal['type'] == TYPE_DIS:
                bid_fSymbol_to_base = 0
                bid_tSymbol_to_base = 0
                ask_fSymbol_to_base = 0
                ask_tSymbol_to_base = 0
                for status in signal['status_assets']:
                    if status['server'] == signal['bid_server']:
                        if status['asset'] == signal['fSymbol']:
                            bid_fSymbol_to_base = status['balance']
                        if status['asset'] == signal['tSymbol']:
                            bid_tSymbol_to_base = status['balance']
                    if status['server'] == signal['ask_server']:
                        if status['asset'] == signal['fSymbol']:
                            ask_fSymbol_to_base = status['balance']
                        if status['asset'] == signal['tSymbol']:
                            ask_tSymbol_to_base = status['balance']
                orders = self._calcSymbolAfterTradeOrders(
                    signal['bid_server'], signal['fSymbol'], signal['tSymbol'],
                    bid_fSymbol_to_base, bid_tSymbol_to_base,
                    signal['group_id'], resInfoSymbol, baseCoin)
                if not orders == []:
                    res.extend(orders)
                orders = self._calcSymbolAfterTradeOrders(
                    signal['ask_server'], signal['fSymbol'], signal['tSymbol'],
                    ask_fSymbol_to_base, ask_tSymbol_to_base,
                    signal['group_id'], resInfoSymbol, baseCoin)
                if not orders == []:
                    res.extend(orders)
            if signal['type'] == TYPE_TRA:
                # find target unique tSymbol
                C1_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                C2_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                ][0]
                C3_symbol = [
                    i for i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                if C1_symbol == signal['V1_fSymbol']:
                    fSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['server']:
                            if status['asset'] == signal['V1_fSymbol']:
                                fSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    tSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['server']:
                            if status['asset'] == signal['V1_tSymbol']:
                                tSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], 0, tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C2_symbol == signal['V2_fSymbol']:
                    fSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['server']:
                            if status['asset'] == signal['V2_fSymbol']:
                                fSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    tSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['server']:
                            if status['asset'] == signal['V2_tSymbol']:
                                tSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], 0, tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C3_symbol == signal['V3_fSymbol']:
                    fSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['server']:
                            if status['asset'] == signal['V3_fSymbol']:
                                fSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    tSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['server']:
                            if status['asset'] == signal['V3_tSymbol']:
                                tSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], 0, tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
            if signal['type'] == TYPE_PAIR:
                # find target unique tSymbol
                C1_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                C2_symbol = [
                    i for i in [signal['V1_fSymbol'], signal['V1_tSymbol']]
                    if i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                ][0]
                C3_symbol = [
                    i for i in [signal['V2_fSymbol'], signal['V2_tSymbol']]
                    if i in [signal['V3_fSymbol'], signal['V3_tSymbol']]
                ][0]
                if C1_symbol == signal['V1_fSymbol']:
                    J1_fSymbol_to_base = 0
                    J2_fSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['J1_server']:
                            if status['asset'] == signal['V1_fSymbol']:
                                J1_fSymbol_to_base = status['balance']
                        if status['server'] == signal['J2_server']:
                            if status['asset'] == signal['V1_fSymbol']:
                                J2_fSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J1_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], J1_fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J2_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], J2_fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    J1_tSymbol_to_base = 0
                    J2_tSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['J1_server']:
                            if status['asset'] == signal['V1_tSymbol']:
                                J1_tSymbol_to_base = status['balance']
                        if status['server'] == signal['J2_server']:
                            if status['asset'] == signal['V1_tSymbol']:
                                J2_tSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J1_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], 0, J1_tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J2_server'], signal['V1_fSymbol'],
                        signal['V1_tSymbol'], 0, J2_tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C2_symbol == signal['V2_fSymbol']:
                    J1_fSymbol_to_base = 0
                    J2_fSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['J1_server']:
                            if status['asset'] == signal['V2_fSymbol']:
                                J1_fSymbol_to_base = status['balance']
                        if status['server'] == signal['J2_server']:
                            if status['asset'] == signal['V2_fSymbol']:
                                J2_fSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J1_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], J1_fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J2_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], J2_fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    J1_tSymbol_to_base = 0
                    J2_tSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['J1_server']:
                            if status['asset'] == signal['V2_tSymbol']:
                                J1_tSymbol_to_base = status['balance']
                        if status['server'] == signal['J2_server']:
                            if status['asset'] == signal['V2_tSymbol']:
                                J2_tSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J1_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], 0, J1_tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J2_server'], signal['V2_fSymbol'],
                        signal['V2_tSymbol'], 0, J2_tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                if C3_symbol == signal['V3_fSymbol']:
                    J1_fSymbol_to_base = 0
                    J2_fSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['J1_server']:
                            if status['asset'] == signal['V3_fSymbol']:
                                J1_fSymbol_to_base = status['balance']
                        if status['server'] == signal['J2_server']:
                            if status['asset'] == signal['V3_fSymbol']:
                                J2_fSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J1_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], J1_fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J2_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], J2_fSymbol_to_base, 0,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                else:
                    J1_tSymbol_to_base = 0
                    J2_tSymbol_to_base = 0
                    for status in signal['status_assets']:
                        if status['server'] == signal['J1_server']:
                            if status['asset'] == signal['V3_tSymbol']:
                                J1_tSymbol_to_base = status['balance']
                        if status['server'] == signal['J2_server']:
                            if status['asset'] == signal['V3_tSymbol']:
                                J2_tSymbol_to_base = status['balance']
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J1_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], 0, J1_tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
                    orders = self._calcSymbolAfterTradeOrders(
                        signal['J2_server'], signal['V3_fSymbol'],
                        signal['V3_tSymbol'], 0, J2_tSymbol_to_base,
                        signal['group_id'], resInfoSymbol, baseCoin)
                    if not orders == []:
                        res.extend(orders)
            # return
            return res
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcSignalRunTradeOrders: {signal=%s, resInfoSymbol=%s, baseCoin=%s}, exception err=%s" % (
                signal, 'resInfoSymbol', baseCoin, err)
            raise CalcException(errStr)

    def calcSignalIsAfterMore(self, signal, resInfoSymbol, baseCoin):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcSignalIsAfterMore: {signal=%s, resInfoSymbol=%s, baseCoin=%s}"
            % (signal, 'resInfoSymbol', baseCoin))
        try:
            isMore = False
            # calc res
            if signal['type'] == TYPE_DIS:
                isDe_bid_fSymbol = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['bid_server'])
                    & (resInfoSymbol['fSymbol'] == signal['fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_bid_fSymbol = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['bid_server'])
                    & (resInfoSymbol['fSymbol'] == signal['fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['tSymbol'])]
                isDe_bid_tSymbol = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['bid_server'])
                    & (resInfoSymbol['fSymbol'] == signal['tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_ask_fSymbol = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['ask_server'])
                    & (resInfoSymbol['fSymbol'] == signal['fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_ask_fSymbol = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['ask_server'])
                    & (resInfoSymbol['fSymbol'] == signal['fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['tSymbol'])]
                isDe_ask_tSymbol = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['ask_server'])
                    & (resInfoSymbol['fSymbol'] == signal['tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                # calc assets
                bid_fSymbol_assets = 0
                bid_tSymbol_assets = 0
                ask_fSymbol_assets = 0
                ask_tSymbol_assets = 0
                for status in signal['status_assets']:
                    if status['server'] == signal['bid_server']:
                        if status['asset'] == signal['fSymbol']:
                            bid_fSymbol_assets = status['balance']
                        if status['asset'] == signal['tSymbol']:
                            bid_tSymbol_assets = status['balance']
                    if status['server'] == signal['ask_server']:
                        if status['asset'] == signal['fSymbol']:
                            ask_fSymbol_assets = status['balance']
                        if status['asset'] == signal['tSymbol']:
                            ask_tSymbol_assets = status['balance']
                if bid_fSymbol_assets > 0:
                    if not isDe_bid_fSymbol.empty:
                        size_min = 0
                        if not isDe_bid_fSymbol['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_bid_fSymbol[
                                'limit_size_min'].values[0]
                        if bid_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_bid_fSymbol.empty:
                        size_min = 0
                        if not isTra_bid_fSymbol['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_bid_fSymbol[
                                'limit_size_min'].values[0]
                        if bid_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if ask_fSymbol_assets > 0:
                    if not isDe_ask_fSymbol.empty:
                        size_min = 0
                        if not isDe_ask_fSymbol['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_ask_fSymbol[
                                'limit_size_min'].values[0]
                        if ask_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_ask_fSymbol.empty:
                        size_min = 0
                        if not isTra_ask_fSymbol['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_ask_fSymbol[
                                'limit_size_min'].values[0]
                        if ask_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if bid_tSymbol_assets > 0:
                    if not isDe_tSymbol.empty:
                        size_min = 0
                        if not isDe_bid_tSymbol['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_bid_tSymbol[
                                'limit_size_min'].values[0]
                        if bid_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if ask_tSymbol_assets > 0:
                    if not isDe_tSymbol.empty:
                        size_min = 0
                        if not isDe_ask_tSymbol['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_ask_tSymbol[
                                'limit_size_min'].values[0]
                        if ask_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
            if signal['type'] == TYPE_TRA:
                isDe_fSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_fSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V1_tSymbol'])]
                isDe_tSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_fSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_fSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V2_tSymbol'])]
                isDe_tSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_fSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_fSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V3_tSymbol'])]
                isDe_tSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                # calc assets
                V1_fSymbol_assets = 0
                V1_tSymbol_assets = 0
                V2_fSymbol_assets = 0
                V2_tSymbol_assets = 0
                V3_fSymbol_assets = 0
                V3_tSymbol_assets = 0
                for status in signal['status_assets']:
                    if status['server'] == signal['server']:
                        if status['asset'] == signal['V1_fSymbol']:
                            V1_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V1_tSymbol']:
                            V1_tSymbol_assets = status['balance']
                        if status['asset'] == signal['V2_fSymbol']:
                            V2_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V2_tSymbol']:
                            V2_tSymbol_assets = status['balance']
                        if status['asset'] == signal['V3_fSymbol']:
                            V3_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V3_tSymbol']:
                            V3_tSymbol_assets = status['balance']
                if V1_fSymbol_assets > 0:
                    if not isDe_fSymbol_V1.empty:
                        size_min = 0
                        if not isDe_fSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_fSymbol_V1[
                                'limit_size_min'].values[0]
                        if V1_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_fSymbol_V1.empty:
                        size_min = 0
                        if not isTra_fSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_fSymbol_V1[
                                'limit_size_min'].values[0]
                        if V1_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if V1_tSymbol_assets > 0:
                    if not isDe_tSymbol_V1.empty:
                        size_min = 0
                        if not isDe_tSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_tSymbol_V1[
                                'limit_size_min'].values[0]
                        if V1_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if V2_fSymbol_assets > 0:
                    if not isDe_fSymbol_V2.empty:
                        size_min = 0
                        if not isDe_fSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_fSymbol_V2[
                                'limit_size_min'].values[0]
                        if V2_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_fSymbol_V2.empty:
                        size_min = 0
                        if not isTra_fSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_fSymbol_V2[
                                'limit_size_min'].values[0]
                        if V2_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if V2_tSymbol_assets > 0:
                    if not isDe_tSymbol_V2.empty:
                        size_min = 0
                        if not isDe_tSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_tSymbol_V2[
                                'limit_size_min'].values[0]
                        if V2_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if V3_fSymbol_assets > 0:
                    if not isDe_fSymbol_V3.empty:
                        size_min = 0
                        if not isDe_fSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_fSymbol_V3[
                                'limit_size_min'].values[0]
                        if V3_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_fSymbol_V3.empty:
                        size_min = 0
                        if not isTra_fSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_fSymbol_V3[
                                'limit_size_min'].values[0]
                        if V3_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if V3_tSymbol_assets > 0:
                    if not isDe_tSymbol_V3.empty:
                        size_min = 0
                        if not isDe_tSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_tSymbol_V3[
                                'limit_size_min'].values[0]
                        if V3_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
            if signal['type'] == TYPE_PAIR:
                isDe_J1_fSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_J1_fSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V1_tSymbol'])]
                isDe_J1_tSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_J1_fSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_J1_fSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V2_tSymbol'])]
                isDe_J1_tSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_J1_fSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_J1_fSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V3_tSymbol'])]
                isDe_J1_tSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J1_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_J2_fSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_J2_fSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V1_tSymbol'])]
                isDe_J2_tSymbol_V1 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V1_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_J2_fSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_J2_fSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V2_tSymbol'])]
                isDe_J2_tSymbol_V2 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V2_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isDe_J2_fSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                isTra_J2_fSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_fSymbol'])
                    & (resInfoSymbol['tSymbol'] == signal['V3_tSymbol'])]
                isDe_J2_tSymbol_V3 = resInfoSymbol[
                    (resInfoSymbol['server'] == signal['J2_server'])
                    & (resInfoSymbol['fSymbol'] == signal['V3_tSymbol'])
                    & (resInfoSymbol['tSymbol'] == baseCoin)]
                # calc assets
                J1_V1_fSymbol_assets = 0
                J1_V1_tSymbol_assets = 0
                J1_V2_fSymbol_assets = 0
                J1_V2_tSymbol_assets = 0
                J1_V3_fSymbol_assets = 0
                J1_V3_tSymbol_assets = 0
                J2_V1_fSymbol_assets = 0
                J2_V1_tSymbol_assets = 0
                J2_V2_fSymbol_assets = 0
                J2_V2_tSymbol_assets = 0
                J2_V3_fSymbol_assets = 0
                J2_V3_tSymbol_assets = 0
                for status in signal['status_assets']:
                    if status['server'] == signal['J1_server']:
                        if status['asset'] == signal['V1_fSymbol']:
                            J1_V1_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V1_tSymbol']:
                            J1_V1_tSymbol_assets = status['balance']
                        if status['asset'] == signal['V2_fSymbol']:
                            J1_V2_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V2_tSymbol']:
                            J1_V2_tSymbol_assets = status['balance']
                        if status['asset'] == signal['V3_fSymbol']:
                            J1_V3_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V3_tSymbol']:
                            J1_V3_tSymbol_assets = status['balance']
                    if status['server'] == signal['J2_server']:
                        if status['asset'] == signal['V1_fSymbol']:
                            J2_V1_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V1_tSymbol']:
                            J2_V1_tSymbol_assets = status['balance']
                        if status['asset'] == signal['V2_fSymbol']:
                            J2_V2_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V2_tSymbol']:
                            J2_V2_tSymbol_assets = status['balance']
                        if status['asset'] == signal['V3_fSymbol']:
                            J2_V3_fSymbol_assets = status['balance']
                        if status['asset'] == signal['V3_tSymbol']:
                            J2_V3_tSymbol_assets = status['balance']
                if J1_V1_fSymbol_assets > 0:
                    if not isDe_J1_fSymbol_V1.empty:
                        size_min = 0
                        if not isDe_J1_fSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J1_fSymbol_V1[
                                'limit_size_min'].values[0]
                        if J1_V1_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_J1_fSymbol_V1.empty:
                        size_min = 0
                        if not isTra_J1_fSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_J1_fSymbol_V1[
                                'limit_size_min'].values[0]
                        if J1_V1_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J1_V1_tSymbol_assets > 0:
                    if not isDe_J1_tSymbol_V1.empty:
                        size_min = 0
                        if not isDe_J1_tSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J1_tSymbol_V1[
                                'limit_size_min'].values[0]
                        if V1_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J1_V2_fSymbol_assets > 0:
                    if not isDe_J1_fSymbol_V2.empty:
                        size_min = 0
                        if not isDe_J1_fSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J1_fSymbol_V2[
                                'limit_size_min'].values[0]
                        if J1_V2_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_J1_fSymbol_V2.empty:
                        size_min = 0
                        if not isTra_J1_fSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_J1_fSymbol_V2[
                                'limit_size_min'].values[0]
                        if J1_V2_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J1_V2_tSymbol_assets > 0:
                    if not isDe_J1_tSymbol_V2.empty:
                        size_min = 0
                        if not isDe_J1_tSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J1_tSymbol_V2[
                                'limit_size_min'].values[0]
                        if J1_V2_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J1_V3_fSymbol_assets > 0:
                    if not isDe_J1_fSymbol_V3.empty:
                        size_min = 0
                        if not isDe_J1_fSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J1_fSymbol_V3[
                                'limit_size_min'].values[0]
                        if J1_V3_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_J1_fSymbol_V3.empty:
                        size_min = 0
                        if not isTra_J1_fSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_J1_fSymbol_V3[
                                'limit_size_min'].values[0]
                        if J1_V3_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J1_V3_tSymbol_assets > 0:
                    if not isDe_J1_tSymbol_V3.empty:
                        size_min = 0
                        if not isDe_J1_tSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J1_tSymbol_V3[
                                'limit_size_min'].values[0]
                        if J1_V3_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J2_V1_fSymbol_assets > 0:
                    if not isDe_J2_fSymbol_V1.empty:
                        size_min = 0
                        if not isDe_J2_fSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J2_fSymbol_V1[
                                'limit_size_min'].values[0]
                        if J2_V1_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_J2_fSymbol_V1.empty:
                        size_min = 0
                        if not isTra_J2_fSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_J2_fSymbol_V1[
                                'limit_size_min'].values[0]
                        if J2_V1_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J2_V1_tSymbol_assets > 0:
                    if not isDe_J2_tSymbol_V1.empty:
                        size_min = 0
                        if not isDe_J2_tSymbol_V1['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J2_tSymbol_V1[
                                'limit_size_min'].values[0]
                        if V1_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J2_V2_fSymbol_assets > 0:
                    if not isDe_J2_fSymbol_V2.empty:
                        size_min = 0
                        if not isDe_J2_fSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J2_fSymbol_V2[
                                'limit_size_min'].values[0]
                        if J2_V2_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_J2_fSymbol_V2.empty:
                        size_min = 0
                        if not isTra_J2_fSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_J2_fSymbol_V2[
                                'limit_size_min'].values[0]
                        if J2_V2_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J2_V2_tSymbol_assets > 0:
                    if not isDe_J2_tSymbol_V2.empty:
                        size_min = 0
                        if not isDe_J2_tSymbol_V2['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J2_tSymbol_V2[
                                'limit_size_min'].values[0]
                        if J2_V2_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J2_V3_fSymbol_assets > 0:
                    if not isDe_J2_fSymbol_V3.empty:
                        size_min = 0
                        if not isDe_J2_fSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J2_fSymbol_V3[
                                'limit_size_min'].values[0]
                        if J2_V3_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                    if not isTra_J2_fSymbol_V3.empty:
                        size_min = 0
                        if not isTra_J2_fSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isTra_J2_fSymbol_V3[
                                'limit_size_min'].values[0]
                        if J2_V3_fSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore
                if J2_V3_tSymbol_assets > 0:
                    if not isDe_J2_tSymbol_V3.empty:
                        size_min = 0
                        if not isDe_J2_tSymbol_V3['limit_size_min'].values[
                                0] == 'NULL':
                            size_min = isDe_J2_tSymbol_V3[
                                'limit_size_min'].values[0]
                        if J2_V3_tSymbol_assets > size_min + CALC_ZERO_NUMBER:
                            isMore = True
                            return isMore

            # return
            return isMore
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcSignalIsAfterMore: {signal=%s, resInfoSymbol=%s, baseCoin=%s}, exception err=%s" % (
                signal, 'resInfoSymbol', baseCoin, err)
            raise CalcException(errStr)

    def calcStatisticJudgeMarketTickerDis(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticJudgeMarketTickerDis: {exchange=%s, timeWindow=%s}"
            % (exchange, timeWindow))
        try:
            statistic = []
            db = DB()
            # statistic dis type
            for server, server_pair in combinations(exchange, 2):
                signal = db.getViewJudgeMarketTickerDisCurrentServer(
                    server, server_pair)
                if not signal == []:
                    df = pd.DataFrame(signal)
                    for (fSymbol,
                         tSymbol), group in df.groupby(['fSymbol', 'tSymbol']):
                        # calc group_id
                        id_str = TYPE_DIS + str(server) + str(
                            server_pair) + str(fSymbol) + str(tSymbol)
                        group_id = '0x1b-' + str(
                            uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
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
                            group['gain_ratio'].values.std(),
                            "group_id":
                            group_id
                        }
                        # update statistic
                        statistic.append(sta)
            return statistic
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcStatisticJudgeMarketTickerDis: {exchange=%s, timeWindow=%s}, exception err=%s" % (
                exchange, timeWindow, err)
            raise CalcException(errStr)

    def calcStatisticJudgeMarketTickerTra(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticJudgeMarketTickerTra: {exchange=%s, timeWindow=%s}"
            % (exchange, timeWindow))
        try:
            statistic = []
            db = DB()
            # statistic dis type
            signal = db.getViewJudgeMarketTickerTraCurrentServer(exchange)
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
                    # calc group_id
                    id_str = TYPE_TRA + str(server) + str(symbol_pair)
                    group_id = '0x2b-' + str(
                        uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
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
                        group[(group['V2_fSymbol'] == group['V3_fSymbol']
                               )].shape[0],
                        "count_backward":
                        group[(group['V2_fSymbol'] == group['V3_tSymbol']
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
                        group['gain_ratio'].values.std(),
                        "group_id":
                        group_id
                    }
                    # update statistic
                    statistic.append(sta)
            return statistic
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcStatisticJudgeMarketTickerTra: {exchange=%s, timeWindow=%s}, exception err=%s" % (
                exchange, timeWindow, err)
            raise CalcException(errStr)

    def calcStatisticJudgeMarketTickerPair(self, exchange, timeWindow):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcStatisticJudgeMarketTickerPair: {exchange=%s, timeWindow=%s}"
            % (exchange, timeWindow))
        try:
            statistic = []
            db = DB()
            # statistic dis type
            for server, server_pair in combinations(exchange, 2):
                signal = db.getViewJudgeMarketTickerPairCurrentServer(
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
                        # calc group_id
                        id_str = TYPE_PAIR + str(server) + str(
                            server_pair) + str(symbol_pair)
                        group_id = '0x3b-' + str(
                            uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
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
                            group[(group['V2_fSymbol'] == group['V3_fSymbol']
                                   )].shape[0],
                            "count_backward":
                            group[(group['V2_fSymbol'] == group['V3_tSymbol']
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
                            group['gain_ratio'].values.std(),
                            "group_id":
                            group_id
                        }
                        # update statistic
                        statistic.append(sta)
            return statistic
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcStatisticJudgeMarketTickerPair: {exchange=%s, timeWindow=%s}, exception err=%s" % (
                exchange, timeWindow, err)
            raise CalcException(errStr)

    def calcJudgeMarketTickerDis(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeMarketTickerDis: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
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
                        (resInfoSymbol['server'] == r['bid_server']) &
                        (resInfoSymbol['fSymbol'] == r['fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['tSymbol']
                           )]['fee_taker']
                    r['ask_fee'] = 0
                    ask_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['ask_server']) &
                        (resInfoSymbol['fSymbol'] == r['fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['tSymbol']
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
                        r['bid_price_base'] / r['bid_price']
                        + r['ask_price_base'] / r['ask_price']) / 2
                    # calc gain_base
                    r['gain_base'] = (
                        r['bid_price'] * r['bid_size']
                        - r['ask_price'] * r['ask_size'] - r['bid_price']
                        * r['bid_size'] * r['bid_fee'] - r['ask_price']
                        * r['ask_size'] * r['ask_fee']) * tSymbol_base_price
                    # calc gain_ratio
                    r['gain_ratio'] = (
                        r['bid_price'] - r['ask_price']
                        - r['bid_price'] * r['bid_fee']
                        - r['ask_price'] * r['ask_fee']) / r['ask_price']
                    # calc signal
                    if r['gain_ratio'] > threshold:
                        signal.append(r)
            # return signal
            return signal
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcJudgeMarketTickerDis: {exchange=%s, threshold=%s, resInfoSymbol=%s}, exception err=%s" % (
                exchange, threshold, 'resInfoSymbol', err)
            raise CalcException(errStr)

    def calcJudgeMarketTickerTra(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeMarketTickerTra: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
            % (exchange, threshold, 'resInfoSymbol'))
        try:
            db = DB()
            signal = []
            # calc tra type
            res = db.getViewMarketTickerCurrentTraServer(exchange)
            # calc gains with fee
            for r in res:
                # calc common symbol
                C1_symbol = [
                    i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                    if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                ][0]
                C2_symbol = [
                    i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                    if i in [r['V2_fSymbol'], r['V2_tSymbol']]
                ][0]
                C3_symbol = [
                    i for i in [r['V2_fSymbol'], r['V2_tSymbol']]
                    if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                ][0]
                # calc V1
                if C1_symbol == r['V1_fSymbol']:  # fSymbol -> tSymbol
                    r['V1_one_price'] = r['V1_bid_one_price']
                    r['V1_one_side'] = CCAT_ORDER_SIDE_SELL
                    r['V1_one_size'] = r['V1_bid_one_size']
                else:  # tSymbol -> fSymbol
                    r['V1_one_price'] = r['V1_ask_one_price']
                    r['V1_one_side'] = CCAT_ORDER_SIDE_BUY
                    r['V1_one_size'] = r['V1_ask_one_size']
                # calc V2
                if C2_symbol == r['V2_fSymbol']:  # fSymbol -> tSymbol
                    r['V2_one_price'] = r['V2_bid_one_price']
                    r['V2_one_side'] = CCAT_ORDER_SIDE_SELL
                    r['V2_one_size'] = r['V2_bid_one_size']
                else:  # tSymbol -> fSymbol
                    r['V2_one_price'] = r['V2_ask_one_price']
                    r['V2_one_side'] = CCAT_ORDER_SIDE_BUY
                    r['V2_one_size'] = r['V2_ask_one_size']
                # calc V3
                if C3_symbol == r['V3_fSymbol']:  # fSymbol -> tSymbol
                    r['V3_one_price'] = r['V3_bid_one_price']
                    r['V3_one_side'] = CCAT_ORDER_SIDE_SELL
                    r['V3_one_size'] = r['V3_bid_one_size']
                else:  # tSymbol -> fSymbol
                    r['V3_one_price'] = r['V3_ask_one_price']
                    r['V3_one_side'] = CCAT_ORDER_SIDE_BUY
                    r['V3_one_size'] = r['V3_ask_one_size']
                # calc symbol one price ratio
                if C3_symbol == r['V3_fSymbol']:
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
                    (resInfoSymbol['server'] == r['server']) &
                    (resInfoSymbol['fSymbol'] == r['V1_fSymbol'])

                    & (resInfoSymbol['tSymbol'] == r['V1_tSymbol'])]['fee_taker']
                r['V2_fee'] = 0
                V2_fee = resInfoSymbol[
                    (resInfoSymbol['server'] == r['server']) &
                    (resInfoSymbol['fSymbol'] == r['V2_fSymbol'])

                    & (resInfoSymbol['tSymbol'] == r['V2_tSymbol'])]['fee_taker']
                r['V3_fee'] = 0
                V3_fee = resInfoSymbol[
                    (resInfoSymbol['server'] == r['server']) &
                    (resInfoSymbol['fSymbol'] == r['V3_fSymbol'])

                    & (resInfoSymbol['tSymbol'] == r['V3_tSymbol'])]['fee_taker']
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
                V2_tSymbol_base_price = (
                    r['V2_bid_one_price_base'] / r['V2_bid_one_price']
                    + r['V2_ask_one_price_base'] / r['V2_ask_one_price']) / 2
                # Begin Calc Gain: Gain V2 tSymbol
                if C3_symbol == r['V3_fSymbol']:
                    # Type clockwise: sell->buy->sell
                    # calc symbol size
                    temp_C3 = min(
                        r['V3_one_size'],
                        r['V2_one_size'] * C2_C3_one_price * (1 - r['V2_fee']))
                    temp_C1 = min(
                        r['V1_one_size'],
                        temp_C3 * C3_C1_one_price * (1 - r['V3_fee']))
                    temp_C3 = temp_C1 / C3_C1_one_price / (1 - r['V3_fee'])
                    temp_C2 = temp_C3 / C2_C3_one_price / (1 - r['V2_fee'])
                    r['V2_one_size'] = temp_C2 * (
                        1 - r['V2_fee']) / r['V2_one_price']
                    r['V3_one_size'] = r['V2_one_size']
                    r['V1_one_size'] = r['V3_one_size'] * r['V3_one_price'] * (
                        1 - r['V3_fee'])
                else:
                    # Type anti-clockwise: sell->buy->buy
                    # calc symbol size
                    temp_C3 = min(
                        r['V3_one_size'],
                        r['V2_one_size'] * C2_C3_one_price * (1 - r['V2_fee']))
                    temp_C1 = min(
                        r['V1_one_size'],
                        temp_C3 * C3_C1_one_price * (1 - r['V3_fee']))
                    temp_C3 = temp_C1 / C3_C1_one_price / (1 - r['V3_fee'])
                    temp_C2 = temp_C3 / C2_C3_one_price / (1 - r['V2_fee'])
                    r['V2_one_size'] = temp_C2 * (
                        1 - r['V2_fee']) / r['V2_one_price']
                    r['V3_one_size'] = r['V2_one_size'] * (
                        1 - r['V3_fee']) / r['V3_one_price']
                    r['V1_one_size'] = r['V3_one_size']
                # calc gain_base
                r['gain_base'] = (
                    C1_C2_one_price * C3_C1_one_price * (1 - r['V1_fee'])
                    * (1 - r['V3_fee']) - 1 / C2_C3_one_price
                    - 1 / C2_C3_one_price * r['V2_fee']) / (
                        1 / C2_C3_one_price) * temp_C2 * V2_tSymbol_base_price
                # calc gain_ratio
                r['gain_ratio'] = (
                    C1_C2_one_price * C3_C1_one_price * (1 - r['V1_fee'])
                    * (1 - r['V3_fee']) - 1 / C2_C3_one_price
                    - 1 / C2_C3_one_price * r['V2_fee']) / (1 / C2_C3_one_price)
                # calc signal
                if r['gain_ratio'] > threshold:
                    signal.append(r)
            # return signal
            return signal
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcJudgeMarketTickerTra: {exchange=%s, threshold=%s, resInfoSymbol=%s}, exception err=%s" % (
                exchange, threshold, 'resInfoSymbol', err)
            raise CalcException(errStr)

    def calcJudgeMarketTickerPair(self, exchange, threshold, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.calc.Calc.calcJudgeMarketTickerPair: {exchange=%s, threshold=%s, resInfoSymbol=%s}"
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
                    C1_symbol = [
                        i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                        if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                    ][0]
                    C2_symbol = [
                        i for i in [r['V1_fSymbol'], r['V1_tSymbol']]
                        if i in [r['V2_fSymbol'], r['V2_tSymbol']]
                    ][0]
                    C3_symbol = [
                        i for i in [r['V2_fSymbol'], r['V2_tSymbol']]
                        if i in [r['V3_fSymbol'], r['V3_tSymbol']]
                    ][0]
                    # calc J1_V1, J2_V1
                    if C1_symbol == r['V1_fSymbol']:  # fSymbol -> tSymbol
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
                    if C2_symbol == r['V2_fSymbol']:  # fSymbol -> tSymbol
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
                    if C3_symbol == r['V3_fSymbol']:  # fSymbol -> tSymbol
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
                    if C3_symbol == r['V3_fSymbol']:
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
                        (resInfoSymbol['server'] == r['J1_server']) &
                        (resInfoSymbol['fSymbol'] == r['V1_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                           )]['fee_taker']
                    r['J1_V2_fee'] = 0
                    J1_V2_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J1_server']) &
                        (resInfoSymbol['fSymbol'] == r['V2_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                           )]['fee_taker']
                    r['J1_V3_fee'] = 0
                    J1_V3_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J1_server']) &
                        (resInfoSymbol['fSymbol'] == r['V3_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                           )]['fee_taker']
                    r['J2_V1_fee'] = 0
                    J2_V1_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J2_server']) &
                        (resInfoSymbol['fSymbol'] == r['V1_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V1_tSymbol']
                           )]['fee_taker']
                    r['J2_V2_fee'] = 0
                    J2_V2_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J2_server']) &
                        (resInfoSymbol['fSymbol'] == r['V2_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V2_tSymbol']
                           )]['fee_taker']
                    r['J2_V3_fee'] = 0
                    J2_V3_fee = resInfoSymbol[
                        (resInfoSymbol['server'] == r['J2_server']) &
                        (resInfoSymbol['fSymbol'] == r['V3_fSymbol']) &
                        (resInfoSymbol['tSymbol'] == r['V3_tSymbol']
                           )]['fee_taker']
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
                    if C3_symbol == r['V3_fSymbol']:
                        # Type J1 = clockwise: sell->buy->sell, J2 = anti-clockwise: sell->buy->buy
                        # calc J1 symbol size
                        temp_J1_C3 = min(
                            r['J1_V3_one_size'],
                            r['J1_V2_one_size'] * J1_C2_C3_one_price
                            * (1 - r['J1_V2_fee']))
                        temp_J1_C1 = min(
                            r['J1_V1_one_size'],
                            temp_J1_C3 * J1_C3_C1_one_price * (1 - r['J1_V3_fee']))
                        temp_J1_C3 = temp_J1_C1 / J1_C3_C1_one_price / (
                            1 - r['J1_V3_fee'])
                        temp_J1_C2 = temp_J1_C3 / J1_C2_C3_one_price / (
                            1 - r['J1_V2_fee'])
                        r['J1_V2_one_size'] = temp_J1_C2 * (
                            1 - r['J1_V2_fee']) / r['J1_V2_one_price']
                        r['J1_V3_one_size'] = r['J1_V2_one_size']
                        r['J1_V1_one_size'] = r['J1_V3_one_size'] * r['J1_V3_one_price'] * (
                            1 - r['J1_V3_fee'])
                        # calc J2 symbol size
                        temp_J2_C3 = min(
                            r['J2_V3_one_size'],
                            r['J2_V2_one_size'] * J2_C2_C3_one_price
                            * (1 - r['J2_V2_fee']))
                        temp_J2_C1 = min(
                            r['J2_V1_one_size'],
                            temp_J2_C3 * J2_C3_C1_one_price * (1 - r['J2_V3_fee']))
                        temp_J2_C3 = temp_J2_C1 / J2_C3_C1_one_price / (
                            1 - r['J2_V3_fee'])
                        temp_J2_C2 = temp_J2_C3 / J2_C2_C3_one_price / (
                            1 - r['J2_V2_fee'])
                        r['J2_V2_one_size'] = temp_J2_C2 * (
                            1 - r['J2_V2_fee']) / r['J2_V2_one_price']
                        r['J2_V3_one_size'] = r['J2_V2_one_size'] * (
                            1 - r['J2_V3_fee']) / r['J2_V3_one_price']
                        r['J2_V1_one_size'] = r['J2_V3_one_size']
                    else:
                        # Type J1 = anti-clockwise: sell->buy->buy, J2 = clockwise: sell->buy->sell
                        # calc J1 symbol size
                        temp_J1_C3 = min(
                            r['J1_V3_one_size'],
                            r['J1_V2_one_size'] * J1_C2_C3_one_price
                            * (1 - r['J1_V2_fee']))
                        temp_J1_C1 = min(
                            r['J1_V1_one_size'],
                            temp_J1_C3 * J1_C3_C1_one_price * (1 - r['J1_V3_fee']))
                        temp_J1_C3 = temp_J1_C1 / J1_C3_C1_one_price / (
                            1 - r['J1_V3_fee'])
                        temp_J1_C2 = temp_J1_C3 / J1_C2_C3_one_price / (
                            1 - r['J1_V2_fee'])
                        r['J1_V2_one_size'] = temp_J1_C2 * (
                            1 - r['J1_V2_fee']) / r['J1_V2_one_price']
                        r['J1_V3_one_size'] = r['J1_V2_one_size'] * (
                            1 - r['J1_V3_fee']) / r['J1_V3_one_price']
                        r['J1_V1_one_size'] = r['J1_V3_one_size']
                        # calc J2 symbol size
                        temp_J2_C3 = min(
                            r['J2_V3_one_size'],
                            r['J2_V2_one_size'] * J2_C2_C3_one_price
                            * (1 - r['J2_V2_fee']))
                        temp_J2_C1 = min(
                            r['J2_V1_one_size'],
                            temp_J2_C3 * J2_C3_C1_one_price * (1 - r['J2_V3_fee']))
                        temp_J2_C3 = temp_J2_C1 / J2_C3_C1_one_price / (
                            1 - r['J2_V3_fee'])
                        temp_J2_C2 = temp_J2_C3 / J2_C2_C3_one_price / (
                            1 - r['J2_V2_fee'])
                        r['J2_V2_one_size'] = temp_J2_C2 * (
                            1 - r['J2_V2_fee']) / r['J2_V2_one_price']
                        r['J2_V3_one_size'] = r['J2_V2_one_size']
                        r['J2_V1_one_size'] = r['J2_V3_one_size'] * r['J2_V3_one_price'] * (
                            1 - r['J2_V3_fee'])
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
                    J1_V1_tSymbol_base_price = (r['J1_V1_bid_one_price_base']
                                                / r['J1_V1_bid_one_price']
                                                + r['J1_V1_ask_one_price_base']
                                                / r['J1_V1_ask_one_price']) / 2
                    J1_V2_tSymbol_base_price = (r['J1_V2_bid_one_price_base']
                                                / r['J1_V2_bid_one_price']
                                                + r['J1_V2_ask_one_price_base']
                                                / r['J1_V2_ask_one_price']) / 2
                    J1_V3_tSymbol_base_price = (r['J1_V3_bid_one_price_base']
                                                / r['J1_V3_bid_one_price']
                                                + r['J1_V3_ask_one_price_base']
                                                / r['J1_V3_ask_one_price']) / 2
                    # calc J2
                    J2_V1_tSymbol_base_price = (r['J2_V1_bid_one_price_base']
                                                / r['J2_V1_bid_one_price']
                                                + r['J2_V1_ask_one_price_base']
                                                / r['J2_V1_ask_one_price']) / 2
                    J2_V2_tSymbol_base_price = (r['J2_V2_bid_one_price_base']
                                                / r['J2_V2_bid_one_price']
                                                + r['J2_V2_ask_one_price_base']
                                                / r['J2_V2_ask_one_price']) / 2
                    J2_V3_tSymbol_base_price = (r['J2_V3_bid_one_price_base']
                                                / r['J2_V3_bid_one_price']
                                                + r['J2_V3_ask_one_price_base']
                                                / r['J2_V3_ask_one_price']) / 2
                    tSymbol_base_price = (
                        (J1_V1_tSymbol_base_price + J2_V1_tSymbol_base_price)
                        * (r['J1_V1_one_size'] + r['J2_V1_one_size'])
                        + (J1_V2_tSymbol_base_price + J2_V2_tSymbol_base_price)
                        * (r['J1_V2_one_size'] + r['J2_V2_one_size'])
                        + (J1_V3_tSymbol_base_price + J2_V3_tSymbol_base_price)
                        * (r['J1_V3_one_size'] + r['J2_V3_one_size'])) / (
                            r['J1_V1_one_size'] + r['J2_V1_one_size']
                            + r['J1_V2_one_size'] + r['J2_V2_one_size']
                            + r['J1_V3_one_size'] + r['J2_V3_one_size'])
                    # Begin Calc Gain
                    C1_symbol_gain_ratio_up = (
                        r['J1_V1_one_price'] - r['J2_V1_one_price']
                        - r['J1_V1_one_price'] * r['J1_V1_fee']
                        - r['J2_V1_one_price'] * r['J2_V1_fee']) * (
                            r['J1_V1_one_size'] + r['J2_V1_one_size']) / 2
                    C1_symbol_gain_ratio_dn = r['J2_V1_one_price'] * (
                        r['J1_V1_one_size'] + r['J2_V1_one_size']) / 2
                    C2_symbol_gain_ratio_up = (
                        r['J1_V2_one_price'] - r['J2_V2_one_price']
                        - r['J1_V2_one_price'] * r['J1_V2_fee']
                        - r['J2_V2_one_price'] * r['J2_V2_fee']) * (
                            r['J1_V2_one_size'] + r['J2_V2_one_size']) / 2
                    C2_symbol_gain_ratio_dn = r['J2_V2_one_price'] * (
                        r['J1_V2_one_size'] + r['J2_V2_one_size']) / 2
                    C3_symbol_gain_ratio_up = (
                        r['J1_V3_one_price'] - r['J2_V3_one_price']
                        - r['J1_V3_one_price'] * r['J1_V3_fee']
                        - r['J2_V3_one_price'] * r['J2_V3_fee']) * (
                            r['J1_V3_one_size'] + r['J2_V3_one_size']) / 2
                    C3_symbol_gain_ratio_dn = r['J2_V3_one_price'] * (
                        r['J1_V3_one_size'] + r['J2_V3_one_size']) / 2
                    # calc gain_base
                    r['gain_base'] = (
                        C1_symbol_gain_ratio_up + C2_symbol_gain_ratio_up
                        + C3_symbol_gain_ratio_up) * tSymbol_base_price
                    # calc gain_ratio
                    r['gain_ratio'] = (
                        C1_symbol_gain_ratio_up + C2_symbol_gain_ratio_up
                        + C3_symbol_gain_ratio_up) / (
                            C1_symbol_gain_ratio_dn + C2_symbol_gain_ratio_dn
                            + C3_symbol_gain_ratio_dn)
                    # calc signal
                    if r['gain_ratio'] > threshold:
                        signal.append(r)
            # return signal
            return signal
        except (BinanceException, HuobiException, OkexException,
                Exception) as err:
            errStr = "src.core.calc.calc.Calc.calcJudgeMarketTickerPair: {exchange=%s, threshold=%s, resInfoSymbol=%s}, exception err=%s" % (
                exchange, threshold, 'resInfoSymbol', err)
            raise CalcException(errStr)
