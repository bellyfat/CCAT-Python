# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from src.core.util.log import Logger

logger = Logger()

# Begin Test
if __name__ == '__main__':
    # 1. integration test for test_listen
    logger.info("3.1 sub testing... python3 tests/engine/test_listen.py")
    os.system("python3 tests/engine/test_listen.py")

    # 2. integration test for test_judge
    logger.info("3.2 sub testing... python3 tests/engine/test_judge.py")
    os.system("python3 tests/engine/test_judge.py")

    # 3. integration test for test_backtest
    logger.info("3.3 sub testing... python3 tests/engine/test_backtest.py")
    os.system("python3 tests/engine/test_backtest.py")

    # 4. integration test for test_execute
    logger.info("3.4 sub testing... python3 tests/engine/test_execute.py")
    os.system("python3 tests/engine/test_execute.py")

    # 5. integration test for test_statistic
    logger.info("3.5 sub testing... python3 tests/engine/test_statistic.py")
    os.system("python3 tests/engine/test_statistic.py")
