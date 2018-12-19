# -*- coding: utf-8 -*-

import os
import sys
import time
sys.path.append(os.getcwd())

from src.core.router import Router
from src.core.util.log import Logger

# global var
__Router = Router()
__logger = Logger()

# Begin Test
if __name__ == '__main__':
    # exec time
    start = time.time()

    # start
    __Router.start()

    # app init
    __Router.initAPP()

    # app update
    __Router.updateAPP(0)

    # stop
    __Router.stop()

    # exec time
    end = time.time()
    __logger.info("tests.test_router finished in %0.3fs" % float(end-start))
