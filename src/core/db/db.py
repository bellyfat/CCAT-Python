# -*- coding: utf-8 -*-

import os
import sqlite3

from src.core.db.sql import *
from src.core.config import Config
from src.core.util.exceptions import DBException

# db class
class DB(object):
    def __init__(self, dbStr):
        self.dbStr = dbStr
        self.conn = sqlite3.connect(dbStr)

    def __del__(self):
        self.conn.close()

    def initDB(self):
        try:
            self.conn.close()
            os.remove(self.dbStr)
            self.conn = sqlite3.connect(self.dbStr)
        except IOError as err:
            raise DBException

    def getTables(self):
        try:
            curs = self.conn.cursor()
            curs.execute(GET_TABLES_SQL)
            tables = curs.fetchall()
            curs.close()
        except sqlite3.Error as err:
            raise DBException
        return tables

    def setTables(self):
        try:
            curs = self.conn.cursor()
            curs.executescript(CREATE_TABELS_SQL)
            curs.close()
        except sqlite3.Error as err:
            raise DBException
