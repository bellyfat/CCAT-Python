# -*- coding: utf-8 -*-

import json

class Config(object):
    def _init_(self):
        self._confStr = "./config"
        with open(self._confStr,'r') as f:
            jsonStr = json.load(f)
        print(jsonStr)
        self._proxies = json.loads(jsonStr.proxies)
        self._okex = json.loads(json.dump(jsonStr.okex))
        self._binance = json.loads(jsonStr.binance)
        self._huobi = json.loads(json.dump(jsonStr.huobi))
        self._gate = json.loads(json.dump(jsonStr.gate))
