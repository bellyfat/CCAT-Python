# -*- coding: utf-8 -*-

import hashlib
import json
import unittest

from src.core.coin.lib.okex import Okex
from src.core.config import Config
from src.core.util.log import Logger

logger = Logger()


class TestOkex(unittest.TestCase):

    def test_getConfig(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getConfig()
        # logger.debug(res)
        self.assertEqual(res["exchange"], okexConf["exchange"])
        self.assertEqual(res["api_key"], okexConf["api_key"])
        self.assertEqual(res["api_secret"], okexConf["api_secret"])
        self.assertEqual(res["proxies"], proxies["url"])

    def test_setProxy(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"])
        okex.setProxy(proxies["url"])
        res = okex.getConfig()
        # logger.debug(res)
        self.assertEqual(res["proxies"], proxies["url"])

    def test_getServerTime(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getServerTime(proxies["url"])
        # logger.debug(res)
        self.assertIsInstance(res, str)

    def test_getServerLimits(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getServerLimits()
        # logger.debug(type(res))
        self.assertIsInstance(res, list)


    def test_getServerSymbols(self):
        proxies = Config()._proxies
        okexConf = Config()._okex
        okex = Okex(okexConf["exchange"], okexConf["api_key"],
                    okexConf["api_secret"], okexConf["passphrase"], proxies["url"])
        res = okex.getServerSymbols()
        # logger.debug(type(res))
        self.assertIsInstance(res, dict)
