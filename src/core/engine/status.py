# -*- coding: utf-8 -*-

from multiprocessing import Manager, Value

from src.core.config import Config
from src.core.util.exceptions import EngineException
from src.core.util.log import Logger


class Status(object):
    def __init__(self):
        # Status ID
        self._id = Value('i', 0)
        self._activeStatus = Manager().list()
        self._doneStatus = Manager().list()
        self._cachesize = Config()._Engine_cacheSize
        # logger
        self._logger = Logger()

    def getActiveStatusTable(self):
        self._logger.debug(
            "src.core.engine.status.Status.getActiveStatusTable")
        try:
            return self._activeStatus
        except Exception as err:
            raise (EngineException(err))

    def getDoneStatusTable(self):
        self._logger.debug("src.core.engine.status.Status.getDoneStatusTable")
        try:
            return self._doneStatus
        except Exception as err:
            raise (EngineException(err))

    def calcEventID(self):
        self._logger.debug("src.core.engine.status.Status.calcEventID")
        try:
            self._id.value = self._id.value + 1
            return self._id.value
        except Exception as err:
            raise (EngineException(err))

    def calcActiveEventNum(self):
        self._logger.debug("src.core.engine.status.Status.calcActiveEventNum")
        try:
            num = len(self._activeStatus)
            return num
        except Exception as err:
            raise (EngineException(err))

    def addEventStatus(self, id):
        self._logger.debug(
            "src.core.engine.status.Status.addEventStatus: {id=%s}" % id)
        try:
            if id not in self._activeStatus:
                self._activeStatus.append(id)
        except Exception as err:
            raise (EngineException(err))

    def delEventStatus(self, id):
        self._logger.debug(
            "src.core.engine.status.Status.delEventStatus: {id=%s}" % id)
        try:
            if id in self._activeStatus:
                self._activeStatus.remove(id)
            if id not in self._doneStatus:
                if len(self._doneStatus) < self._cachesize:
                    self._doneStatus.append(id)
                else:
                    self._doneStatus.pop(0)
                    self._doneStatus.append(id)
        except Exception as err:
            raise (EngineException(err))
