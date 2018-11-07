# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from tests.test_coin import TestCoin

if __name__ == '__main__':
    # Begin Test
    # 1. unit test for test_coin
    print("1. unit test for test_coin")
    testCoin = TestCoin()
    testCoin.run()
