# -*- coding: utf-8 -*-

import ast
import json
import os
import uuid

from src.core.calc.calc import Calc
from src.core.calc.enums import SIGNAL_AUTO, SIGNAL_BASECOIN, SIGNAL_SIGNALS
from src.core.engine.enums import TYPE_DIS, TYPE_PAIR, TYPE_TRA
from src.core.util.exceptions import CalcException
from src.core.util.helper import tuple_str_to_list, utcnow_timestamp
from src.core.util.log import Logger


class Signal(object):
    def __init__(self, signals=[]):
        # signal init
        self._signals = signals
        self._signals_str = SIGNAL_SIGNALS
        # logger
        self._logger = Logger()

    def signals(self, exchange='all', types='all', auto=SIGNAL_AUTO):
        self._logger.debug(
            "src.core.calc.signal.Signal.signals: {exchange=%s, types=%s, auto=%s}"
            % (exchange, types, auto))
        try:
            if not self._signals == []:
                signals = []
                for s in self._signals:
                    if s['type'] == TYPE_DIS:
                        if (types == 'all' or TYPE_DIS in types) and (
                                exchange == 'all' or
                            (s['bid_server'] in exchange
                             and s['ask_server'] in exchange)):
                            signals.append(s)
                    if s['type'] == TYPE_TRA:
                        if (types == 'all' or TYPE_TRA in types) and (
                                exchange == 'all' or s['server'] in exchange):
                            signals.append(s)
                    if s['type'] == TYPE_PAIR:
                        if (types == 'all' or TYPE_PAIR in types) and (
                                exchange == 'all' or
                            (s['J1_server'] in exchange
                             and s['J2_server'] in exchange)):
                            signals.append(s)
                return signals
            if auto:
                return self._autoSignals(exchange, types)
            if not auto:
                return self._configSignals(exchange, types)
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.signals: {exchange=%s, types=%s, auto=%s}, exception err=%s" % (
                exchange, types, auto, err)
            raise CalcException(errStr)

    def _autoSignals(self, exchange, types):
        self._logger.debug("src.core.calc.signal.Signal._autoSignals")
        try:
            signals = []
            # return signals
            return signals
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.signals, exception err=%s" % err
            raise CalcException(errStr)

    def _configSignals(self, exchange, types):
        self._logger.debug("src.core.calc.signal.Signal._configSignals")
        try:
            signals = []
            strList = ast.literal_eval(self._signals_str)
            if not strList == []:
                pid = os.getpid()
                timeStamp = utcnow_timestamp()
                id = 0
                for s in strList:
                    id = id + 1
                    signal = {}
                    if s['type'] == TYPE_DIS:
                        if (types == 'all' or TYPE_DIS in types) and (
                                exchange == 'all' or
                            (s['bid_server'] in exchange
                             and s['ask_server'] in exchange)):
                            id_str = str(pid) + str(timeStamp) + str(id)
                            signal['timeStamp'] = timeStamp
                            signal['signal_id'] = '0x1c-' + str(
                                uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
                            signal['type'] = s['type']
                            signal['bid_server'] = s['bid_server']
                            signal['ask_server'] = s['ask_server']
                            signal['fSymbol'] = s['fSymbol']
                            signal['tSymbol'] = s['tSymbol']
                            signal['forward_ratio'] = float(s['forward_ratio'])
                            signal['backward_ratio'] = float(
                                s['backward_ratio'])
                            signal['base_start'] = float(s['base_start'])
                            signal['base_gain'] = float(s['base_gain'])
                            signal['base_timeout'] = float(s['base_timeout'])
                            signal['group_id'] = str(s['group_id'])
                            signal['status_done'] = False
                            signal['status_assets'] = [
                                {
                                    "server": s['bid_server'],
                                    "asset": SIGNAL_BASECOIN,
                                    "balance": float(s['base_start']) / 2,
                                    "free": float(s['base_start']) / 2,
                                    "locked": 0.0
                                },
                                {
                                    "server": s['ask_server'],
                                    "asset": SIGNAL_BASECOIN,
                                    "balance": float(s['base_start']) / 2,
                                    "free": float(s['base_start']) / 2,
                                    "locked": 0.0
                                }
                            ]
                            signal['status_gain'] = 0.0
                    if s['type'] == TYPE_TRA:
                        if (types == 'all' or TYPE_TRA in types) and (
                                exchange == 'all' or s['server'] in exchange):
                            tuple = tuple_str_to_list(s['symbol_pair'])
                            id_str = str(pid) + str(timeStamp) + str(id)
                            signal['timeStamp'] = timeStamp
                            signal['signal_id'] = '0x2c-' + str(
                                uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
                            signal['type'] = s['type']
                            signal['server'] = s['server']
                            signal['V1_fSymbol'] = tuple[0][0]
                            signal['V1_tSymbol'] = tuple[0][1]
                            signal['V2_fSymbol'] = tuple[1][0]
                            signal['V2_tSymbol'] = tuple[1][1]
                            signal['V3_fSymbol'] = tuple[2][0]
                            signal['V3_tSymbol'] = tuple[2][1]
                            signal['forward_ratio'] = float(s['forward_ratio'])
                            signal['base_start'] = float(s['base_start'])
                            signal['base_gain'] = float(s['base_gain'])
                            signal['base_timeout'] = float(s['base_timeout'])
                            signal['group_id'] = str(s['group_id'])
                            signal['status_done'] = False
                            signal['status_assets'] = [{
                                "server":
                                s['server'],
                                "asset":
                                SIGNAL_BASECOIN,
                                "balance":
                                float(s['base_start']),
                                "free":
                                float(s['base_start']),
                                "locked":
                                0.0
                            }]
                            signal['status_gain'] = 0.0
                    if s['type'] == TYPE_PAIR:
                        if (types == 'all' or TYPE_PAIR in types) and (
                                exchange == 'all' or
                            (s['J1_server'] in exchange
                             and s['J2_server'] in exchange)):
                            tuple = tuple_str_to_list(s['symbol_pair'])
                            id_str = str(pid) + str(timeStamp) + str(id)
                            signal['timeStamp'] = timeStamp
                            signal['signal_id'] = '0x3c-' + str(
                                uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
                            signal['type'] = s['type']
                            signal['J1_server'] = s['J1_server']
                            signal['J2_server'] = s['J2_server']
                            signal['V1_fSymbol'] = tuple[0][0]
                            signal['V1_tSymbol'] = tuple[0][1]
                            signal['V2_fSymbol'] = tuple[1][0]
                            signal['V2_tSymbol'] = tuple[1][1]
                            signal['V3_fSymbol'] = tuple[2][0]
                            signal['V3_tSymbol'] = tuple[2][1]
                            signal['forward_ratio'] = float(s['forward_ratio'])
                            signal['base_start'] = float(s['base_start'])
                            signal['base_gain'] = float(s['base_gain'])
                            signal['base_timeout'] = float(s['base_timeout'])
                            signal['group_id'] = str(s['group_id'])
                            signal['status_done'] = False
                            signal['status_assets'] = [
                                {
                                    "server": s['J1_server'],
                                    "asset": SIGNAL_BASECOIN,
                                    "balance": float(s['base_start']) / 2,
                                    "free": float(s['base_start']) / 2,
                                    "locked": 0.0
                                },
                                {
                                    "server": s['J2_server'],
                                    "asset": SIGNAL_BASECOIN,
                                    "balance": float(s['base_start']) / 2,
                                    "free": float(s['base_start']) / 2,
                                    "locked": 0.0
                                }
                            ]
                            signal['status_gain'] = 0.0
                    if not signal == {}:
                        signals.append(signal)
            # return signals
            return signals
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.signals, exception err=%s" % err
            raise CalcException(errStr)

    def backtestUpdateSignalStatusByOrders(self, infoOrders, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.signal.Signal.backtestUpdateSignalStatusByOrders: {infoOrders=%s, resInfoSymbol=%s}"
            % ('infoOrders', 'resInfoSymbol'))
        try:
            if not self._signals:
                raise Exception("NO SIGNAL ERROR, signals empty.")
            calc = Calc()
            resStatus = []
            timeStamp = utcnow_timestamp()
            for signal in self._signals:
                orders = infoOrders[(
                    infoOrders['group_id'] == signal['group_id'])]
                status = calc.calcSignalStatusByOrders(
                    signal, orders, resInfoSymbol, SIGNAL_BASECOIN)
                if not status == []:
                    resStatus.append({"signal_id": signal['signal_id'], "status": status})
            if not resStatus == []:
                for signal in self._signals:
                    for res in resStatus:
                        if signal['signal_id'] == res['signal_id']:
                            signal['timeStamp'] = timeStamp
                            signal['status_done'] = res['status'][
                                'status_done']
                            signal['status_assets'] = res['status'][
                                'status_assets']
                            signal['status_gain'] = res['status'][
                                'status_gain']
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestUpdateSignalStatusByOrders: {infoOrders=%s, resInfoSymbol=%s}, exception err=%s" % (
                'infoOrders', 'resInfoSymbol', err)
            raise CalcException(errStr)

    def backtestRollbackTrade(self, ):
        pass

    def backtestSignalsPreTrade(self, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.signal.Signal.backtestSignalsPreTrade: {resInfoSymbol=%s}"
            % 'resInfoSymbol')
        try:
            if not self._signals:
                raise Exception("NO SIGNAL ERROR, signals empty.")
            calc = Calc()
            res = []
            for signal in self._signals:
                orders = calc.calcSignalPreTradeOrders(signal, resInfoSymbol,
                                                       SIGNAL_BASECOIN)
                if not orders == []:
                    res.extend(orders)
            return res
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsPreTrade: {resInfoSymbol=%s}, exception err=%s" % (
                'resInfoSymbol', err)
            raise CalcException(errStr)

    def backtestSignalsRunTrade(self, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.signal.Signal.backtestSignalsRunTrade: {resInfoSymbol=%s}"
            % 'resInfoSymbol')
        try:
            if not self._signals:
                raise Exception("NO SIGNAL ERROR, signals empty.")
            calc = Calc()
            res = []
            for signal in self._signals:
                if signal['status_gain'] < signal['base_gain']:
                    orders = calc.calcSignalRunTradeOrders(
                        signal, resInfoSymbol)
                    if not orders == []:
                        res.extend(orders)
                if signal['status_gain'] >= signal['base_gain']:
                    orders = calc.calcSignalAfterTradeOrders(
                        signal, resInfoSymbol, SIGNAL_BASECOIN)
                    if not orders == []:
                        res.extend(orders)
            return res
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsRunTrade: {resInfoSymbol=%s}, exception err=%s" % (
                'resInfoSymbol', err)
            raise CalcException(errStr)

    def backtestSignalsIsRunMore(self, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.signal.Signal.backtestSignalsIsRunMore: {resInfoSymbol=%s}"
            % 'resInfoSymbol')
        try:
            if not self._signals:
                raise Exception("NO SIGNAL ERROR, signals empty.")
            isMore = False
            for signal in self._signals:
                if signal['status_gain'] < signal['base_gain']:
                    isMore = True
                    break
            return isMore
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsIsRunMore: {resInfoSymbol=%s}, exception err=%s" % (
                'resInfoSymbol', err)
            raise CalcException(errStr)

    def backtestSignalsAfterTrade(self, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.signal.Signal.backtestSignalsAfterTrade: {resInfoSymbol=%s}"
            % 'resInfoSymbol')
        try:
            if not self._signals:
                raise Exception("NO SIGNAL ERROR, signals empty.")
            calc = Calc()
            res = []
            for signal in self._signals:
                orders = calc.calcSignalAfterTradeOrders(
                    signal, resInfoSymbol, SIGNAL_BASECOIN)
                if not orders == []:
                    res.extend(orders)
            return res
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsAfterTrade: {resInfoSymbol=%s}, exception err=%s" % (
                'resInfoSymbol', err)
            raise CalcException(errStr)

    def backtestSignalsIsAfterMore(self, resInfoSymbol):
        self._logger.debug(
            "src.core.calc.signal.Signal.backtestSignalsIsAfterMore: {resInfoSymbol=%s}"
            % 'resInfoSymbol')
        try:
            if not self._signals:
                raise Exception("NO SIGNAL ERROR, signals empty.")
            calc = Calc()
            isMore = False
            for signal in self._signals:
                isMore = calc.calcSignalIsAfterMore(signal, resInfoSymbol, SIGNAL_BASECOIN)
                if isMore:
                    break
            return isMore
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsIsAfterMore: {resInfoSymbol=%s}, exception err=%s" % (
                'resInfoSymbol', err)
            raise CalcException(errStr)
