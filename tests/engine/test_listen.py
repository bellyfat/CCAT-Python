# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.getcwd())

from src.core.engine.listen import Listen
from src.core.engine.engine import Event, EventEngine
from src.core.config import Config
from src.core.util.util import Util
from src.core.util.log import Logger

# global var
util = Util()
eventEngine = EventEngine()
listenCof = Config()._listen
logger = Logger()

class TestListen(unittest.TestCase):
    def setUp(self):
        util.init()
        self.listen = Listen(eventEngine)
        self.listen.registerListenEvent()
        eventEngine.start()

    def test_depthEvent(self):
        listen = Listen(eventEngine)
        listen.sendListenDepthEvent()

    def test_klineEvent(self):
        listen = Listen(eventEngine)
        listen.sendListenKlineEvent()

    def test_tickerEvent(self):
        listen = Listen(eventEngine)
        listen.sendListenTickerEvent()

    def tearDown(self):
        eventEngine.terminate()
        self.listen.unregisterListenEvent()
