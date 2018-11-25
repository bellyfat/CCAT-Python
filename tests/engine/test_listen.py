# -*- coding: utf-8 -*-

import os
import sys
import time
sys.path.append(os.getcwd())

from src.core.engine.engine import EventEngine
from src.core.engine.register import Register
from src.core.engine.sender import Sender
from src.core.engine.handler import Handler
from src.core.util.util import Util
from src.core.util.log import Logger

# global var
__eventEngine = EventEngine()
__logger = Logger()

# Begin Test
if __name__ == '__main__':
    # exec time
    start = time.time()
    # clase instanse
    util = Util()
    sender = Sender(__eventEngine)
    handler = Handler(sender)
    register = Register(__eventEngine, handler)

    # app init
    util.initDB()
    util.initDBInfo()
    util.initServerLimits()

    # register engine
    register.register()

    # start engine
    __eventEngine.start()

    # app update
    util.updateDBAccountBalance(sender)
    util.updateDBAccountWithdraw(sender)
    util.updateDBMarketKline(sender)
    util.updateDBMarketTicker(sender)


    # stop engine
    time.sleep(2) # for engine begin handle
    __eventEngine.stop()

    # unregister engine
    register.unregister()

    # exec time
    end = time.time()
    __logger.debug("tests.engine.test_listen finished in %0.3fs" % float(end-start))
