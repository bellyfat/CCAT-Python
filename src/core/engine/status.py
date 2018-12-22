# -*- coding: utf-8 -*-

from multiprocessing import Manager, Value

from src.core.config import Config
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
        return self._activeStatus

    def getDoneStatusTable(self):
        self._logger.debug(
            "src.core.engine.status.Status.getDoneStatusTable")
        return self._doneStatus

    def calcEventID(self):
        self._logger.debug(
            "src.core.engine.status.Status.calcEventID")
        self._id.value = self._id.value + 1
        return self._id.value

    def calcActiveEventNum(self):
        self._logger.debug(
            "src.core.engine.status.Status.calcActiveEventNum")
        num = len(self._activeStatus)
        return num

    def addEventStatus(self, id):
        self._logger.debug(
            "src.core.engine.status.Status.addEventStatus: {id=%s}"
            % id)
        if not id in self._activeStatus:
            self._activeStatus.append(id)

    def delEventStatus(self, id):
        self._logger.debug(
            "src.core.engine.status.Status.delEventStatus: {id=%s}"
            % id)
        if id in self._activeStatus:
            self._activeStatus.remove(id)
        if not id in self._doneStatus:
            if len(self._doneStatus) < self._cachesize:
                self._doneStatus.append(id)
            else:
                self._doneStatus.pop(0)
                self._doneStatus.append(id)
