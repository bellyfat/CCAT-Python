# -*- coding: utf-8 -*-

import time
from multiprocessing import Process, Queue, Value

from src.core.config import Config
from src.core.engine.enums import (HIGH_PRIORITY_ENVENT,
                                   HIGH_PRIORITY_ENVENT_TIMEOUT,
                                   LOW_PRIORITY_ENVENT,
                                   LOW_PRIORITY_ENVENT_TIMEOUT,
                                   MEDIUM_PRIORITY_ENVENT,
                                   MEDIUM_PRIORITY_ENVENT_TIMEOUT)
from src.core.util.exceptions import EngineException
from src.core.util.helper import utcnow_timestamp
from src.core.util.log import Logger


class EventEngine(object):
    # 初始化事件事件驱动引擎
    def __init__(self):
        self.__engineCof = Config()._engine
        # 保存事件列表 按优先级不同分别保存
        self.__lowEnventQueue = Queue()
        self.__mediumEventQueue = Queue()
        self.__highEventQueue = Queue()
        # 引擎开关
        self.__active = Value('b', False)
        # 事件处理字典{'event1': [handler1,handler2] , 'event2':[handler3, ...,handler4]}
        self.__handlers = {}
        # 保存事件处理进程池
        self.__processPool = []
        # 事件引擎主进程
        self.__mainProcess = None # Process(target=self.__run)
        # logger
        self.__logger = Logger()

    # 执行事件循环
    def __run(self):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run")
        while self.__active.value:
            # 执行 Epoch
            time.sleep(float(self.__engineCof["epoch"]))
            # 控制最大进程数量
            ######################################################
            ## need update later with Router
            ######################################################
            for p in self.__processPool:
                if not p.is_alive():
                    self.__processPool.remove(p)
            if len(self.__processPool) > int(self.__engineCof["maxProcess"]):
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
                    ) - event.timeStamp > HIGH_PRIORITY_ENVENT_TIMEOUT:
                        if not self.__highEventQueue.empty():
                            self.__logger.warn(
                                "src.core.engine.engine.EventEngine.__mainProcess.__run.__highEventQueue TIMEOUT: { type=%s, priority=%s, args=%s }"
                                % (event.type, event.priority, event.args))
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
                    ) - event.timeStamp > MEDIUM_PRIORITY_ENVENT_TIMEOUT:
                        if not self.__mediumEventQueue.empty():
                            self.__logger.warn(
                                "src.core.engine.engine.EventEngine.__mainProcess.__run.__mediumEventQueue TIMEOUT: { type=%s, priority=%s, args=%s }"
                                % (event.type, event.priority, event.args))
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
                    ) - event.timeStamp > LOW_PRIORITY_ENVENT_TIMEOUT:
                        if not self.__lowEnventQueue.empty():
                            self.__logger.warn(
                                "src.core.engine.engine.EventEngine.__mainProcess.__run.__lowEnventQueue TIMEOUT: { type=%s, priority=%s, args=%s }"
                                % (event.type, event.priority, event.args))
                            event = self.__lowEnventQueue.get(block=False)
                        else:
                            event = None
                            break
                # 事件队列非空
                if not event == None:
                    # 执行事件
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: { type=%s, priority=%s, args=%s }"
                        % (event.type, event.priority, event.args))
                    self.__process(event)
                else:
                    self.__logger.debug(
                        "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: empty"
                    )
        # break out while
        # 终止所有事件处理进程
        for p in self.__processPool:
            p.join()

    # 执行事件
    def __process(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run.__process: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        if event.type in self.__handlers:
            for handler in self.__handlers[event.type]:
                # 开一个进程去异步处理
                p = Process(target=handler, args=(event, ))
                # 保存到进程池
                self.__processPool.append(p)
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

    def sendEvent(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.sendEvent: { type=%s, priority=%s, args=%s }"
            % (event.type, event.priority, event.args))
        # 发送事件 像队列里存入事件
        if event.priority == LOW_PRIORITY_ENVENT:
            self.__lowEnventQueue.put(event)
        if event.priority == MEDIUM_PRIORITY_ENVENT:
            self.__mediumEventQueue.put(event)
        if event.priority == HIGH_PRIORITY_ENVENT:
            self.__highEventQueue.put(event)


class Event(object):
    # 事件对象
    def __init__(self, event):
        self.type = event["type"]
        self.priority = event["priority"]
        self.timeStamp = int(event["timeStamp"])
        self.args = event["args"]
