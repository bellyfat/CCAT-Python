# -*- coding: utf-8 -*-

import json
import os
import sqlite3

from src.core.coin.binance import Binance
from src.core.coin.okex import Okex
from src.core.config import Config
from src.core.db.sql import *
from src.core.util.exceptions import DBException
from src.core.util.helper import utcnow_timestamp, sqlite_escape
from src.core.util.log import Logger

proxies = Config()._proxies

binanceConf = Config()._binance
binance = Binance(binanceConf["exchange"], binanceConf["api_key"],
                  binanceConf["api_secret"], proxies["url"])

okexConf = Config()._okex
okex = Okex(okexConf["exchange"], okexConf["api_key"],
            okexConf["api_secret"], okexConf["passphrase"], proxies["url"])

logger = Logger()

# db class


class DB(object):
    def __init__(self, dbStr):
        self.dbStr = dbStr
        self.conn = sqlite3.connect(dbStr)

    def __del__(self):
        self.conn.close()

    def initDB(self):
        try:
            self.conn.close()
            os.remove(self.dbStr)
            self.conn = sqlite3.connect(self.dbStr)
        except IOError as err:
            raise DBException

    def getTables(self):
        logger.debug(GET_TABLES_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_TABLES_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def creatTables(self):
        logger.debug(CREATE_TABELS_SQL)
        try:
            curs = self.conn.cursor()
            curs.executescript(CREATE_TABELS_SQL)
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def getAccountInfo(self):
        logger.debug(GET_ACCOUNT_INFO_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_ACCOUNT_INFO_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getMarketDepth(self):
        logger.debug(GET_MARKET_DEPTH_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_MARKET_DEPTH_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getMarketKline(self):
        logger.debug(GET_MARKET_KLINE_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_MARKET_KLINE_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getMarketTicker(self):
        logger.debug(GET_MARKET_TIKER_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_MARKET_TIKER_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getServerInfo(self):
        logger.debug(GET_SERVER_INFO_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_SERVER_INFO_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getSymbolInfo(self):
        logger.debug(GET_SYMBOL_INFO_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_SYMBOL_INFO_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getTradeBacktestHistory(self):
        logger.debug(GET_TRADE_BACKTEST_HISTORY_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_TRADE_BACKTEST_HISTORY_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getTradeOrderHistory(self):
        logger.debug(GET_TRADE_ORDER_HISTORY_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_TRADE_ORDER_HISTORY_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getWithdrawHistory(self):
        logger.debug(GET_WITHDRAW_HISTORY_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_WITHDRAW_HISTORY_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def getWithdrawInfo(self):
        logger.debug(GET_WITHDRAW_INFO_SQL)
        try:
            curs = self.conn.cursor()
            curs.execute(GET_WITHDRAW_INFO_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except sqlite3.Error as err:
            raise DBException

    def insertAccountInfo(self, exchange):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                timeStamp = okex.getServerTime()
                base = okex.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        INSERT_OKEX_ACCOUNT_INFO_SQL = INSERT_ACCOUNT_INFO_SQL.substitute(
                            server=str(okexConf["exchange"]),
                            timeStamp=int(timeStamp),
                            asset=str(b["asset"]),
                            balance=float(b["balance"]),
                            free=float(b["free"]),
                            locked=float(b["locked"])
                        )
                        logger.debug(INSERT_OKEX_ACCOUNT_INFO_SQL)
                        curs.execute(INSERT_OKEX_ACCOUNT_INFO_SQL)
            # Binance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                timeStamp = binance.getServerTime()
                base = binance.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        INSERT_BINANCE_ACCOUNT_INFO_SQL = INSERT_ACCOUNT_INFO_SQL.substitute(
                            server=str(binanceConf["exchange"]),
                            timeStamp=int(timeStamp),
                            asset=str(b["asset"]),
                            balance=float(b["balance"]),
                            free=float(b["free"]),
                            locked=float(b["locked"])
                        )
                        logger.debug(INSERT_BINANCE_ACCOUNT_INFO_SQL)
                        curs.execute(INSERT_BINANCE_ACCOUNT_INFO_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertMarketDepth(self, exchange, fSymbol, tSymbol, limit=100):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                base = okex.getMarketOrderbookDepth(fSymbol, tSymbol, limit)
                INSERT_OKEX_MARKET_DEPTH_SQL = INSERT_MARKET_DEPTH_SQL.substitute(
                    server=str(okexConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_price_size=str(sqlite_escape(
                        json.dumps(base["bid_price_size"]))),
                    ask_price_size=str(sqlite_escape(
                        json.dumps(base["ask_price_size"])))
                )
                logger.debug(INSERT_OKEX_MARKET_DEPTH_SQL)
                curs.execute(INSERT_OKEX_MARKET_DEPTH_SQL)
            # Binnance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                base = binance.getMarketOrderbookDepth(fSymbol, tSymbol, limit)
                INSERT_BINANCE_MARKET_DEPTH_SQL = INSERT_MARKET_DEPTH_SQL.substitute(
                    server=str(binanceConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_price_size=str(sqlite_escape(
                        json.dumps(base["bid_price_size"]))),
                    ask_price_size=str(sqlite_escape(
                        json.dumps(base["ask_price_size"])))
                )
                logger.debug(INSERT_BINANCE_MARKET_DEPTH_SQL)
                curs.execute(INSERT_BINANCE_MARKET_DEPTH_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertMarketKline(self, exchange, fSymbol, tSymbol, interval, start, end):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                base = okex.getMarketKline(
                    fSymbol, tSymbol, interval, start, end)
                for b in base:
                    INSERT_OKEX_MARKET_KLINE_SQL = INSERT_MARKET_KLINE_SQL.substitute(
                        server=str(okexConf["exchange"]),
                        timeStamp=int(b["timeStamp"]),
                        fSymbol=str(b["fSymbol"]),
                        tSymbol=str(b["tSymbol"]),
                        open=float(b["open"]),
                        high=float(b["high"]),
                        low=float(b["low"]),
                        close=float(b["close"]),
                        volume=float(b["volume"])
                    )
                    logger.debug(INSERT_OKEX_MARKET_KLINE_SQL)
                    curs.execute(INSERT_OKEX_MARKET_KLINE_SQL)
            # Binance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                base = binance.getMarketKline(
                    fSymbol, tSymbol, interval, start, end)
                for b in base:
                    INSERT_BINANCE_MARKET_KLINE_SQL = INSERT_MARKET_KLINE_SQL.substitute(
                        server=str(binanceConf["exchange"]),
                        timeStamp=int(b["timeStamp"]),
                        fSymbol=str(b["fSymbol"]),
                        tSymbol=str(b["tSymbol"]),
                        open=float(b["open"]),
                        high=float(b["high"]),
                        low=float(b["low"]),
                        close=float(b["close"]),
                        volume=float(b["volume"])
                    )
                    logger.debug(INSERT_BINANCE_MARKET_KLINE_SQL)
                    curs.execute(INSERT_BINANCE_MARKET_KLINE_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertMarketTicker(self, exchange, fSymbol, tSymbol):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                base = okex.getMarketOrderbookTicker(fSymbol, tSymbol)
                INSERT_OKEX_MARKET_TIKER_SQL = INSERT_MARKET_TIKER_SQL.substitute(
                    server=str(okexConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_one_price=float(base["bid_one_price"]),
                    bid_one_size=float(base["bid_one_size"]),
                    ask_one_price=float(base["ask_one_price"]),
                    ask_one_size=float(base["ask_one_size"])
                )
                logger.debug(INSERT_OKEX_MARKET_TIKER_SQL)
                curs.execute(INSERT_OKEX_MARKET_TIKER_SQL)
            # Binance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                base = binance.getMarketOrderbookTicker(fSymbol, tSymbol)
                INSERT_BINANCE_MARKET_TIKER_SQL = INSERT_MARKET_TIKER_SQL.substitute(
                    server=str(binanceConf["exchange"]),
                    timeStamp=int(base["timeStamp"]),
                    fSymbol=str(base["fSymbol"]),
                    tSymbol=str(base["tSymbol"]),
                    bid_one_price=float(base["bid_one_price"]),
                    bid_one_size=float(base["bid_one_size"]),
                    ask_one_price=float(base["ask_one_price"]),
                    ask_one_size=float(base["ask_one_size"])
                )
                logger.debug(INSERT_BINANCE_MARKET_TIKER_SQL)
                curs.execute(INSERT_BINANCE_MARKET_TIKER_SQL)
            # Huobi
            # if exchange == "all" or "huobi" in exchange:
            # to_be_continue
            # Gate
            # if exchange == "all" or "gate" in exchange:
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertServerInfo(self):
        try:
            curs = self.conn.cursor()
            # OKEX
            res = okex.getServerLimits()
            INSERT_OKEX_SERVER_INFO_SQL = INSERT_SERVER_INFO_SQL.substitute(
                server=str(okexConf["exchange"]),
                requests_second="NULL" if res["requests_second"] == '' else float(
                    res["requests_second"]),
                orders_second="NULL" if res["orders_second"] == '' else float(
                    res["orders_second"]),
                orders_day="NULL" if res["orders_day"] == '' else float(
                    res["orders_day"]),
                webSockets_second="NULL" if res["webSockets_second"] == '' else float(
                    res["webSockets_second"])
            )
            logger.debug(INSERT_OKEX_SERVER_INFO_SQL)
            # binance
            res = binance.getServerLimits()
            INSERT_BINANCE_SERVER_INFO_SQL = INSERT_SERVER_INFO_SQL.substitute(
                server=str(binanceConf["exchange"]),
                requests_second="NULL" if res["requests_second"] == '' else float(
                    res["requests_second"]),
                orders_second="NULL" if res["orders_second"] == '' else float(
                    res["orders_second"]),
                orders_day="NULL" if res["orders_day"] == '' else float(
                    res["orders_day"]),
                webSockets_second="NULL" if res["webSockets_second"] == '' else float(
                    res["webSockets_second"])
            )
            logger.debug(INSERT_BINANCE_SERVER_INFO_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            curs.execute(INSERT_OKEX_SERVER_INFO_SQL)
            curs.execute(INSERT_BINANCE_SERVER_INFO_SQL)
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertSymbolInfo(self):
        try:
            curs = self.conn.cursor()
            # OKEX
            base = okex.getSymbolsLimits()
            fees = okex.getTradeFees()
            for b in base:
                fees_key = fees[0]
                INSERT_OKEX_SYMBOL_INFO_SQL = INSERT_SYMBOL_INFO_SQL.substitute(
                    server=str(okexConf["exchange"]),
                    fSymbol=str(b["fSymbol"]),
                    tSymbol=str(b["tSymbol"]),
                    limit_price_precision="NULL" if b["tSymbol_price"]["precision"] == '' else float(
                        b["tSymbol_price"]["precision"]),
                    limit_price_max="NULL" if b["tSymbol_price"]["max"] == '' else float(
                        b["tSymbol_price"]["max"]),
                    limit_price_min="NULL" if b["tSymbol_price"]["min"] == '' else float(
                        b["tSymbol_price"]["min"]),
                    limit_price_step="NULL" if b["tSymbol_price"]["step"] == '' else float(
                        b["tSymbol_price"]["step"]),
                    limit_size_precision="NULL" if b["fSymbol_size"]["precision"] == '' else float(
                        b["fSymbol_size"]["precision"]),
                    limit_size_max="NULL" if b["fSymbol_size"]["max"] == '' else float(
                        b["fSymbol_size"]["max"]),
                    limit_size_min="NULL" if b["fSymbol_size"]["min"] == '' else float(
                        b["fSymbol_size"]["min"]),
                    limit_size_step="NULL" if b["fSymbol_size"]["step"] == '' else float(
                        b["fSymbol_size"]["step"]),
                    limit_min_notional="NULL" if b["min_notional"] == '' else float(
                        b["min_notional"]),
                    fee_maker="NULL" if fees_key["maker"] == '' else float(
                        fees_key["maker"]),
                    fee_taker="NULL" if fees_key["taker"] == '' else float(
                        fees_key["taker"])
                )
                logger.debug(INSERT_OKEX_SYMBOL_INFO_SQL)
                curs.execute(INSERT_OKEX_SYMBOL_INFO_SQL)
            # binance
            base = binance.getSymbolsLimits()
            fees = binance.getTradeFees()
            for b in base:
                fees_key = ''
                for f in fees:
                    if f["symbol"] == b["fSymbol"] + b["tSymbol"]:
                        fees_key = f
                INSERT_BINANCE_SYMBOL_INFO_SQL = INSERT_SYMBOL_INFO_SQL.substitute(
                    server=str(binanceConf["exchange"]),
                    fSymbol=str(b["fSymbol"]),
                    tSymbol=str(b["tSymbol"]),
                    limit_price_precision="NULL" if b["tSymbol_price"]["precision"] == '' else float(
                        b["tSymbol_price"]["precision"]),
                    limit_price_max="NULL" if b["tSymbol_price"]["max"] == '' else float(
                        b["tSymbol_price"]["max"]),
                    limit_price_min="NULL" if b["tSymbol_price"]["min"] == '' else float(
                        b["tSymbol_price"]["min"]),
                    limit_price_step="NULL" if b["tSymbol_price"]["step"] == '' else float(
                        b["tSymbol_price"]["step"]),
                    limit_size_precision="NULL" if b["fSymbol_size"]["precision"] == '' else float(
                        b["fSymbol_size"]["precision"]),
                    limit_size_max="NULL" if b["fSymbol_size"]["max"] == '' else float(
                        b["fSymbol_size"]["max"]),
                    limit_size_min="NULL" if b["fSymbol_size"]["min"] == '' else float(
                        b["fSymbol_size"]["min"]),
                    limit_size_step="NULL" if b["fSymbol_size"]["step"] == '' else float(
                        b["fSymbol_size"]["step"]),
                    limit_min_notional="NULL" if b["min_notional"] == '' else float(
                        b["min_notional"]),
                    fee_maker="NULL" if fees_key["maker"] == '' else float(
                        fees_key["maker"]),
                    fee_taker="NULL" if fees_key["taker"] == '' else float(
                        fees_key["taker"])
                )
                logger.debug(INSERT_BINANCE_SYMBOL_INFO_SQL)
                curs.execute(INSERT_BINANCE_SYMBOL_INFO_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertTradeBacktestHistory(self, exchange, fSymbol, tSymbol, ask_or_bid, price, quantity, ratio='', type="limit"):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                timeStamp = utcnow_timestamp()
                order_id = '0x' + str(timeStamp)
                status = 'filled'
                if ratio == '':
                    ratio = okex.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                INSERT_OKEX_TRADE_BACKTEST_HISTORY_SQL = INSERT_TRADE_BACKTEST_HISTORY_SQL.substitute(
                    server=str(okexConf["exchange"]),
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
                    fee=float(fee)
                )
                logger.debug(INSERT_OKEX_TRADE_BACKTEST_HISTORY_SQL)
                curs.execute(INSERT_OKEX_TRADE_BACKTEST_HISTORY_SQL)
            # Binance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                timeStamp = utcnow_timestamp()
                order_id = '0x' + str(timeStamp)
                status = 'filled'
                if ratio == '':
                    ratio = binance.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                INSERT_BINANCE_TRADE_BACKTEST_HISTORY_SQL = INSERT_TRADE_BACKTEST_HISTORY_SQL.substitute(
                    server=str(binanceConf["exchange"]),
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
                    fee=float(fee)
                )
                logger.debug(INSERT_BINANCE_TRADE_BACKTEST_HISTORY_SQL)
                curs.execute(INSERT_BINANCE_TRADE_BACKTEST_HISTORY_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertTradeOrderHistory(self, exchange, fSymbol, tSymbol, ask_or_bid, price, quantity, ratio='', type="limit"):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                base = okex.createOrder(
                    fSymbol, tSymbol, ask_or_bid, price, quantity, ratio, type)
                INSERT_OKEX_TRADE_ORDER_HISTORY_SQL = INSERT_TRADE_ORDER_HISTORY_SQL.substitute(
                    server=str(okexConf["exchange"]),
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
                    fee=float(base["fee"])
                )
                logger.debug(INSERT_OKEX_TRADE_ORDER_HISTORY_SQL)
                curs.execute(INSERT_OKEX_TRADE_ORDER_HISTORY_SQL)
            # Binance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                base = binance.createOrder(
                    fSymbol, tSymbol, ask_or_bid, price, quantity, ratio, type)
                INSERT_BINANCE_TRADE_ORDER_HISTORY_SQL = INSERT_TRADE_ORDER_HISTORY_SQL.substitute(
                    server=str(binanceConf["exchange"]),
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
                    fee=float(base["fee"])
                )
                logger.debug(INSERT_BINANCE_TRADE_ORDER_HISTORY_SQL)
                curs.execute(INSERT_BINANCE_TRADE_ORDER_HISTORY_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertWithdrawHistory(self, exchange, asset):
        try:
            curs = self.conn.cursor()
            # OKEX
            if exchange == "all" or okexConf["exchange"] in exchange:
                timeStamp = okex.getServerTime()
                base = okex.getAccountAssetDetail(asset)
                INSERT_OKEX_WITHDRAW_HISTORY_SQL = INSERT_WITHDRAW_HISTORY_SQL.substitute(
                    server=str(okexConf["exchange"]),
                    timeStamp=int(timeStamp),
                    deposite=str(sqlite_escape(', '.join(json.dumps(b)
                                                         for b in base["deposit"]))),
                    withdraw=str(sqlite_escape(', '.join(json.dumps(b)
                                                         for b in base["withdraw"])))
                )
                logger.debug(INSERT_OKEX_WITHDRAW_HISTORY_SQL)
                curs.execute(INSERT_OKEX_WITHDRAW_HISTORY_SQL)
            # Binance
            if exchange == "all" or binanceConf["exchange"] in exchange:
                timeStamp = binance.getServerTime()
                base = binance.getAccountAssetDetail(asset)
                INSERT_BINANCE_WITHDRAW_HISTORY_SQL = INSERT_WITHDRAW_HISTORY_SQL.substitute(
                    server=str(binanceConf["exchange"]),
                    timeStamp=int(timeStamp),
                    deposite=str(sqlite_escape(', '.join(json.dumps(b)
                                                         for b in base["deposit"]))),
                    withdraw=str(sqlite_escape(', '.join(json.dumps(b)
                                                         for b in base["withdraw"])))
                )
                logger.debug(INSERT_BINANCE_WITHDRAW_HISTORY_SQL)
                curs.execute(INSERT_BINANCE_WITHDRAW_HISTORY_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException

    def insertWithdrawInfo(self):
        try:
            curs = self.conn.cursor()
            # OKEX
            base = okex.getAccountLimits()
            for b in base:
                INSERT_OKEX_WITHDRAW_INFO_SQL = INSERT_WITHDRAW_INFO_SQL.substitute(
                    server=str(okexConf["exchange"]),
                    asset=str(b["asset"]),
                    can_deposite=str(b["can_deposite"]),
                    can_withdraw=str(b["can_withdraw"]),
                    min_withdraw=float(b["min_withdraw"])
                )
                logger.debug(INSERT_OKEX_WITHDRAW_INFO_SQL)
                curs.execute(INSERT_OKEX_WITHDRAW_INFO_SQL)
            # Binance
            base = binance.getAccountLimits()
            for b in base:
                INSERT_BINANCE_WITHDRAW_INFO_SQL = INSERT_WITHDRAW_INFO_SQL.substitute(
                    server=str(binanceConf["exchange"]),
                    asset=str(b["asset"]),
                    can_deposite=str(b["can_deposite"]),
                    can_withdraw=str(b["can_withdraw"]),
                    min_withdraw=float(b["min_withdraw"])
                )
                logger.debug(INSERT_BINANCE_WITHDRAW_INFO_SQL)
                curs.execute(INSERT_BINANCE_WITHDRAW_INFO_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self.conn.commit()
            curs.close()
        except sqlite3.Error as err:
            raise DBException
