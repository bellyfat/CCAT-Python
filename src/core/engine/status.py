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
from src.core.util.helper import utcnow_timestamp
from src.core.util.log import Logger


class Status(object):
    def __init__(self):
        # Status ID
        self.ID = Value('i', 0)
        # columns = ["id", "type", "priority", "timeStamp", "args", "creat", "start", "end"]
        self._status = Manager().list()
        # logger
        self._logger = Logger()

    def addEventStatus(self, event):
        self._logger.info(
            "src.core.engine.status.Status.addEventStatus: {type:%s, priority:%s, timeStamp:%s, argss:%s}"
            % (event.type, event.priority, event.timeStamp, event.args))
        self.ID.value = self.ID.value + 1
        item = {
            "id": self.ID.value,
            "type": event.type,
            "priority": event.priority,
            "timeStamp": event.timeStamp,
            "args": event.args,
            "creat": utcnow_timestamp(),
            "start": '',
            "end": ''
        }
        self._status.append(item)

    def updateEventStatus(self, event):
        self._logger.info(
            "src.core.engine.status.Status.updateEventStatus: {type:%s, priority:%s, timeStamp:%s, argss:%s}"
            % (event.type, event.priority, event.timeStamp, event.args))
        for item in self._status:
            pass

    def delEventStatus(self, event):
        self._logger.info(
            "src.core.engine.status.Status.delEventStatus: {type:%s, priority:%s, timeStamp:%s, argss:%s}"
            % (event.type, event.priority, event.timeStamp, event.args))
        pass
