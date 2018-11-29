# -*- coding: utf-8 -*-

from multiprocessing import Manager, Value

import pandas as pd

from src.core.engine.enums import (HIGH_PRIORITY_EVENT,
                                   HIGH_PRIORITY_EVENT_TIMEOUT,
                                   LOW_PRIORITY_EVENT,
                                   LOW_PRIORITY_EVENT_TIMEOUT,
                                   MEDIUM_PRIORITY_EVENT,
                                   MEDIUM_PRIORITY_EVENT_TIMEOUT)
from src.core.util.exceptions import EngineException
from src.core.util.log import Logger


class Status(object):
    def __init__(self):
        # Status ID
        self._id = Value('i', 0)
        self._status = Manager().list()
        # logger
        self._logger = Logger()

    def getStatusTable(self):
        res = [item for item in self._status]
        if res!=[]:
            res = pd.DataFrame(res).set_index(["id"], inplace=False)
        self._logger.debug("src.core.engine.status.Status.getStatusTable:\n\t%s" % res)
        return res

    def calcEventID(self):
        self._id.value = self._id.value + 1
        self._logger.debug("src.core.engine.status.Status.calcEventID: { id=%s}" % self._id.value)
        return self._id.value

    def calcActiveEventNum(self):
        num = len(self._status)
        self._logger.debug("src.core.engine.status.Status.calcActiveEventNum: { num=%s}" % num)
        return num

    def addEventStatus(self, event):
        self._logger.info(
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
        self._status.append(item)

    def delEventStatus(self, event):
        self._logger.info(
            "src.core.engine.status.Status.delEventStatus: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        for item in self._status:
            if item["id"] == event.id:
                self._status.remove(item)
