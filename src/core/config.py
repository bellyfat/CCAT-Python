# -*- coding: utf-8 -*-
import os
import json


class Config(object):

    _confStr = os.path.join(os.getcwd(),"config")
    _proxies = ""
    _okex = ""
    _binance = ""
    _huobi = ""
    _gate = ""

    def __init__(self):
        with open(Config._confStr, 'r') as f:
            jsonStr = json.load(f)
        Config._db = jsonStr["db"]
        Config._proxies = jsonStr["proxies"]
        Config._okex = jsonStr["okex"]
        Config._binance = jsonStr["binance"]
        Config._huobi = jsonStr["huobi"]
        Config._gate = jsonStr["gate"]
