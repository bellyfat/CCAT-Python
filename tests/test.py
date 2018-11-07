# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

# Begin Test
if __name__ == '__main__':
    # 1. unit test for test_coin
    print("\033[0;33;40m\n1. python3 -m unittest tests/test_coin.py\n\033[0m")
    os.system("python3 -m unittest tests/test_coin.py")
