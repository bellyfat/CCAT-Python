# -*- coding: utf-8 -*-

import os
import time
from threading import Thread, current_thread

import pandas as pd

from src.core.calc.signal import Signal
from src.core.config import Config
from src.core.db.db import DB
from src.core.engine.enums import (ACTIVE_STATUS_EVENT, DONE_STATUS_EVENT,
                                   QUEUE_STATUS_EVENT, TYPE_DIS, TYPE_PAIR,
                                   TYPE_TRA)
from src.core.util.exceptions import (DBException, EngineException,
                                      UtilException)
from src.core.util.helper import timestamp_to_isoformat, utcnow_timestamp
from src.core.util.log import Logger


# util class
class Util(object):
    def __init__(self, eventEngine, sender):
        # Config init
        # Main Settings
        self._types = Config()._Main_types
        self._exchanges = Config()._Main_exchanges
        self._excludeCoins = Config()._Main_excludeCoins
        self._baseCoin = Config()._Main_baseCoin
        self._marketDepthLimit = Config()._Main_marketDepthLimit
        self._marketTickerAggStep = Config()._Main_marketTickerAggStep
        self._apiEpochSaveBound = Config()._Main_apiEpochSaveBound
        self._apiResultEpoch = Config()._Main_apiResultEpoch
        # huobi exchange for insert deposit and withdraw history
        self._Okex_exchange = Config()._Okex_exchange
        self._Binance_exchange = Config()._Binance_exchange
        self._Huobi_exchange = Config()._Huobi_exchange
        # ServerLimit
        self._serverLimits = None
        # Engine
        self._engine = eventEngine
        self._sender = sender
        # logger
        self._logger = Logger()

    # Init DB 数据库
    def initDB(self):
        self._logger.debug("src.core.util.util.Util.initDB")
        try:
            db = DB()
            db.initDB()
            db.creatTables()
            db.creatViews()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.initDB: exception err=%s" % UtilException(
                err)
            raise UtilException(errStr)

    # Init Info数据
    def threadInsertInfoServer(self, server):
        self._logger.debug(
            "src.core.util.util.Util.threadInsertInfoServer: {thread=%s, server=%s}"
            % (current_thread().name, server))
        try:
            db = DB()
            db.insertInfoServer(server)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoServer: {thread=%s, server=%s}, exception err=%s" % (
                current_thread().name, server, UtilException(err))
            self._logger.critical(errStr)

    def threadInsertInfoSymbol(self, server):
        self._logger.debug(
            "src.core.util.util.Util.threadInsertInfoSymbol: {thread=%s, server=%s}"
            % (current_thread().name, server))
        try:
            db = DB()
            db.insertInfoSymbol(server)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoSymbol: {thread=%s, server=%s}, exception err=%s" % (
                current_thread().name, server, UtilException(err))
            self._logger.critical(errStr)

    def threadInsertInfoWithdraw(self, server):
        self._logger.debug(
            "src.core.util.util.Util.threadInsertInfoWithdraw: {thread=%s, server=%s}"
            % (current_thread().name, server))
        try:
            db = DB()
            db.insertInfoWithdraw(server)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadInsertInfoWithdraw: {thread=%s, server=%s}, exception err=%s" % (
                current_thread().name, server, UtilException(err))
            self._logger.critical(errStr)

    def initDBInfo(self):
        self._logger.debug("src.core.util.util.Util.initDBInfo")
        try:
            tds = []
            for server in self._exchanges:
                td = Thread(
                    target=self.threadInsertInfoServer,
                    name="%s-threadInsertInfoServer" % server,
                    args=([server], ))
                tds.append(td)
                td.start()
                td = Thread(
                    target=self.threadInsertInfoSymbol,
                    name="%s-threadInsertInfoSymbol" % server,
                    args=([server], ))
                tds.append(td)
                td.start()
                td = Thread(
                    target=self.threadInsertInfoWithdraw,
                    name="%s-threadInsertInfoWithdraw" % server,
                    args=([server], ))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.initDBInfo: exception err=%s" % UtilException(
                err)
            raise UtilException(errStr)

    # Init ServerLimit数据
    def initServerLimits(self):
        self._logger.debug("src.core.util.util.Util.initServerLimits")
        try:
            db = DB()
            res = db.getInfoServer()
            self._serverLimits = pd.DataFrame(res).set_index(["server"],
                                                             inplace=False)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.initServerLimits: exception err=%s" % UtilException(
                err)
            raise UtilException(errStr)

    # Account Balance 事件
    def updateDBAccountBalance(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBAccountBalance: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            ets = []
            startTime = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBAccountBalance: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "info_second"])
                time.sleep(epoch)
                event = self._sender.sendListenAccountBalanceEvent([server])
                ets.append(event)
            if not async:
                st = QUEUE_STATUS_EVENT
                for event in ets:
                    st = self._engine.getEventStatus(event)
                    while st != DONE_STATUS_EVENT and (time.time(
                    ) - startTime < timeout or timeout == 0):
                        st = self._engine.getEventStatus(event)
                        time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBAccountBalance: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout." % (async, timeout))
                    for event in ets:
                        if not self._engine.killEvent(event):
                            self._logger.error(
                                "src.core.util.util.Util.updateDBAccountBalance: {async: % s, timeout: % s}, exception err=KILL EVENT ERROR, kill timeout event handler error." % (async, timeout))
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBAccountBalance: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Account Withdraw 事件
    def threadSendListenAccountWithdrawEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, 'res', epoch, async, timeout))
        ets = []
        startTime = time.time()
        for r in res:
            if not time.time(
            ) - startTime < timeout and not timeout == 0:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                break
            if not r['can_deposit'] == 'False' and not r[
                    'can_withdraw'] == 'False':
                time.sleep(epoch)
                event = self._sender.sendListenAccountWithdrawEvent(
                    [r["server"]], r["asset"])
                ets.append(event)
        if not async:
            st = QUEUE_STATUS_EVENT
            for event in ets:
                st = self._engine.getEventStatus(event)
                while st != DONE_STATUS_EVENT and (time.time(
                ) - startTime < timeout or timeout == 0):
                    st = self._engine.getEventStatus(event)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenAccountWithdrawEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                for event in ets:
                    if not self._engine.killEvent(event):
                        self._logger.error(
                            "src.core.util.util.Util..threadSendListenAccountWithdrawEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error." % (current_thread().name, 'res', epoch, async, timeout))

    def updateDBAccountWithdraw(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBAccountWithdraw: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            db = DB()
            tds = []
            startTime = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBAccountWithdraw: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "info_second"])
                if server in [self._Okex_exchange, self._Binance_exchange]:
                    time.sleep(epoch)
                    td = Thread(
                        target=db.insertAccountWithdrawHistory,
                        name="%s-thread" % server,
                        args=([server], ))
                    tds.append(td)
                    td.start()
                if server == self._Huobi_exchange:
                    res = db.getInfoWithdraw([server])
                    td = Thread(
                        target=self.threadSendListenAccountWithdrawEvent,
                        name="%s-thread" % server,
                        args=(res, epoch, async, timeout))
                    tds.append(td)
                    td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBAccountWithdraw: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Market Depth 事件
    def threadSendListenMarketDepthEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketDepthEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, 'res', epoch, async, timeout))
        ets = []
        startTime = time.time()
        for r in res:
            if not time.time(
            ) - startTime < timeout and not timeout == 0:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenMarketDepthEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                break
            time.sleep(epoch)
            event = self._sender.sendListenMarketDepthEvent(
                [r["server"]], r["fSymbol"], r["tSymbol"],
                self._marketDepthLimit)
            ets.append(event)
        if not async:
            st = QUEUE_STATUS_EVENT
            for event in ets:
                st = self._engine.getEventStatus(event)
                while st != DONE_STATUS_EVENT and (time.time(
                ) - startTime < timeout or timeout == 0):
                    st = self._engine.getEventStatus(event)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenMarketDepthEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                for event in ets:
                    if not self._engine.killEvent(event):
                        self._logger.error(
                            "src.core.util.util.Util.threadSendListenMarketDepthEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error." % (current_thread().name, 'res', epoch, async, timeout))

    def updateDBMarketDepth(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBMarketDepth: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            tds = []
            db = DB()
            db.delMarketDepth()
            startTime = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBMarketDepth: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewMarketSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketDepthEvent,
                    name="%s-threadSendListenMarketDepthEvent" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketDepth: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Market Kline 事件
    def threadSendListenMarketKlineEvent(self, res, start, end, interval,
                                         epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, res: %s, start: %s, interval: %s, end: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, 'res', start, end, interval, epoch, async,
               timeout))
        ets = []
        startTime = time.time()
        for r in res:
            if not time.time(
            ) - startTime < timeout and not timeout == 0:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, res: %s, start: %s, interval: %s, end: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout."
                    % (current_thread().name, 'res', start, end, interval, epoch, async,
                       timeout))
                break
            time.sleep(epoch)
            event = self._sender.sendListenMarketKlineEvent(
                [r["server"]], r["fSymbol"], r["tSymbol"], interval, start, end)
            ets.append(event)
        self._logger.info("thread=%sm send done" % current_thread().name)
        if not async:
            st = QUEUE_STATUS_EVENT
            for event in ets:
                st = self._engine.getEventStatus(event)
                while st != DONE_STATUS_EVENT and (time.time(
                ) - startTime < timeout or timeout == 0):
                    st = self._engine.getEventStatus(event)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, res: %s, start: %s, end: %s, interval: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                    % (current_thread().name, 'res', start, end, interval, epoch,
                       async, timeout))
                for event in ets:
                    if not self._engine.killEvent(event):
                        self._logger.error(
                            "src.core.util.util.Util.threadSendListenMarketKlineEvent: {thread: %s, res: %s, start: %s, end: %s, interval: %s, epoch: %s, async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error."
                            % (current_thread().name, 'res', start, end, interval, epoch,
                               async, timeout))

    def updateDBMarketKline(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBMarketKline: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            tds = []
            db = DB()
            db.delMarketKline()
            interval = '1d'
            end = utcnow_timestamp() - 12 * 60 * 60 * 1000
            start = end - 24 * 60 * 60 * 1000
            startTime = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBMarketKline: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewInfoSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketKlineEvent,
                    name="%s-threadSendListenMarketKlineEvent" % server,
                    args=(res, timestamp_to_isoformat(start),
                          timestamp_to_isoformat(end), interval, epoch, async,
                          timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketKline: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Market ticker 事件
    def threadSendListenMarketTickerEvent(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendListenMarketTickerEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, 'res', epoch, async, timeout))
        ets = []
        db = DB()
        startTime = time.time()
        for r in res:
            if not time.time(
            ) - startTime < timeout and not timeout == 0:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenMarketTickerEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                break
            aggDepth = db.getViewMarketSymbolPairsAggDepth(
                self._exchanges, r["fSymbol"],
                r["tSymbol"])[0]["aggDepth"]
            aggDepth = float(aggDepth) * self._marketTickerAggStep
            time.sleep(epoch)
            event = self._sender.sendListenMarketTickerEvent(
                [r["server"]], r["fSymbol"], r["tSymbol"], aggDepth)
            ets.append(event)
        if not async:
            st = QUEUE_STATUS_EVENT
            for event in ets:
                st = self._engine.getEventStatus(event)
                while st != DONE_STATUS_EVENT and (time.time(
                ) - startTime < timeout or timeout == 0):
                    st = self._engine.getEventStatus(event)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.error(
                    "src.core.util.util.Util.threadSendListenMarketTickerEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                for event in ets:
                    if not self._engine.killEvent(event):
                        self._logger.error(
                            "src.core.util.util.Util.threadSendListenMarketTickerEvent: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error."
                            % (current_thread().name, 'res', epoch, async, timeout))

    def updateDBMarketTicker(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBMarketTicker: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            tds = []
            db = DB()
            db.delMarketTicker()
            startTime = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBMarketTicker: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "market_second"])
                res = db.getViewMarketSymbolPairs([server])
                td = Thread(
                    target=self.threadSendListenMarketTickerEvent,
                    name="%s-threadSendListenMarketTickerEvent" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBMarketTicker: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Judge 事件
    def updateDBJudgeMarketDepth(self):
        pass

    def updateDBJudgeMarketKline(self):
        pass

    def updateDBJudgeMarketTicker(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            db = DB()
            db.delJudgeSignalTickerDis()
            db.delJudgeSignalTickerTra()
            db.delJudgeSignalTickerPair()
            ets = []
            startTime = time.time()
            for type in self._types:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                event = self._sender.sendJudgeMarketTickerEvent(
                    self._exchanges, [type])
                ets.append(event)
            if not async:
                st = QUEUE_STATUS_EVENT
                for event in ets:
                    st = self._engine.getEventStatus(event)
                    while st != DONE_STATUS_EVENT and (time.time(
                    ) - startTime < timeout or timeout == 0):
                        st = self._engine.getEventStatus(event)
                        time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                        % (async, timeout))
                    for event in ets:
                        if not self._engine.killEvent(event):
                            self._logger.error(
                                "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error."
                                % (async, timeout))
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Backtest 事件
    def updateDBBacktestHistoryCreat(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBBacktestHistoryCreat: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            ets = []
            sig = Signal()
            startTime = time.time()
            for type in self._types:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBBacktestHistoryCreat: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                # calc signals
                signals = sig.signals(self._exchanges, [type])
                if not signals == []:
                    df = pd.DataFrame(signals)
                    if type == TYPE_DIS:
                        for group_key, group in df.groupby(['fSymbol', 'tSymbol']):
                            event = self._sender.sendBacktestHistoryCreatEvent(
                                group.to_dict('records'), timeout)
                            ets.append(event)
                    if type == TYPE_TRA:
                        for group_key, group in df.groupby(['V1_fSymbol', 'V1_tSymbol', 'V2_fSymbol', 'V2_tSymbol', 'V3_fSymbol', 'V3_tSymbol']):
                            event = self._sender.sendBacktestHistoryCreatEvent(
                                group.to_dict('records'), timeout)
                            ets.append(event)
                    if type == TYPE_PAIR:
                        for group_key, group in df.groupby(['V1_fSymbol', 'V1_tSymbol', 'V2_fSymbol', 'V2_tSymbol', 'V3_fSymbol', 'V3_tSymbol']):
                            event = self._sender.sendBacktestHistoryCreatEvent(
                                group.to_dict('records'), timeout)
                            ets.append(event)
            if not async:
                st = QUEUE_STATUS_EVENT
                for event in ets:
                    st = self._engine.getEventStatus(event)
                    while st != DONE_STATUS_EVENT and (time.time(
                    ) - startTime < timeout or timeout == 0):
                        st = self._engine.getEventStatus(event)
                        time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBBacktestHistoryCreat: {async: %s, timeout: %s}, err=TIMEOUT ERROR, waiting result from event handler timeout."
                        % (async, timeout))
                    for event in ets:
                        if not self._engine.killEvent(event):
                            self._logger.error(
                                "src.core.util.util.Util.updateDBBacktestHistoryCreat: {async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error."
                                % (async, timeout))
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBBacktestHistoryCreat: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # Order 事件
    def threadSendInsertDBOrderHistory(self, res, epoch, async, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadSendInsertDBOrderHistory: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}"
            % (current_thread().name, 'res', epoch, async, timeout))
        ets = []
        startTime = time.time()
        for r in res:
            if not time.time(
            ) - startTime < timeout and not timeout == 0:
                self._logger.error(
                    "src.core.util.util.Util.threadSendInsertDBOrderHistory: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                break
            time.sleep(epoch)
            event = self._sender.sendOrderHistoryInsertEvent(
                [r["server"]], r["fSymbol"], r["tSymbol"], '100',
                r["fee_taker"])
            ets.append(event)
        if not async:
            st = QUEUE_STATUS_EVENT
            for event in ets:
                st = self._engine.getEventStatus(event)
                while st != DONE_STATUS_EVENT and (time.time(
                ) - startTime < timeout or timeout == 0):
                    st = self._engine.getEventStatus(event)
                    time.sleep(self._apiResultEpoch)
            if st != DONE_STATUS_EVENT:
                self._logger.error(
                    "src.core.util.util.Util.threadSendInsertDBOrderHistory: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                    % (current_thread().name, 'res', epoch, async, timeout))
                for event in ets:
                    if not self._engine.killEvent(event):
                        self._logger.error(
                            "src.core.util.util.Util.threadSendInsertDBOrderHistory: {thread: %s, res: %s, epoch: %s, async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error."
                            % (current_thread().name, 'res', epoch, async, timeout))

    def updateDBOrderHistoryInsert(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBOrderHistoryInsert: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            db = DB()
            tds = []
            startTime = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBOrderHistoryInsert: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "info_second"])
                res = db.getInfoSymbol([server])
                td = Thread(
                    target=self.threadSendInsertDBOrderHistory,
                    name="%s-thread" % server,
                    args=(res, epoch, async, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBOrderHistoryInsert: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    def updateDBOrderHistoryCreat(self):
        pass

    # Statistic 事件
    def updateDBStatisticJudge(self, async=True, timeout=30):
        self._logger.debug(
            "src.core.util.util.Util.updateDBStatisticJudge: {async: %s, timeout: %s}"
            % (async, timeout))
        try:
            ets = []
            db = DB()
            db.delStatisticSignalTickerDis()
            db.delStatisticSignalTickerTra()
            db.delStatisticSignalTickerPair()
            startTime = time.time()
            for type in self._types:
                if not time.time(
                ) - startTime < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBStatisticJudge: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, sending event to event handler timeout." % (async, timeout))
                    break
                event = self._sender.sendStatiscJudgeEvent(
                    self._exchanges, [type])
                ets.append(event)
            if not async:
                st = QUEUE_STATUS_EVENT
                for event in ets:
                    st = self._engine.getEventStatus(event)
                    while st != DONE_STATUS_EVENT and (time.time(
                    ) - startTime < timeout or timeout == 0):
                        st = self._engine.getEventStatus(event)
                        time.sleep(self._apiResultEpoch)
                if st != DONE_STATUS_EVENT:
                    self._logger.error(
                        "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=TIMEOUT ERROR, waiting result from event handler timeout."
                        % (async, timeout))
                    for event in ets:
                        if not self._engine.killEvent(event):
                            self._logger.error(
                                "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=KILL EVENT ERROR, kill timeout event handler error."
                                % (current_thread().name, 'res', epoch, async, timeout))
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.updateDBJudgeMarketTicker: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    def updateDBStatisticBacktest(self):
        pass

    def updateDBStatisticOrder(self):
        pass

    # Util 紧急功能
    # 一键 cancle 撤销所有订单
    def threadOneClickCancleOrders(self, server, epoch, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadOneClickCancleOrders: {thread: %s, server: %s, epoch: %s, timeout: %s}"
            % (current_thread().name, server, epoch, timeout))
        try:
            db = DB()
            res = False
            start = time.time()
            while (res == False and ((time.time() - start) < timeout or timeout == 0)):
                time.sleep(epoch)
                res = db.oneClickCancleOrders(server)
            if not res:
                errStr = "src.core.util.util.Util.threadOneClickCancleOrders: {thread: %s, server: %s, epoch: %s, timeout: %s}，exception err=TIMEOUT ERROR." % (
                    current_thread().name, server, epoch, timeout)
                self._logger.error(errStr)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadOneClickCancleOrders: {thread: %s, server: %s, epoch: %s, timeout: %s}，exception err=%s" % (
                current_thread().name, server, epoch, timeout, Exception(err))
            self._logger.error(errStr)

    def oneClickCancleOrders(self, timeout=30):
        self._logger.debug("src.core.util.util.Util.oneClickCancleOrders")
        try:
            tds = []
            start = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - start < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.oneClickCancleOrders: {timeout: %s}, exception err=TIMEOUT ERROR." % timeout)
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "orders_second"])
                td = Thread(
                    target=self.threadOneClickCancleOrders,
                    name="%s-thread" % server,
                    args=([server], epoch, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.oneClickCancleOrders: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # 一键 order 交易所有币到baseCoin
    def threadOneClickTransToBaseCoin(self, server, baseCoin, epoch, timeout):
        self._logger.debug(
            "src.core.util.util.Util.threadOneClickTransToBaseCoin: {thread: %s, server: %s, baseCoin: %s, epoch: %s, timeout: %s}"
            % (current_thread().name, server, baseCoin, epoch, timeout))
        try:
            db = DB()
            res = False
            start = time.time()
            while (res == False and ((time.time() - start) < timeout or timeout == 0)):
                time.sleep(epoch)
                res = db.oneClickTransToBaseCoin(server, baseCoin)
            if not res:
                errStr = "src.core.util.util.Util.threadOneClickTransToBaseCoin: {thread: %s, server: %s, baseCoin %s, epoch: %s, timeout: %s}，exception err=TIMEOUT ERROR." % (
                    current_thread().name, server, baseCoin, epoch, timeout)
                self._logger.error(errStr)
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.threadOneClickTransToBaseCoin: {thread: %s, server: %s, baseCoin %s, epoch: %s, timeout: %s}，exception err=%s" % (
                current_thread().name, server, baseCoin, epoch, timeout,
                Exception(err))
            self._logger.error(errStr)

    def oneClickTransToBaseCoin(self, baseCoin='', timeout=30):
        self._logger.debug("src.core.util.util.Util.oneClickTransToBaseCoin")
        try:
            if not baseCoin:
                baseCoin = self._baseCoin
            tds = []
            start = time.time()
            for server in self._exchanges:
                if not time.time(
                ) - start < timeout and not timeout == 0:
                    self._logger.error(
                        "src.core.util.util.Util.oneClickTransToBaseCoin: {baseCoin: %s, timeout: %s}, exception err=TIMEOUT ERROR." % (baseCoin, timeout))
                    break
                epoch = float(self._apiEpochSaveBound) / float(
                    self._serverLimits.at[server, "orders_second"])
                td = Thread(
                    target=self.threadOneClickTransToBaseCoin,
                    name="%s-thread" % server,
                    args=([server], baseCoin, epoch, timeout))
                tds.append(td)
                td.start()
            for td in tds:
                td.join()
        except (DBException, EngineException, Exception) as err:
            errStr = "src.core.util.util.Util.oneClickTransToBaseCoin: {async: %s, timeout: %s}, exception err=%s" % (
                async, timeout, UtilException(err))
            raise UtilException(errStr)

    # 一键 withdraw baseCoin 提币到交易所钱包
    def oneClickWithdrawBaseCoin(self):
        pass

    # 一键 deposite baseCoin 充币到交易所钱包
    def oneClickDepositeBaseCoin(self):
        pass
