# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.engine.engine import EventEngine
from src.core.engine.listen import Listen, ListenHandler
from src.core.util.util import Util
from src.core.util.log import Logger

# global var
__eventEngine = EventEngine()
__logger = Logger()

# Begin Test
if __name__ == '__main__':
    # clase instanse
    util = Util()
    listen = Listen(__eventEngine)
    listenHandler = ListenHandler()

    # app init
    util.initAPP()
    util.initServerLimits()

    # constant var

    # register engine
    listen.registerListenEvent(listenHandler)

    # start engine
    __eventEngine.start()

    # app update
    util.updateDBAccount(listen)
