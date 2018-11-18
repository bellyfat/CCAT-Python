# -*- coding: utf-8 -*-

import os
import sys
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

    def test_sendListenDepthEvent(self):
        logger.debug("test_sendListenDepthEvent")
        self.listen.sendListenDepthEvent("all", "ETH", "USDT", 10)
        res = self.db.getMarketDepth()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_sendListenKlineEvent(self):
        logger.debug("test_sendListenKlineEvent")
        self.listen.sendListenKlineEvent("all", "BTC", "USDT", "1m",
                                         "2018-11-17T00:00:00.000Z",
                                         "2018-11-17T01:00:00.000Z")
        res = self.db.getMarketKline()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_sendListenTickerEvent(self):
        logger.debug("test_sendListenTickerEvent")
        self.listen.sendListenTickerEvent("all", "BTC", "USDT")
        res = self.db.getMarketTicker()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def tearDown(self):
        logger.debug("tearDown")
        self.eventEngine.stop()
        # self.eventEngine.terminate()
        self.listen.unregisterListenEvent()
