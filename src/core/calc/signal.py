# -*- coding: utf-8 -*-

import ast
import json

from src.core.engine.enums import SIGNAL_SIGNALS, TYPE_DIS, TYPE_PAIR, TYPE_TRA
from src.core.util.exceptions import CalcException
from src.core.util.helper import tuple_str_to_list
from src.core.util.log import Logger


class Signal(object):
    def __init__(self):
        self._signals = []
        self._signals_str = SIGNAL_SIGNALS
        self._logger = Logger()

    def signals(self, types='all'):
        self._logger.debug("src.core.calc.signal.Signal.signals")
        try:
            strList = ast.literal_eval(self._signals_str)
            for s in strList:
                type_arg = {}
                signal = {}
                if types == 'all' or TYPE_DIS in types:
                    if s['type'] == TYPE_DIS:
                        type_arg['bid_server'] = s['type_arg']['bid_server']
                        type_arg['ask_server'] = s['type_arg']['ask_server']
                        type_arg['fSymbol'] = s['type_arg']['fSymbol']
                        type_arg['tSymbol'] = s['type_arg']['tSymbol']
                        signal['type'] = s['type']
                        signal['type_arg'] = type_arg
                        signal['base_start'] = float(s['base_start'])
                        signal['base_gain'] = float(s['base_gain'])
                        signal['timeout'] = float(s['timeout'])
                if types == 'all' or TYPE_TRA in types:
                    if s['type'] == TYPE_TRA:
                        tuple = tuple_str_to_list(s['type_arg']['symbol_pair'])
                        type_arg['server'] = s['type_arg']['server']
                        type_arg['V1_fSymbol'] = tuple[0][0]
                        type_arg['V1_tSymbol'] = tuple[0][1]
                        type_arg['V2_fSymbol'] = tuple[1][0]
                        type_arg['V2_tSymbol'] = tuple[1][1]
                        type_arg['V3_fSymbol'] = tuple[2][0]
                        type_arg['V3_tSymbol'] = tuple[2][1]
                        signal['type'] = s['type']
                        signal['type_arg'] = type_arg
                        signal['base_start'] = float(s['base_start'])
                        signal['base_gain'] = float(s['base_gain'])
                        signal['timeout'] = float(s['timeout'])
                if types == 'all' or TYPE_PAIR in types:
                    if s['type'] == TYPE_PAIR:
                        tuple = tuple_str_to_list(s['type_arg']['symbol_pair'])
                        type_arg['J1_server'] = s['type_arg']['J1_server']
                        type_arg['J2_server'] = s['type_arg']['J2_server']
                        type_arg['V1_fSymbol'] = tuple[0][0]
                        type_arg['V1_tSymbol'] = tuple[0][1]
                        type_arg['V2_fSymbol'] = tuple[1][0]
                        type_arg['V2_tSymbol'] = tuple[1][1]
                        type_arg['V3_fSymbol'] = tuple[2][0]
                        type_arg['V3_tSymbol'] = tuple[2][1]
                        signal['type'] = s['type']
                        signal['type_arg'] = type_arg
                        signal['base_start'] = float(s['base_start'])
                        signal['base_gain'] = float(s['base_gain'])
                        signal['timeout'] = float(s['timeout'])
                if not signal == {}:
                    self._signals.append(signal)
            # return signals
            return self._signals
        except Exception as err:
            errStr = "src.core.calc.signal.Signal.signals, exception err=%s" % err
            raise CalcException(errStr)
