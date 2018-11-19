# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.util.util import Util
from src.core.util.log import Logger

util = Util()
logger = Logger()

# Begin Test
if __name__ == '__main__':
    # app init
    util.initAPP()
