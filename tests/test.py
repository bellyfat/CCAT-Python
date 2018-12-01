# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.util.log import Logger

logger = Logger()

# Begin Test
if __name__ == '__main__':
    # 1. unit test for test_coin
    logger.debug("1. unit testing... python3 tests/test_coin.py")
    os.system("python3 tests/test_coin.py")

    # 2. unit test for test_db
    logger.debug("2. unit testing... python3 tests/test_db.py")
    os.system("python3 tests/test_db.py")

    # 3. integration test for test_engine
    logger.debug("3. intergration testing... python3 tests/test_engine.py")
    os.system("python3 tests/test_engine.py")

    # # 4. system test for test_main
    logger.debug("4. system testing... python3 tests/test_main.py")
    os.system("python3 tests/test_main.py")
