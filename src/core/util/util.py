# -*- coding: utf-8 -*-

import os
from src.core.db.db import DB
from src.core.config import Config
from src.core.util.log import Logger
from src.core.util.exceptions import DBException, ApplicationException

# util class
class Util(object):

    def __init__(self):
        self.logger = Logger()

    def init(self):
        try:
            db = DB()
            db.initDB()
            db.creatTables()
            db.creatViews()
        except DBException as err:
            errStr = "src.core.util.util.init: Critical. ApplicationException: Can Not Init File. %s" % err
            self.logger.critical(errStr)
            raise ApplicationException(errStr)
