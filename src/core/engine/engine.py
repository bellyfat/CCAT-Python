# -*- coding: utf-8 -*-

import time
from multiprocessing import Process, Queue, Value

from src.core.config import Config
from src.core.engine.enums import (ACTIVE_STATUS_EVENT, DONE_STATUS_EVENT,
                                   HIGH_PRIORITY_EVENT,
                                   HIGH_PRIORITY_EVENT_TIMEOUT,
                                   LOW_PRIORITY_EVENT,
                                   LOW_PRIORITY_EVENT_TIMEOUT,
                                   MEDIUM_PRIORITY_EVENT,
                                   MEDIUM_PRIORITY_EVENT_TIMEOUT,
                                   QUEUE_STATUS_EVENT)
from src.core.engine.status import Status
from src.core.util.exceptions import EngineException
from src.core.util.helper import utcnow_timestamp
from src.core.util.log import Logger


class EventEngine(object):
    # 初始化事件事件驱动引擎
    def __init__(self):
        # Config init
        self.__epoch = Config()._Engine_epoch
        self.__maxProcess = Config()._Engine_maxProcess
        # 保存事件列表 按优先级不同分别保存
        self.__lowEnventQueue = Queue()
        self.__mediumEventQueue = Queue()
        self.__highEventQueue = Queue()
        # 引擎开关
        self.__active = Value('b', False)
        # 事件处理字典{'event1': [handler1,handler2] , 'event2':[handler3, ...,handler4]}
        self.__handlers = {}
        # 保存事件处理进程池 控制最大进程数量 以及关闭引擎时处理已启动进程
        self.__processPool = []
        # 保存已执行事件处理状态
        self.__status = Status()
        # 事件引擎主进程
        self.__mainProcess = None  # Process(target=self.__run)
        # logger
        self.__logger = Logger()

    # 执行事件循环
    def __run(self):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run")
        while self.__active.value:
            # 执行 Epoch
            time.sleep(self.__epoch)
            # 控制最大进程数量
            if self.__status.calcActiveEventNum() > int(self.__maxProcess):
                self.__logger.warn(
                    "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: Too Many"
                )
            else:
                # 按优先级 获取队列中的事件 超时1秒
                event = None
                if not self.__highEventQueue.empty():
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__highEventQueue"
                    )
                    event = self.__highEventQueue.get(block=False)
                    while utcnow_timestamp(
                    ) - event.timeStamp > HIGH_PRIORITY_EVENT_TIMEOUT:
                        if not self.__highEventQueue.empty():
                            self.__logger.warn(
                                "src.core.engine.engine.EventEngine.__mainProcess.__run.__highEventQueue TIMEOUT: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
                                % (event.id, event.type, event.priority,
                                   event.timeStamp, event.args))
                            event = self.__highEventQueue.get(block=False)
                        else:
                            event = None
                            break

                if not self.__mediumEventQueue.empty() and event == None:
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__mediumEventQueue"
                    )
                    event = self.__mediumEventQueue.get(block=False)
                    while utcnow_timestamp(
                    ) - event.timeStamp > MEDIUM_PRIORITY_EVENT_TIMEOUT:
                        if not self.__mediumEventQueue.empty():
                            self.__logger.warn(
                                "src.core.engine.engine.EventEngine.__mainProcess.__run.__mediumEventQueue TIMEOUT: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
                                % (event.id, event.type, event.priority,
                                   event.timeStamp, event.args))
                            event = self.__mediumEventQueue.get(block=False)
                        else:
                            event = None
                            break

                if not self.__lowEnventQueue.empty() and event == None:
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__lowEnventQueue"
                    )
                    event = self.__lowEnventQueue.get(block=False)
                    while utcnow_timestamp(
                    ) - event.timeStamp > LOW_PRIORITY_EVENT_TIMEOUT:
                        if not self.__lowEnventQueue.empty():
                            self.__logger.warn(
                                "src.core.engine.engine.EventEngine.__mainProcess.__run.__lowEnventQueue TIMEOUT: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
                                % (event.id, event.type, event.priority,
                                   event.timeStamp, event.args))
                            event = self.__lowEnventQueue.get(block=False)
                        else:
                            event = None
                            break
                # 事件队列非空
                if not event == None:
                    # 执行事件
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
                        % (event.id, event.type, event.priority,
                           event.timeStamp, event.args))
                    self.__process(event)
                else:
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: empty"
                    )
                    # 趁队列空闲的时候清理进程池
                    for p in self.__processPool:
                        if not p.is_alive():
                            self.__processPool.remove(p)
        # break out while
        # 终止所有事件处理进程
        for p in self.__processPool:
            if p.is_alive():
                p.join()

    # 执行事件
    def __process(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run.__process: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        if event.type in self.__handlers:
            for handler in self.__handlers[event.type]:
                # 开一个进程去异步处理
                p = Process(
                    target=handler, args=(event, self.__status.delEventStatus))
                # 保存到进程池
                self.__processPool.append(p)
                # 同步抄送至事件运行状态表格里
                self.__status.addEventStatus(event)
                # 运行进程
                p.start()

    # 开启事件引擎
    def start(self):
        self.__logger.info("src.core.engine.engine.EventEngine.start")
        self.__active.value = True
        # 开启事件引擎主进程
        self.__mainProcess = Process(target=self.__run)
        self.__mainProcess.start()

    # 暂停事件引擎
    def stop(self):
        self.__logger.info("src.core.engine.engine.EventEngine.stop")
        # 将事件管理器设为停止
        self.__active.value = False
        # 等待事件引擎主进程退出
        self.__mainProcess.join()

    # 终止事件引擎
    def terminate(self):
        self.__logger.info("src.core.engine.engine.EventEngine.terminate")
        # 将事件管理器设为停止
        self.__active.value = False
        # 等待事件引擎主进程退出
        self.__mainProcess.terminate()

    # 注册事件
    def register(self, type, handler):
        self.__logger.info(
            "src.core.engine.engine.EventEngine.register: {type:%s, handler:%s}"
            % (type, handler))
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handlerList = self.__handlers[type]
        except KeyError:
            handlerList = []
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)
        self.__handlers[type] = handlerList

    def unregister(self, type, handler):
        self.__logger.info(
            "src.core.engine.engine.EventEngine.unregister: {type:%s, handler:%s}"
            % (type, handler))
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        try:
            handlerList = self.__handlers[type]
            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                handlerList.remove(handler)
            # 如果函数列表为空，则从引擎中移除该事件类型
            if not handlerList:
                del self.__handlers[type]
        except KeyError as err:
            errStr = "src.core.engine.engine.EventEngine.unregister: %s" % EngineException(
                err)
            self.__logger.error(errStr)
            raise EngineException(err)

    def sendEvent(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.sendEvent: { id=%s, type=%s, priority=%s, timeStamp=%s, args=%s }"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        # 发送事件 像队列里存入事件
        if event.priority == LOW_PRIORITY_EVENT:
            self.__lowEnventQueue.put(event)
        if event.priority == MEDIUM_PRIORITY_EVENT:
            self.__mediumEventQueue.put(event)
        if event.priority == HIGH_PRIORITY_EVENT:
            self.__highEventQueue.put(event)

    def getEventID(self):
        id = self.__status.calcEventID()
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.getEventID: { id=%s}" % id)
        return id

    def getEventStatus(self, id):
        status = QUEUE_STATUS_EVENT
        res = self.__status.getActiveStatusTable()
        if res != []:
            if id in res.index:
                status = ACTIVE_STATUS_EVENT
        res = self.__status.getDoneStatusTable()
        if res != []:
            if id in res.index:
                status = DONE_STATUS_EVENT
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.getEventStatus: { id=%s, status=%s}"
            % (id, status))
        return status

    def getActiveEventTable(self):
        res = self.__status.getActiveStatusTable()
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.getActiveEventTable:\n\t%s" %
            res)
        return res

    def getDoneEventTable(self):
        res = self.__status.getDoneStatusTable()
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.getDoneEventTable:\n\t%s" %
            res)
        return res


class Event(object):
    # 事件对象
    def __init__(self, event):
        self.id = event["id"]
        self.type = event["type"]
        self.priority = event["priority"]
        self.timeStamp = int(event["timeStamp"])
        self.args = event["args"]
