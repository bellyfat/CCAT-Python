# -*- coding: utf-8 -*-

import json
import os
import sqlite3

from src.core.coin.binance import Binance
from src.core.coin.okex import Okex
from src.core.config import Config
from src.core.db.sql import *
from src.core.util.exceptions import (BinanceException, DBException,
                                      OkexException)
from src.core.util.helper import dict_factory, sqlite_escape, utcnow_timestamp
from src.core.util.log import Logger


# db class
class DB(object):
    def __init__(self):
        proxies = Config()._proxies
        dbStr = os.path.join(os.getcwd(), Config()._db["url"])
        self._dbStr = dbStr
        self._conn = sqlite3.connect(dbStr)
        self._conn.row_factory = dict_factory
        os.chmod(self._dbStr, 0o664)  # 设置读写权限
        self._okexConf = Config()._okex
        self._okex = Okex(self._okexConf["exchange"],
                          self._okexConf["api_key"],
                          self._okexConf["api_secret"],
                          self._okexConf["passphrase"], proxies["url"])
        self._binanceConf = Config()._binance
        self._binance = Binance(
            self._binanceConf["exchange"], self._binanceConf["api_key"],
            self._binanceConf["api_secret"], proxies["url"])
        self._logger = Logger()

    def __del__(self):
        self._conn.close()

    def initDB(self):
        self._logger.debug("src.core.db.db.DB.initDB")
        try:
            self._conn.close()
            os.remove(self._dbStr)
            self._conn = sqlite3.connect(self._dbStr)
            self._conn.row_factory = dict_factory
            os.chmod(self._dbStr, 0o664)  # 设置读写权限
        except IOError as err:
            raise DBException(err)

    def getViews(self):
        self._logger.debug("src.core.db.db.DB.getViews")
        self._logger.debug(GET_VIEWS_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_VIEWS_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def creatViews(self):
        self._logger.debug("src.core.db.db.DB.creatViews")
        self._logger.debug(CREATE_VIEWS_SQL)
        try:
            curs = self._conn.cursor()
            curs.executescript(CREATE_VIEWS_SQL)
            curs.close()
        except sqlite3.Error as err:
            raise DBException(err)

    def getViewInfoSymbolPairs(self, exchange):
        self._logger.debug("src.core.db.db.DB.getViewInfoSymbolPairs")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_INFO_SYMBOL_PAIRS_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getViewAccountBalanceCurrent(self, exchange):
        self._logger.debug("src.core.db.db.DB.getViewAccountBalanceCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_ACCOUNT_BALANCE_CURRENT_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getTables(self):
        self._logger.debug("src.core.db.db.DB.getTables")
        self._logger.debug(GET_TABLES_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_TABLES_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def creatTables(self):
        self._logger.debug("src.core.db.db.DB.creatTables")
        self._logger.debug(CREATE_TABELS_SQL)
        try:
            curs = self._conn.cursor()
            curs.executescript(CREATE_TABELS_SQL)
            curs.close()
        except sqlite3.Error as err:
            raise DBException(err)

    def getAccountBalanceHistory(self):
        self._logger.debug("src.core.db.db.DB.getAccountBalanceHistory")
        self._logger.debug(GET_ACCOUNT_INFO_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_ACCOUNT_INFO_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getMarketDepth(self):
        self._logger.debug("src.core.db.db.DB.getMarketDepth")
        self._logger.debug(GET_MARKET_DEPTH_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_MARKET_DEPTH_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getMarketKline(self):
        self._logger.debug("src.core.db.db.DB.getMarketKline")
        self._logger.debug(GET_MARKET_KLINE_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_MARKET_KLINE_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getMarketTicker(self):
        self._logger.debug("src.core.db.db.DB.getMarketTicker")
        self._logger.debug(GET_MARKET_TIKER_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_MARKET_TIKER_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getInfoServer(self):
        self._logger.debug("src.core.db.db.DB.getInfoServer")
        self._logger.debug(GET_INFO_SERVER_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_INFO_SERVER_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getInfoSymbol(self):
        self._logger.debug("src.core.db.db.DB.getInfoSymbol")
        self._logger.debug(GET_INFO_SYMBOL_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_INFO_SYMBOL_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getTradeBacktestHistory(self):
        self._logger.debug("src.core.db.db.DB.getTradeBacktestHistory")
        self._logger.debug(GET_TRADE_BACKTEST_HISTORY_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_TRADE_BACKTEST_HISTORY_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getTradeOrderHistory(self):
        self._logger.debug("src.core.db.db.DB.getTradeOrderHistory")
        self._logger.debug(GET_TRADE_ORDER_HISTORY_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_TRADE_ORDER_HISTORY_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getAccountWithdrawHistory(self):
        self._logger.debug("src.core.db.db.DB.getAccountWithdrawHistory")
        self._logger.debug(GET_WITHDRAW_HISTORY_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_WITHDRAW_HISTORY_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def getInfoWithdraw(self):
        self._logger.debug("src.core.db.db.DB.getInfoWithdraw")
        self._logger.debug(GET_INFO_WITHDRAW_SQL)
        try:
            curs = self._conn.cursor()
            curs.execute(GET_INFO_WITHDRAW_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException(err)

    def insertAccountBalanceHistory(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertAccountBalanceHistory: { exchange=%s }" % exchange)
        try:
            curs = self._conn.cursor()
            timeStamp = utcnow_timestamp()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        INSERT_OKEX_ACCOUNT_INFO_SQL = INSERT_ACCOUNT_INFO_SQL.substitute(
                            server=str(self._okexConf["exchange"]),
                            timeStamp=int(timeStamp),
                            asset=str(b["asset"]),
                            balance=float(b["balance"]),
                            free=float(b["free"]),
                            locked=float(b["locked"]))
                        self._logger.debug(INSERT_OKEX_ACCOUNT_INFO_SQL)
                        curs.execute(INSERT_OKEX_ACCOUNT_INFO_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        INSERT_BINANCE_ACCOUNT_INFO_SQL = INSERT_ACCOUNT_INFO_SQL.substitute(
                            server=str(self._binanceConf["exchange"]),
                            timeStamp=int(timeStamp),
                            asset=str(b["asset"]),
                            balance=float(b["balance"]),
                            free=float(b["free"]),
                            locked=float(b["locked"]))
                        self._logger.debug(INSERT_BINANCE_ACCOUNT_INFO_SQL)
                        curs.execute(INSERT_BINANCE_ACCOUNT_INFO_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertMarketDepth(self, exchange, fSymbol, tSymbol, limit=100):
        self._logger.debug("src.core.db.db.DB.insertMarketDepth: { exchange=%s, fSymbol=%s, tSymbol=%s, limit=%s }" % (exchange, fSymbol， tSymbol, limit))
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getMarketOrderbookDepth(
                    fSymbol, tSymbol, limit)
                INSERT_OKEX_MARKET_DEPTH_SQL = INSERT_MARKET_DEPTH_SQL.substitute(
                    server=str(self._okexConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_price_size=str(
                        sqlite_escape(json.dumps(base["bid_price_size"]))),
                    ask_price_size=str(
                        sqlite_escape(json.dumps(base["ask_price_size"]))))
                self._logger.debug(INSERT_OKEX_MARKET_DEPTH_SQL)
                curs.execute(INSERT_OKEX_MARKET_DEPTH_SQL)
            # Binnance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getMarketOrderbookDepth(
                    fSymbol, tSymbol, limit)
                INSERT_BINANCE_MARKET_DEPTH_SQL = INSERT_MARKET_DEPTH_SQL.substitute(
                    server=str(self._binanceConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_price_size=str(
                        sqlite_escape(json.dumps(base["bid_price_size"]))),
                    ask_price_size=str(
                        sqlite_escape(json.dumps(base["ask_price_size"]))))
                self._logger.debug(INSERT_BINANCE_MARKET_DEPTH_SQL)
                curs.execute(INSERT_BINANCE_MARKET_DEPTH_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertMarketKline(self, exchange, fSymbol, tSymbol, interval, start,
                          end):
        self._logger.debug(
            "src.core.db.db.DB.insertMarketKline: { exchange=%s, fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s }"
            % (exchange, fSymbol, tSymbol, interval, start, end))
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getMarketKline(fSymbol, tSymbol, interval,
                                                 start, end)
                for b in base:
                    INSERT_OKEX_MARKET_KLINE_SQL = INSERT_MARKET_KLINE_SQL.substitute(
                        server=str(self._okexConf["exchange"]),
                        timeStamp=int(b["timeStamp"]),
                        fSymbol=str(b["fSymbol"]),
                        tSymbol=str(b["tSymbol"]),
                        open=float(b["open"]),
                        high=float(b["high"]),
                        low=float(b["low"]),
                        close=float(b["close"]),
                        volume=float(b["volume"]))
                    self._logger.debug(INSERT_OKEX_MARKET_KLINE_SQL)
                    curs.execute(INSERT_OKEX_MARKET_KLINE_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getMarketKline(fSymbol, tSymbol, interval,
                                                    start, end)
                for b in base:
                    INSERT_BINANCE_MARKET_KLINE_SQL = INSERT_MARKET_KLINE_SQL.substitute(
                        server=str(self._binanceConf["exchange"]),
                        timeStamp=int(b["timeStamp"]),
                        fSymbol=str(b["fSymbol"]),
                        tSymbol=str(b["tSymbol"]),
                        open=float(b["open"]),
                        high=float(b["high"]),
                        low=float(b["low"]),
                        close=float(b["close"]),
                        volume=float(b["volume"]))
                    self._logger.debug(INSERT_BINANCE_MARKET_KLINE_SQL)
                    curs.execute(INSERT_BINANCE_MARKET_KLINE_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertMarketTicker(self, exchange, fSymbol, tSymbol):
        self._logger.debug("src.core.db.db.DB.insertMarketTicker: { exchange=%s, fSymbol=%s, tSymbol=%s }" % (exchange, fSymbol， tSymbol))
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getMarketOrderbookTicker(fSymbol, tSymbol)
                INSERT_OKEX_MARKET_TIKER_SQL = INSERT_MARKET_TIKER_SQL.substitute(
                    server=str(self._okexConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_one_price=float(base["bid_one_price"]),
                    bid_one_size=float(base["bid_one_size"]),
                    ask_one_price=float(base["ask_one_price"]),
                    ask_one_size=float(base["ask_one_size"]))
                self._logger.debug(INSERT_OKEX_MARKET_TIKER_SQL)
                curs.execute(INSERT_OKEX_MARKET_TIKER_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getMarketOrderbookTicker(fSymbol, tSymbol)
                INSERT_BINANCE_MARKET_TIKER_SQL = INSERT_MARKET_TIKER_SQL.substitute(
                    server=str(self._binanceConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_one_price=float(base["bid_one_price"]),
                    bid_one_size=float(base["bid_one_size"]),
                    ask_one_price=float(base["ask_one_price"]),
                    ask_one_size=float(base["ask_one_size"]))
                self._logger.debug(INSERT_BINANCE_MARKET_TIKER_SQL)
                curs.execute(INSERT_BINANCE_MARKET_TIKER_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertInfoServer(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertInfoServer: { exchange=%s }" % exchange)
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                res = self._okex.getServerLimits()
                INSERT_OKEX_INFO_SERVER_SQL = INSERT_INFO_SERVER_SQL.substitute(
                    server=str(self._okexConf["exchange"]),
                    requests_second="NULL" if res["requests_second"] == '' else
                    float(res["requests_second"]),
                    orders_second="NULL" if res["orders_second"] == '' else
                    float(res["orders_second"]),
                    orders_day="NULL"
                    if res["orders_day"] == '' else float(res["orders_day"]),
                    webSockets_second="NULL" if res["webSockets_second"] == ''
                    else float(res["webSockets_second"]))
                self._logger.debug(INSERT_OKEX_INFO_SERVER_SQL)
                curs.execute(INSERT_OKEX_INFO_SERVER_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                res = self._binance.getServerLimits()
                INSERT_BINANCE_INFO_SERVER_SQL = INSERT_INFO_SERVER_SQL.substitute(
                    server=str(self._binanceConf["exchange"]),
                    requests_second="NULL" if res["requests_second"] == '' else
                    float(res["requests_second"]),
                    orders_second="NULL" if res["orders_second"] == '' else
                    float(res["orders_second"]),
                    orders_day="NULL"
                    if res["orders_day"] == '' else float(res["orders_day"]),
                    webSockets_second="NULL" if res["webSockets_second"] == ''
                    else float(res["webSockets_second"]))
                self._logger.debug(INSERT_BINANCE_INFO_SERVER_SQL)
                curs.execute(INSERT_BINANCE_INFO_SERVER_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertInfoSymbol(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertInfoSymbol: { exchange=%s }" % exchange)
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getSymbolsLimits()
                fees = self._okex.getTradeFees()
                for b in base:
                    fees_key = fees[0]
                    INSERT_OKEX_INFO_SYMBOL_SQL = INSERT_INFO_SYMBOL_SQL.substitute(
                        server=str(self._okexConf["exchange"]),
                        fSymbol=str(b["fSymbol"]),
                        tSymbol=str(b["tSymbol"]),
                        limit_price_precision="NULL"
                        if b["tSymbol_price"]["precision"] == '' else float(
                            b["tSymbol_price"]["precision"]),
                        limit_price_max="NULL"
                        if b["tSymbol_price"]["max"] == '' else float(
                            b["tSymbol_price"]["max"]),
                        limit_price_min="NULL"
                        if b["tSymbol_price"]["min"] == '' else float(
                            b["tSymbol_price"]["min"]),
                        limit_price_step="NULL"
                        if b["tSymbol_price"]["step"] == '' else float(
                            b["tSymbol_price"]["step"]),
                        limit_size_precision="NULL"
                        if b["fSymbol_size"]["precision"] == '' else float(
                            b["fSymbol_size"]["precision"]),
                        limit_size_max="NULL" if b["fSymbol_size"]["max"] == ''
                        else float(b["fSymbol_size"]["max"]),
                        limit_size_min="NULL" if b["fSymbol_size"]["min"] == ''
                        else float(b["fSymbol_size"]["min"]),
                        limit_size_step="NULL"
                        if b["fSymbol_size"]["step"] == '' else float(
                            b["fSymbol_size"]["step"]),
                        limit_min_notional="NULL" if b["min_notional"] == ''
                        else float(b["min_notional"]),
                        fee_maker="NULL" if fees_key["maker"] == '' else float(
                            fees_key["maker"]),
                        fee_taker="NULL" if fees_key["taker"] == '' else float(
                            fees_key["taker"]))
                    self._logger.debug(INSERT_OKEX_INFO_SYMBOL_SQL)
                    curs.execute(INSERT_OKEX_INFO_SYMBOL_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getSymbolsLimits()
                fees = self._binance.getTradeFees()
                for b in base:
                    fees_key = ''
                    for f in fees:
                        if f["symbol"] == b["fSymbol"] + b["tSymbol"]:
                            fees_key = f
                    INSERT_BINANCE_INFO_SYMBOL_SQL = INSERT_INFO_SYMBOL_SQL.substitute(
                        server=str(self._binanceConf["exchange"]),
                        fSymbol=str(b["fSymbol"]),
                        tSymbol=str(b["tSymbol"]),
                        limit_price_precision="NULL"
                        if b["tSymbol_price"]["precision"] == '' else float(
                            b["tSymbol_price"]["precision"]),
                        limit_price_max="NULL"
                        if b["tSymbol_price"]["max"] == '' else float(
                            b["tSymbol_price"]["max"]),
                        limit_price_min="NULL"
                        if b["tSymbol_price"]["min"] == '' else float(
                            b["tSymbol_price"]["min"]),
                        limit_price_step="NULL"
                        if b["tSymbol_price"]["step"] == '' else float(
                            b["tSymbol_price"]["step"]),
                        limit_size_precision="NULL"
                        if b["fSymbol_size"]["precision"] == '' else float(
                            b["fSymbol_size"]["precision"]),
                        limit_size_max="NULL" if b["fSymbol_size"]["max"] == ''
                        else float(b["fSymbol_size"]["max"]),
                        limit_size_min="NULL" if b["fSymbol_size"]["min"] == ''
                        else float(b["fSymbol_size"]["min"]),
                        limit_size_step="NULL"
                        if b["fSymbol_size"]["step"] == '' else float(
                            b["fSymbol_size"]["step"]),
                        limit_min_notional="NULL" if b["min_notional"] == ''
                        else float(b["min_notional"]),
                        fee_maker="NULL" if fees_key["maker"] == '' else float(
                            fees_key["maker"]),
                        fee_taker="NULL" if fees_key["taker"] == '' else float(
                            fees_key["taker"]))
                    self._logger.debug(INSERT_BINANCE_INFO_SYMBOL_SQL)
                    curs.execute(INSERT_BINANCE_INFO_SYMBOL_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertTradeBacktestHistory(self,
                                   exchange,
                                   fSymbol,
                                   tSymbol,
                                   ask_or_bid,
                                   price,
                                   quantity,
                                   ratio='',
                                   type="limit"):
        self._logger.debug("src.core.db.db.DB.insertTradeBacktestHistory: { exchange=%s, fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, ratio=%s, type=%s }" % (exchange, fSymbol, tSymbol, ask_or_bid, price, ratio, type))
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                timeStamp = utcnow_timestamp()
                order_id = '0x' + str(timeStamp)
                status = 'filled'
                if ratio == '':
                    ratio = self._okex.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                INSERT_OKEX_TRADE_BACKTEST_HISTORY_SQL = INSERT_TRADE_BACKTEST_HISTORY_SQL.substitute(
                    server=str(self._okexConf["exchange"]),
                    timeStamp=int(timeStamp),
                    order_id=str(order_id),
                    status=str(status),
                    type=str(type),
                    fSymbol=str(fSymbol),
                    tSymbol=str(tSymbol),
                    ask_or_bid=str(ask_or_bid),
                    ask_bid_price=float(price),
                    ask_bid_size=float(quantity),
                    filled_price=float(price),
                    filled_size=float(quantity),
                    fee=float(fee))
                self._logger.debug(INSERT_OKEX_TRADE_BACKTEST_HISTORY_SQL)
                curs.execute(INSERT_OKEX_TRADE_BACKTEST_HISTORY_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                timeStamp = utcnow_timestamp()
                order_id = '0x' + str(timeStamp)
                status = 'filled'
                if ratio == '':
                    ratio = self._binance.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                INSERT_BINANCE_TRADE_BACKTEST_HISTORY_SQL = INSERT_TRADE_BACKTEST_HISTORY_SQL.substitute(
                    server=str(self._binanceConf["exchange"]),
                    timeStamp=int(timeStamp),
                    order_id=str(order_id),
                    status=str(status),
                    type=str(type),
                    fSymbol=str(fSymbol),
                    tSymbol=str(tSymbol),
                    ask_or_bid=str(ask_or_bid),
                    ask_bid_price=float(price),
                    ask_bid_size=float(quantity),
                    filled_price=float(price),
                    filled_size=float(quantity),
                    fee=float(fee))
                self._logger.debug(INSERT_BINANCE_TRADE_BACKTEST_HISTORY_SQL)
                curs.execute(INSERT_BINANCE_TRADE_BACKTEST_HISTORY_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertTradeOrderHistory(self,
                                exchange,
                                fSymbol,
                                tSymbol,
                                ask_or_bid,
                                price,
                                quantity,
                                ratio='',
                                type="limit"):
        self._logger.debug("src.core.db.db.DB.insertTradeOrderHistory: { exchange=%s, fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, ratio=%s, type=%s }" % (exchange, fSymbol, tSymbol, ask_or_bid, price, ratio, type))
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.createOrder(fSymbol, tSymbol, ask_or_bid,
                                              price, quantity, ratio, type)
                INSERT_OKEX_TRADE_ORDER_HISTORY_SQL = INSERT_TRADE_ORDER_HISTORY_SQL.substitute(
                    server=str(self._okexConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    order_id=str(base["order_id"]),
                    status=str(base["status"]),
                    type=str(base["type"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    ask_or_bid=str(base["ask_or_bid"]),
                    ask_bid_price=float(base["ask_bid_price"]),
                    ask_bid_size=float(base["ask_bid_size"]),
                    filled_price=float(base["filled_price"]),
                    filled_size=float(base["filled_size"]),
                    fee=float(base["fee"]))
                self._logger.debug(INSERT_OKEX_TRADE_ORDER_HISTORY_SQL)
                curs.execute(INSERT_OKEX_TRADE_ORDER_HISTORY_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.createOrder(fSymbol, tSymbol, ask_or_bid,
                                                 price, quantity, ratio, type)
                INSERT_BINANCE_TRADE_ORDER_HISTORY_SQL = INSERT_TRADE_ORDER_HISTORY_SQL.substitute(
                    server=str(self._binanceConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    order_id=str(base["order_id"]),
                    status=str(base["status"]),
                    type=str(base["type"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    ask_or_bid=str(base["ask_or_bid"]),
                    ask_bid_price=float(base["ask_bid_price"]),
                    ask_bid_size=float(base["ask_bid_size"]),
                    filled_price=float(base["filled_price"]),
                    filled_size=float(base["filled_size"]),
                    fee=float(base["fee"]))
                self._logger.debug(INSERT_BINANCE_TRADE_ORDER_HISTORY_SQL)
                curs.execute(INSERT_BINANCE_TRADE_ORDER_HISTORY_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertAccountWithdrawHistory(self, exchange, asset):
        self._logger.debug("src.core.db.db.DB.insertAccountWithdrawHistory: { exchange=%s, asset=%s }" % (exchange, asset))
        try:
            curs = self._conn.cursor()
            timeStamp = utcnow_timestamp()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getAccountAssetDetail(asset)
                INSERT_OKEX_WITHDRAW_HISTORY_SQL = INSERT_WITHDRAW_HISTORY_SQL.substitute(
                    server=str(self._okexConf["exchange"]),
                    timeStamp=int(timeStamp),
                    asset=str(asset),
                    deposite=str(
                        sqlite_escape(', '.join(
                            json.dumps(b) for b in base["deposit"]))),
                    withdraw=str(
                        sqlite_escape(', '.join(
                            json.dumps(b) for b in base["withdraw"]))))
                self._logger.debug(INSERT_OKEX_WITHDRAW_HISTORY_SQL)
                curs.execute(INSERT_OKEX_WITHDRAW_HISTORY_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getAccountAssetDetail(asset)
                INSERT_BINANCE_WITHDRAW_HISTORY_SQL = INSERT_WITHDRAW_HISTORY_SQL.substitute(
                    server=str(self._binanceConf["exchange"]),
                    timeStamp=int(timeStamp),
                    asset=str(asset),
                    deposite=str(
                        sqlite_escape(', '.join(
                            json.dumps(b) for b in base["deposit"]))),
                    withdraw=str(
                        sqlite_escape(', '.join(
                            json.dumps(b) for b in base["withdraw"]))))
                self._logger.debug(INSERT_BINANCE_WITHDRAW_HISTORY_SQL)
                curs.execute(INSERT_BINANCE_WITHDRAW_HISTORY_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)

    def insertInfoWithdraw(self, exchange="all"):
        self._logger.debug("src.core.db.db.DB.insertInfoWithdraw: { exchange=%s}" % exchange)
        try:
            curs = self._conn.cursor()
            # OKEX
            if exchange == "all" or self._okexConf["exchange"] in exchange:
                base = self._okex.getAccountLimits()
                for b in base:
                    INSERT_OKEX_INFO_WITHDRAW_SQL = INSERT_INFO_WITHDRAW_SQL.substitute(
                        server=str(self._okexConf["exchange"]),
                        asset=str(b["asset"]),
                        can_deposite=str(b["can_deposite"]),
                        can_withdraw=str(b["can_withdraw"]),
                        min_withdraw=float(b["min_withdraw"]))
                    self._logger.debug(INSERT_OKEX_INFO_WITHDRAW_SQL)
                    curs.execute(INSERT_OKEX_INFO_WITHDRAW_SQL)
            # Binance
            if exchange == "all" or self._binanceConf["exchange"] in exchange:
                base = self._binance.getAccountLimits()
                for b in base:
                    INSERT_BINANCE_INFO_WITHDRAW_SQL = INSERT_INFO_WITHDRAW_SQL.substitute(
                        server=str(self._binanceConf["exchange"]),
                        asset=str(b["asset"]),
                        can_deposite=str(b["can_deposite"]),
                        can_withdraw=str(b["can_withdraw"]),
                        min_withdraw=float(b["min_withdraw"]))
                    self._logger.debug(INSERT_BINANCE_INFO_WITHDRAW_SQL)
                    curs.execute(INSERT_BINANCE_INFO_WITHDRAW_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self._conn.commit()
            curs.close()
        except (OkexException, BinanceException, sqlite3.Error) as err:
            raise DBException(err)
