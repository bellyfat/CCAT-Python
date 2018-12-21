# -*- coding: utf-8 -*-

import json
import ast
from src.core.coin.enums import TYPE_DIS, TYPE_TRA, TYPE_PAIR

class Signal(object):
    def __init__(self, signals):
        self._str = signals
        self._signals = []

    def signals(self):
        strList = ast.literal_eval(self._str)
        signals = []
        for str in strList:
            signals.append(json.loads(str))

        for s in signals:
            if s["type"] == TYPE_DIS:

            if s["type"] == TYPE_TRA:
            if s["type"] == TYPE_PAIR:
