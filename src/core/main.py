# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.engine.engine import Event, EventEngine
from src.core.util.util import Util
from src.core.util.log import Logger

# global var
__eventEngine = EventEngine()
__logger = Logger()


# Init App
def initAPP(self):
    self._logger.debug("src.core.main.initAPP")
    try:
        self.initDB()
        self.initDBInfo()
        self.initServerLimits()
    except ApplicationException as err:
        errStr = "src.core.main.initAPP: %s" % ApplicationException(err)
        self._logger.critical(errStr)
        raise ApplicationException(err)

# Update App
def updateAPP(self, listen):
    pass

# Begin Test
if __name__ == '__main__':
    # define var
    util = Util(__eventEngine)

    # app init
    util.initAPP()

    # app update
    util.updateDBAccount()
