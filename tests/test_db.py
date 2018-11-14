# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.getcwd())

from src.core.db.db import DB
from src.core.config import Config
from src.core.util.log import Logger

dbStr = os.path.join(os.getcwd(), Config()._db["url"])
db = DB(dbStr)
logger = Logger()

class TestDB(unittest.TestCase):

    def test_initDB(self):
        db.initDB()
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getTables(self):
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_setTables(self):
        db.setTables()
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

# list of test_db
# db test items
test_db = [
    TestDB("test_initDB"),
    TestDB("test_getTables"),
    TestDB("test_setTables"),
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_db)
    # run test
    runner.run(suite)
