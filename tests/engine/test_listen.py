# -*- coding: utf-8 -*-

from src.core.util.log import Logger
from src.core.util.util import Util
from src.core.db.db import DB
from src.core.config import Config
from src.core.engine.engine import Event, EventEngine
from src.core.engine.listen import Listen
import os
import sys
import unittest
sys.path.append(os.getcwd())

# global var
logger = Logger()
listenCof = Config()._listen
dbStr = os.path.join(os.getcwd(), Config()._db["url"])


class TestListen(unittest.TestCase):
    def setUp(self):
        logger.debug("setUp")
        util = Util()
        util.init()
        self.db = DB()
        self.eventEngine = EventEngine()
        self.listen = Listen(self.eventEngine)
        self.listen.registerListenEvent()
        self.eventEngine.start()

    def test_listenEvent(self):
        logger.debug("test_listenEvent")
        self.listen.sendListenDepthEvent("all", "ETH", "USDT", 10)
        # self.listen.sendListenKlineEvent("all", "BTC", "USDT", "1m", "2018-11-17T00:00:00.000Z", "2018-11-17T01:00:00.000Z")
        # self.listen.sendListenTickerEvent("all", "BTC", "USDT")
        res = self.db.getMarketDepth()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def tearDown(self):
        logger.debug("tearDown")
        self.eventEngine.stop()
        self.listen.unregisterListenEvent()
        self.eventEngine.terminate()
