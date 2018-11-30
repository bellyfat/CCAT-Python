# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.getcwd())

from src.core.coin.huobi import Huobi
from src.core.config import Config
from src.core.util.log import Logger


# proxies
_proxies = Config()._Proxies_url if Config()._Proxies_proxies else None
# Huobi
_Huobi_exchange = Config()._Huobi_exchange
_Huobi_api_key = Config()._Huobi_api_key
_Huobi_api_secret = Config()._Huobi_api_secret
_Huobi_acct_id = Config()._Huobi_acct_id

huobi = Huobi(_Huobi_exchange, _Huobi_api_key, _Huobi_api_secret, _Huobi_acct_id,
            _proxies)
logger = Logger()


class TestHuobi(unittest.TestCase):
    def test_getConfig(self):
        res = huobi.getConfig()
        logger.debug(res)
        self.assertEqual(res["exchange"], _Huobi_exchange)

    def test_setProxy(self):
        huobi.setProxy(_proxies)
        res = huobi.getConfig()
        logger.debug(res)
        self.assertEqual(res["proxies"], _proxies)

    def test_getServerTime(self):
        res = huobi.getServerTime()
        logger.debug(res)
        self.assertIsInstance(res, int)



if __name__ == "__main__":
    unittest.main()
