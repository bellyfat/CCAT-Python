# -*- coding: utf-8 -*-

import sqlite3

from src.core.db.sql import *
from src.core.config import Config

# db class
class DB(object):
    def __init__(self, dbStr):
        self.conn = sqlite3.connect(dbStr)

    def __del__(self):
        self.conn.close()

    def get_tables(self):
        curs = self.conn.cursor()
        curs.execute(GET_TABLES_SQL)
        return curs.fetchall()
