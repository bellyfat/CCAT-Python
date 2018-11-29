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
def initAPP(util, sender):
    __logger.debug("src.core.main.initAPP")
    try:
        util.initDB()
        util.initDBInfo()
        util.initServerLimits()
        util.updateDBAccountBalance(sender)
        util.updateDBAccountWithdraw(sender)
        util.updateDBMarketKline(sender)
    except ApplicationException as err:
        errStr = "src.core.main.initAPP: %s" % ApplicationException(err)
        __logger.critical(errStr)
        raise ApplicationException(err)

# Update App
def updateAPP(util, sender):
    __logger.debug("src.core.main.initAPP")
    try:
        util.initServerLimits()
        util.updateDBMarketKline(sender)
    except ApplicationException as err:
        errStr = "src.core.main.initAPP: %s" % ApplicationException(err)
        __logger.critical(errStr)
        raise ApplicationException(err)

# Begin Test
if __name__ == '__main__':
    # define var
    util = Util()
    sender = Sender(__eventEngine)
    handler = Handler(sender)
    register = Register(__eventEngine, handler)

    # app
    pass
