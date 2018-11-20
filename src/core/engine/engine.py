# -*- coding: utf-8 -*-

import time
from multiprocessing import Process, Queue, Value

from src.core.config import Config
from src.core.util.log import Logger
from src.core.util.exceptions import EngineException


class EventEngine(object):
    # 初始化事件事件驱动引擎
    def __init__(self):
        # 保存事件列表
        self.__eventQueue = Queue()
        # 引擎开关
        self.__active = Value('b', False)
        # 事件处理字典{'event1': [handler1,handler2] , 'event2':[handler3, ...,handler4]}
        self.__handlers = {}
        # 保存事件处理进程池
        self.__processPool = []
        # 事件引擎主进程
        self.__mainProcess = Process(target=self.__run, args=(self.__active, ))
        # logger
        self.__logger = Logger()

    # 执行事件循环
    def __run(self, __active):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run")
        while __active.value:
            # 事件队列非空
            if not self.__eventQueue.empty():
                # 获取队列中的事件 超时1秒
                event = self.__eventQueue.get(
                    block=True, timeout=float(Config()._engine["timeout"]))
                # 执行事件
                self.__logger.debug(
                    "src.core.engine.engine.EventEngine.__mainProcess.__run.eventQueue: "
                    + event.type)
                self.__process(event)
            else:
                # 等待 epoch
                self.__logger.debug(
                    "src.core.engine.engine.EventEngine.__mainProcess.__run.eventQueue: empty"
                )
                time.sleep(float(Config()._engine["epoch"]))

    # 执行事件
    def __process(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__process: " +
            event.type)
        if event.type in self.__handlers:
            for handler in self.__handlers[event.type]:
                # 开一个进程去异步处理
                p = Process(target=handler, args=(event, ))
                # 保存到进程池
                self.__processPool.append(p)
                p.start()

    # 开启事件引擎
    def start(self):
        self.__logger.debug("src.core.engine.engine.EventEngine.start")
        self.__active.value = True
        # 开启事件引擎主进程
        self.__mainProcess.start()

    # 暂停事件引擎
    def stop(self):
        self.__logger.debug("src.core.engine.engine.EventEngine.stop")
        # 将事件管理器设为停止
        self.__active.value = False
        # 等待事件处理进程退出
        for p in self.__processPool:
            p.join()
        self.__mainProcess.join()

    # 终止事件引擎
    def terminate(self):
        self.__logger.debug("src.core.engine.engine.EventEngine.terminate")
        self.__active.value = False
        # 终止所有事件处理进程
        for p in self.__processPool:
            p.terminate()
        self.__mainProcess.terminate()

    # 注册事件
    def register(self, event, handler):
        self.__logger.debug("src.core.engine.engine.EventEngine.register")
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        type = event.type
        try:
            handlerList = self.__handlers[type]
        except KeyError:
            handlerList = []
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)
        self.__handlers[type] = handlerList

    def unregister(self, event, handler):
        self.__logger.debug("src.core.engine.engine.EventEngine.unregister")
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        type = event.type
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
        self.__logger.debug("src.core.engine.engine.EventEngine.sendEvent")
        # 发送事件 像队列里存入事件
        self.__eventQueue.put(event)


class Event(object):
    # 事件对象
    def __init__(self, event):
        self.type = event["type"]
        self.dict = event["dict"]
