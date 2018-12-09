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
        res = [item["id"] for item in self._activeStatus]
        self._logger.debug(
            "src.core.engine.status.Status.getActiveStatusTable: {res=%s }" %
            res)
        return res

    def getDoneStatusTable(self):
        res = [item["id"] for item in self._doneStatus]
        self._logger.debug(
            "src.core.engine.status.Status.getDoneStatusTable: {res=%s }" % res)
        return res

    def calcEventID(self):
        self._id.value = self._id.value + 1
        self._logger.debug(
            "src.core.engine.status.Status.calcEventID: { id=%s }" %
            self._id.value)
        return self._id.value

    def calcActiveEventNum(self):
        num = len(self._activeStatus)
        self._logger.debug(
            "src.core.engine.status.Status.calcActiveEventNum: { num=%s}" %
            num)
        return num

    def addEventStatus(self, event):
        self._logger.debug(
            "src.core.engine.status.Status.addEventStatus: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        item = {
            "id": event.id,
            "type": event.type,
            "priority": event.priority,
            "timeStamp": event.timeStamp,
            "args": event.args
        }
        self._activeStatus.append(item)

    def delEventStatus(self, event):
        self._logger.debug(
            "src.core.engine.status.Status.delEventStatus: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        for item in self._activeStatus:
            if item["id"] == event.id:
                self._activeStatus.remove(item)
                if len(self._doneStatus) < self._cachesize:
                    self._doneStatus.append(item)
                else:
                    self._doneStatus.pop(0)
                    self._doneStatus.append(item)
