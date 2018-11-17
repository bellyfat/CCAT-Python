# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.util.log import Logger

logger = Logger()

# Begin Test
if __name__ == '__main__':
    # 1. unit test for test_coin
    # logger.info("1. testing... python3 tests/test_coin.py")
    # os.system("python3 tests/test_coin.py")

    # 2. unit test for test_db
    # logger.info("2. testing... python3 tests/test_db.py")
    # os.system("python3 tests/test_db.py")

    # 3. unit test for test_engine
    logger.info("2. testing... python3 tests/test_engine.py")
    os.system("python3 tests/test_engine.py")
