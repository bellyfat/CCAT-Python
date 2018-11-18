# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
from src.core.util.log import Logger


class EventEngine(object):
    # 初始化事件事件驱动引擎
    def __init__(self):
        # 保存事件列表
        self.__eventQueue = Queue()
        # 引擎开关
        self.__active = False
        # 事件处理字典{'event1': [handler1,handler2] , 'event2':[handler3, ...,handler4]}
        self.__handlers = {}
        # 保存事件处理进程池
        self.__processPool = []
        # 事件引擎主进程
        self.__mainProcess = Process(target=self.__run)
        # logger
        self.logger = Logger()

    # 执行事件循环
    def __run(self):
        while self.__active:
            # 事件队列非空
            if not self.__eventQueue.empty():
                # 获取队列中的事件 超时1秒
                event = self.__eventQueue.get(block=True, timeout=1)
                # 执行事件
                self.logger.debug(event)
                self.__process(event)
            else:
                # print('无任何事件')
                pass

    # 执行事件
    def __process(self, event):
        if event.type in self.__handlers:
            for handler in self.__handlers[event.type]:
                # 开一个进程去异步处理
                p = Process(target=handler, args=(event, ))
                # 保存到进程池
                self.__processPool.append(p)
                p.start()

    # 开启事件引擎
    def start(self):
        self.__active = True
        self.__mainProcess.start()

    # 暂停事件引擎
    def stop(self):
        """停止"""
        # 将事件管理器设为停止
        self.__active = False
        # 等待事件处理进程退出
        for p in self.__processPool:
            p.join()
        self.__mainProcess.join()

    # 终止事件引擎
    def terminate(self):
        self.__active = False
        # 终止所有事件处理进程
        for p in self.__processPool:
            p.terminate()
        self.__mainProcess.join()

    # 注册事件
    def register(self, type, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handlerList = self.__handlers[type]
        except KeyError:
            handlerList = []
            self.__handlers[type] = handlerList
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            self.logger.debug(handler)
            handlerList.append(handler)

    def unregister(self, type, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        try:
            handlerList = self.__handlers[type]
            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                self.logger.debug(handler)
                handlerList.remove(handler)
            # 如果函数列表为空，则从引擎中移除该事件类型
            if not handlerList:
                del self.__handlers[type]
        except KeyError:
            pass

    def sendEvent(self, event):
        # 发送事件 像队列里存入事件
        self.logger.debug(event)
        self.__eventQueue.put(event)


class Event(object):
    # 事件对象
    def __init__(self, type='', dict={}):
        self.type = type
        self.dict = dict
