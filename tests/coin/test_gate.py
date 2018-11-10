# -*- coding: utf-8 -*-

import hashlib
import json
import os
import sys
import unittest

sys.path.append(os.getcwd())

from src.core.coin.lib.binance import Binance
from src.core.config import Config
from src.core.util.log import Logger


logger = Logger()


class TestGate(unittest.TestCase):

    def test_getConfig(self):
        pass


if __name__ == "__main__":
    unittest.main()
