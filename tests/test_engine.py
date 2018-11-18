# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.getcwd())

from src.core.util.util import Util
from src.core.engine.engine import Event, EventEngine
from tests.engine.test_listen import TestListen
from tests.engine.test_backtest import TestBacktest
from tests.engine.test_execute import TestExecute
from tests.engine.test_statistic import TestStatistic


# list of test_engine
# listen test items
test_listen = [
    # TestListen(""),
]
# backtest test items
test_backtest = [
    # TestBacktest(""),
]
# execute test items
test_execute = [
    # TestExecute(""),
]
# statistic test items
test_statistic = [
    # TestStatistic(""),
]

# Begin Test
if __name__ == '__main__':
    # Setup test fixtures
    util = Util()
    util.init()
    eventEngine = EventEngine()
    eventEngine.register()
    # Test
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_listen)
    suite.addTests(test_backtest)
    suite.addTests(test_execute)
    suite.addTests(test_statistic)
    # run test
    runner.run(suite)

    # Tear down test fixtures
