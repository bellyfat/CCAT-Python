# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.util.log import Logger

logger = Logger()

# Begin Test
if __name__ == '__main__':
    # 1. unit test for test_coin
    logger.info("1. testing... python3 tests/test_coin.py")
    os.system("python3 tests/test_coin.py")
