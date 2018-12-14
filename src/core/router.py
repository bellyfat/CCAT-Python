# -*- coding: utf-8 -*-

from src.core.engine.engine import EventEngine
from src.core.engine.handler import Handler
from src.core.engine.register import Register
from src.core.engine.sender import Sender
from src.core.util.exceptions import RouterException, UtilException
from src.core.util.log import Logger
from src.core.util.util import Util


class Router(object):
    def __init__(self):
        self._logger = Logger()

    def initAPP(self):
