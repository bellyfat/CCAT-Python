# -*- coding: utf-8 -*-

from src.core.db.db import DB
from src.core.util.log import Logger

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
            errStr = "%s/n, Application Error. Can Not Init File." % err
            self.logger.critical(errStr)
            raise DBException
