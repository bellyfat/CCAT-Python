# -*- coding: utf-8 -*-

import time
from multiprocessing import Manager, Process, Queue, Value

import psutil

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
        self.__processPool = Manager().list()
        # 保存已执行事件处理状态
        self.__status = Status()
        # 事件引擎主进程
        self.__mainProcess = Process(target=self.__run)
        # logger
        self.__logger = Logger()

    # 执行事件循环
    def __run(self):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run")
        try:
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
                                self.__logger.error(
                                    "src.core.engine.engine.EventEngine.__mainProcess.__run.__highEventQueue TIMEOUT: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
                                    % (event.id, event.type, event.priority,
                                       event.timeStamp, event.args))
                                self.__status.delEventStatus(event)
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
                                self.__logger.error(
                                    "src.core.engine.engine.EventEngine.__mainProcess.__run.__mediumEventQueue TIMEOUT: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
                                    % (event.id, event.type, event.priority,
                                       event.timeStamp, event.args))
                                self.__status.delEventStatus(event)
                                event = self.__mediumEventQueue.get(
                                    block=False)
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
                                self.__logger.error(
                                    "src.core.engine.engine.EventEngine.__mainProcess.__run.__lowEnventQueue TIMEOUT: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
                                    % (event.id, event.type, event.priority,
                                       event.timeStamp, event.args))
                                self.__status.delEventStatus(event)
                                event = self.__lowEnventQueue.get(block=False)
                            else:
                                event = None
                                break
                    # 事件队列非空
                    if not event == None:
                        # 执行事件
                        self.__logger.debug(
                            "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
                            % (event.id, event.type, event.priority,
                               event.timeStamp, event.args))
                        self.__process(event)
                    else:
                        self.__logger.debug(
                            "src.core.engine.engine.EventEngine.__mainProcess.__run.__eventQueue: empty"
                        )
                    # 定期清理进程池
                    if len(self.__processPool) > self.__maxProcess:
                        for (_id, _pid) in self.__processPool:
                            if not psutil.pid_exists(_pid):
                                self.__processPool.remove((_id, _pid))
            # break out while
            # 终止所有事件处理进程
            for (_id, _pid) in self.__processPool:
                if psutil.pid_exists(_pid):
                    _p = psutil.Process(_pid)
                    _p.terminate()
                    self.__processPool.remove((_id, _pid))
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.__mainProcess.__run: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    # 执行事件
    def __process(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.__mainProcess.__run.__process: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}"
            % (event.id, event.type, event.priority, event.timeStamp,
               event.args))
        try:
            if event.type in self.__handlers:
                for handler in self.__handlers[event.type]:
                    # 开一个进程去异步处理
                    p = Process(
                        target=handler, args=(event, self.__status.delEventStatus))
                    # 运行进程
                    p.start()
                    # 保存到进程池
                    self.__processPool.append((event.id, p.pid))
                    # 同步抄送至事件运行状态表格里
                    self.__status.addEventStatus(event.id)
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.__mainProcess.__run.__process: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}, exception err=%s" % (
                event.id, event.type, event.priority, event.timeStamp, event.args, EngineException(err))
            raise EngineException(errStr)

    # 开启事件引擎
    def start(self):
        self.__logger.debug("src.core.engine.engine.EventEngine.start")
        try:
            if not self.__active.value:
                self.__active.value = True
                # 开启事件引擎主进程
                self.__mainProcess.start()
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.start: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    # 暂停事件引擎
    def stop(self):
        self.__logger.debug("src.core.engine.engine.EventEngine.stop")
        try:
            if self.__active.value:
                # 将事件管理器设为停止
                self.__active.value = False
                # 等待事件引擎主进程退出
                self.__mainProcess.join()
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.stop: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    # 终止事件引擎
    def terminate(self):
        self.__logger.debug("src.core.engine.engine.EventEngine.terminate")
        try:
            # 将事件管理器设为停止
            self.__active.value = False
            # 引擎主进程直接退出
            self.__mainProcess.terminate()
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.terminate: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    # 注册事件
    def register(self, type, handler):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.register: {type:%s, handler:%s}"
            % (type, handler))
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            try:
                handlerList = self.__handlers[type]
            except KeyError:
                handlerList = []
            # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
            if handler not in handlerList:
                handlerList.append(handler)
            self.__handlers[type] = handlerList
        except (KeyError, Exception) as err:
            errStr = "src.core.engine.engine.EventEngine.register: {type:%s, handler:%s}, exception err=%s" % (type, handler, EngineException(
                err))
            raise EngineException(errStr)

    # 注销事件

    def unregister(self, type, handler):
        self.__logger.debug(
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
        except (KeyError, Exception) as err:
            errStr = "src.core.engine.engine.EventEngine.unregister: {type:%s, handler:%s}, exception err=%s" % (
                type, handler, EngineException(err))
            raise EngineException(errStr)

    # 发送事件
    def sendEvent(self, event):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.sendEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}" % (
                event.id, event.type, event.priority, event.timeStamp, event.args))
        try:
            # 发送事件 像队列里存入事件
            if event.priority == LOW_PRIORITY_EVENT:
                self.__lowEnventQueue.put(event)
            if event.priority == MEDIUM_PRIORITY_EVENT:
                self.__mediumEventQueue.put(event)
            if event.priority == HIGH_PRIORITY_EVENT:
                self.__highEventQueue.put(event)
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.sendEvent: {id=%s, type=%s, priority=%s, timeStamp=%s, args=%s}, exception err=%s" % (
                event.id, event.type, event.priority, event.timeStamp, event.args, EngineException(err))
            raise EngineException(errStr)

    # kill 事件
    def killEvent(self, id):
        self.__logger.debug(
            "src.core.engine.engine.EventEngine.killEvent: {id=%s}" % id)
        try:
            # 查询事件状态
            status = self.getEventStatus(id)
            # 删除事件进程
            if not status == DONE_STATUS_EVENT:
                for (_id, _pid) in self.__processPool:
                    if _id == id:
                        if psutil.pid_exists(_pid):
                            _p = psutil.Process(_pid)
                            _p.terminate()
                        # 更新事件状态
                        self.__processPool.remove((_id, _pid))
                        self.__status.delEventStatus(id)
                # 确认事件状态
                status = self.getEventStatus(id)
                if not status == DONE_STATUS_EVENT:
                    return False
            return True
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.killEvent: {id=%s}, exception err=%s" % (
                id, EngineException(err))
            raise EngineException(errStr)

    # 获取事件ID
    def getEventID(self):
        try:
            id = self.__status.calcEventID()
            self.__logger.debug(
                "src.core.engine.engine.EventEngine.getEventID: {id=%s}" % id)
            return id
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.getEventID: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    def getEventStatus(self, id):
        try:
            status = QUEUE_STATUS_EVENT
            res = self.__status.getActiveStatusTable()
            if not res == []:
                if id in res:
                    status = ACTIVE_STATUS_EVENT
            res = self.__status.getDoneStatusTable()
            if not res == []:
                if id in res:
                    status = DONE_STATUS_EVENT
            # 进程池二次确认
            if status == ACTIVE_STATUS_EVENT:
                for (_id, _pid) in self.__processPool:
                    if _id == id:
                        if not psutil.pid_exists(_pid):
                            status = DONE_STATUS_EVENT
                            self.__status.delEventStatus(_id)
                            self.__processPool.remove((_id, _pid))
            self.__logger.debug(
                "src.core.engine.engine.EventEngine.getEventStatus: {id=%s, status=%s}"
                % (id, status))
            return status
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.getEventStatus: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    def getActiveEventTable(self):
        try:
            res = self.__status.getActiveStatusTable()
            self.__logger.debug(
                "src.core.engine.engine.EventEngine.getActiveEventTable: {res=%s}" %
                res)
            return res
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.getActiveEventTable: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)

    def getDoneEventTable(self):
        try:
            res = self.__status.getDoneStatusTable()
            self.__logger.debug(
                "src.core.engine.engine.EventEngine.getDoneEventTable: {res=%s}" %
                res)
            return res
        except Exception as err:
            errStr = "src.core.engine.engine.EventEngine.getDoneEventTable: exception err=%s" % EngineException(
                err)
            raise EngineException(errStr)


class Event(object):
    # 事件对象
    def __init__(self, event):
        self.id = event["id"]
        self.type = event["type"]
        self.priority = event["priority"]
        self.timeStamp = int(event["timeStamp"])
        self.args = event["args"]
