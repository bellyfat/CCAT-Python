# -*- coding: utf-8 -*-

import ast
import json

from src.core.calc.calc import Calc
from src.core.calc.enums import SIGNAL_AUTO, SIGNAL_BASECOIN, SIGNAL_SIGNALS
from src.core.engine.enums import TYPE_DIS, TYPE_PAIR, TYPE_TRA
from src.core.util.exceptions import CalcException
from src.core.util.helper import tuple_str_to_list
from src.core.util.log import Logger


class Signal(object):
    def __init__(self, signals=[]):
        # signal init
        self._signals = signals
        self._signals_str = SIGNAL_SIGNALS
        # logger
        self._logger = Logger()

    def signals(self, exchange='all', types='all', auto=SIGNAL_AUTO):
        self._logger.debug("src.core.calc.signal.Signal.signals")
        try:
            if not self._signals == []:
                return self._signals
            if auto:
                return self._autoSignals(exchange, types)
            if not auto:
                return self._configSignals(exchange, types)
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.signals, exception err=%s" % err
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
            for s in strList:
                signal = {}
                if s['type'] == TYPE_DIS:
                    if (types == 'all' or TYPE_DIS in types) and (
                            exchange == 'all' or
                        (s['bid_server'] in exchange
                         and s['ask_server'] in exchange)):
                        signal['type'] = s['type']
                        signal['bid_server'] = s['bid_server']
                        signal['ask_server'] = s['ask_server']
                        signal['fSymbol'] = s['fSymbol']
                        signal['tSymbol'] = s['tSymbol']
                        signal['group_id'] = str(s['group_id'])
                        signal['forward_ratio'] = float(s['forward_ratio'])
                        signal['backward_ratio'] = float(s['backward_ratio'])
                        signal['base_start'] = float(s['base_start'])
                        signal['base_gain'] = float(s['base_gain'])
                        signal['base_timeout'] = float(s['base_timeout'])
                        signal['status_done'] = False
                        signal['status_assets'] = [{
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
                if s['type'] == TYPE_TRA:
                    if (types == 'all' or TYPE_TRA in types) and (
                            exchange == 'all' or s['server'] in exchange):
                        tuple = tuple_str_to_list(s['symbol_pair'])
                        signal['type'] = s['type']
                        signal['server'] = s['server']
                        signal['V1_fSymbol'] = tuple[0][0]
                        signal['V1_tSymbol'] = tuple[0][1]
                        signal['V2_fSymbol'] = tuple[1][0]
                        signal['V2_tSymbol'] = tuple[1][1]
                        signal['V3_fSymbol'] = tuple[2][0]
                        signal['V3_tSymbol'] = tuple[2][1]
                        signal['group_id'] = str(s['group_id'])
                        signal['base_start'] = float(s['base_start'])
                        signal['base_gain'] = float(s['base_gain'])
                        signal['base_timeout'] = float(s['base_timeout'])
                        signal['status_done'] = False
                        signal['status_assets'] = [{
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
                        signal['type'] = s['type']
                        signal['J1_server'] = s['J1_server']
                        signal['J2_server'] = s['J2_server']
                        signal['V1_fSymbol'] = tuple[0][0]
                        signal['V1_tSymbol'] = tuple[0][1]
                        signal['V2_fSymbol'] = tuple[1][0]
                        signal['V2_tSymbol'] = tuple[1][1]
                        signal['V3_fSymbol'] = tuple[2][0]
                        signal['V3_tSymbol'] = tuple[2][1]
                        signal['group_id'] = str(s['group_id'])
                        signal['base_start'] = float(s['base_start'])
                        signal['base_gain'] = float(s['base_gain'])
                        signal['base_timeout'] = float(s['base_timeout'])
                        signal['status_done'] = False
                        signal['status_assets'] = [{
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
                if not signal == {}:
                    signals.append(signal)
            # return signals
            return signals
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.signals, exception err=%s" % err
            raise CalcException(errStr)

    def _updateSignalsStatusByOrders(self, orders):
        pass

    def backtestUpdateSignalStatusByOrders(self, orders):
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
                orders = calc.calcSignalPreTradeOrders(
                    signal['group_id'], signal, resInfoSymbol, SIGNAL_BASECOIN)
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
            isDone = True
            return (res, isDone)
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsRunTrade: {resInfoSymbol=%s}, exception err=%s" % (
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
            return res
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.backtestSignalsAfterTrade: {resInfoSymbol=%s}, exception err=%s" % (
                'resInfoSymbol', err)
            raise CalcException(errStr)
