# -*- coding: utf-8 -*-

import os
import sys
import time
import unittest
sys.path.append(os.getcwd())

from src.core.config import Config
from src.core.db.db import DB
from src.core.engine.engine import Event, EventEngine
from src.core.engine.listen import Listen
from src.core.util.log import Logger

# global var
logger = Logger()
listenCof = Config()._listen


class TestListen(unittest.TestCase):
    def setUp(self):
        logger.debug("setUp")
        self.db = DB()
        self.eventEngine = EventEngine()
        self.listen = Listen(self.eventEngine)
        self.listen.registerListenEvent()
        self.eventEngine.start()

    def test_sendListenEvent(self):
        logger.debug("test_sendListenEvent")
        # sendListenDepthEvent
        self.listen.sendListenDepthEvent("all", "ETH", "USDT", 10)
        # sendListenKlineEvent
        self.listen.sendListenKlineEvent("all", "ETH", "USDT", "1m",
                                         "2018-11-18T00:00:00.000Z",
                                         "2018-11-18T01:00:00.000Z")
        # sendListenTickerEvent
        self.listen.sendListenTickerEvent("all", "ETH", "USDT")
        # 等待新进程运行完毕
        time.sleep(5)
        # result
        res = self.db.getMarketDepth()
        logger.debug(res)
        self.assertIsInstance(res, list)
        res = self.db.getMarketKline()
        logger.debug(res)
        self.assertIsInstance(res, list)
        res = self.db.getMarketTicker()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def tearDown(self):
        logger.debug("tearDown")
        self.eventEngine.stop()
        # self.eventEngine.terminate()
        self.listen.unregisterListenEvent()
