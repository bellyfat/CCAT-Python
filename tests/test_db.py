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

    def test_creatTables(self):
        db.creatTables()
        res = db.getTables()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getServerInfo(self):
        res = db.getServerInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertServerInfo(self):
        db.insertServerInfo()
        res = db.getServerInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getSymbolInfo(self):
        res = db.getSymbolInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertSymbolInfo(self):
        db.insertSymbolInfo()
        res = db.getSymbolInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getAccountInfo(self):
        res = db.getAccountInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertAccountInfo(self):
        db.insertAccountInfo()
        res = db.getAccountInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_getWithdrawInfo(self):
        res = db.getWithdrawInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

    def test_insertWithdrawInfo(self):
        db.insertWithdrawInfo()
        res = db.getWithdrawInfo()
        logger.debug(res)
        self.assertIsInstance(res, list)

# list of test_db
# db test items
test_db = [
    TestDB("test_initDB"),
    TestDB("test_getTables"),
    TestDB("test_creatTables"),
    TestDB("test_getServerInfo"),
    TestDB("test_insertServerInfo"),
    TestDB("test_getSymbolInfo"),
    # TestDB("test_insertSymbolInfo"),
    TestDB("test_getAccountInfo"),
    TestDB("test_insertAccountInfo"),
    TestDB("test_getWithdrawInfo"),
    TestDB("test_insertWithdrawInfo"),
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    # add tests
    suite.addTests(test_db)
    # run test
    runner.run(suite)
