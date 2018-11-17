# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.getcwd())


from src.core.config import Config
from src.core.util.log import Logger

class TestExecute(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
