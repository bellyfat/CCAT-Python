# -*- coding: utf-8 -*-

import sqlite3

from src.core.db.sql import *

# db class
class DB(object):
    def __init__(self, dbStr):
        self.conn = sqlite3.connect(dbStr)

    def 
