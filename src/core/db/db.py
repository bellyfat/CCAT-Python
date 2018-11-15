# -*- coding: utf-8 -*-

import os
import sqlite3

from src.core.db.sql import *
from src.core.coin.okex import Okex
from src.core.coin.binance import Binance
from src.core.config import Config
from src.core.util.log import Logger
from src.core.util.exceptions import DBException

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

    def insertServerInfo(self):
        try:
            curs = self.conn.cursor()
            # OKEX
            res = okex.getServerLimits()
            INSERT_OKEX_SERVER_INFO_SQL = INSERT_SERVER_INFO_SQL.substitute(
                server=str(okexConf["exchange"]),
                requests_second="NULL" if res["requests_second"]=='' else float(res["requests_second"]),
                orders_second="NULL" if res["orders_second"]=='' else float(res["orders_second"]),
                orders_day="NULL" if res["orders_day"]=='' else float(res["orders_day"]),
                webSockets_second="NULL" if res["webSockets_second"]=='' else float(res["webSockets_second"])
            )
            logger.debug(INSERT_OKEX_SERVER_INFO_SQL)
            # binance
            res = binance.getServerLimits()
            INSERT_BINANCE_SERVER_INFO_SQL = INSERT_SERVER_INFO_SQL.substitute(
                server=str(binanceConf["exchange"]),
                requests_second="NULL" if res["requests_second"]=='' else float(res["requests_second"]),
                orders_second="NULL" if res["orders_second"]=='' else float(res["orders_second"]),
                orders_day="NULL" if res["orders_day"]=='' else float(res["orders_day"]),
                webSockets_second="NULL" if res["webSockets_second"]=='' else float(res["webSockets_second"])
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

    def insertSymbolInfo(self):
        try:
            curs = self.conn.cursor()
            # OKEX
            base = okex.getServerSymbols()
            fees = okex.getTradeFees()
            for key in base.keys():
                for value in base[key]:
                    res = okex.getSymbolsLimits(key, value)
                    INSERT_OKEX_SYMBOL_INFO_SQL = INSERT_SYMBOL_INFO_SQL.substitute(
                        server=str(okexConf["exchange"]),
                        fSymbol=str(key),
                        tSymbol=str(value),
                        limit_price_precision="NULL" if res["tSymbol_price"]["precision"]=='' else float(res["tSymbol_price"]["precision"]),
                        limit_price_max="NULL" if res["tSymbol_price"]["max"]=='' else float(res["tSymbol_price"]["max"]),
                        limit_price_min="NULL" if res["tSymbol_price"]["min"]=='' else float(res["tSymbol_price"]["min"]),
                        limit_price_step="NULL" if res["tSymbol_price"]["step"]=='' else float(res["tSymbol_price"]["step"]),
                        limit_size_precision="NULL" if res["fSymbol_size"]["precision"]=='' else float(res["fSymbol_size"]["precision"]),
                        limit_size_max="NULL" if res["fSymbol_size"]["max"]=='' else float(res["fSymbol_size"]["max"]),
                        limit_size_min="NULL" if res["fSymbol_size"]["min"]=='' else float(res["fSymbol_size"]["min"]),
                        limit_size_step="NULL" if res["fSymbol_size"]["step"]=='' else float(res["fSymbol_size"]["step"]),
                        limit_min_notional="NULL" if res["min_notional"]=='' else float(res["min_notional"]),
                        fee_maker="NULL" if fees[0]["maker"]=='' else float(fees[0]["maker"]),
                        fee_taker="NULL" if fees[0]["taker"]=='' else float(fees[0]["taker"])
                    )
                    logger.debug(INSERT_OKEX_SYMBOL_INFO_SQL)
                    curs.execute(INSERT_OKEX_SYMBOL_INFO_SQL)
            # binance
            base = binance.getServerSymbols()
            fees = binance.getTradeFees()
            for key in base.keys():
                for value in base[key]:
                    res = binance.getSymbolsLimits(key, value)
                    for f in fees:
                        if f["symbol"] == key+value:
                            fees_key = f
                    INSERT_BINANCE_SYMBOL_INFO_SQL = INSERT_SYMBOL_INFO_SQL.substitute(
                        server=str(binanceConf["exchange"]),
                        fSymbol=str(key),
                        tSymbol=str(value),
                        limit_price_precision="NULL" if res["tSymbol_price"]["precision"]=='' else float(res["tSymbol_price"]["precision"]),
                        limit_price_max="NULL" if res["tSymbol_price"]["max"]=='' else float(res["tSymbol_price"]["max"]),
                        limit_price_min="NULL" if res["tSymbol_price"]["min"]=='' else float(res["tSymbol_price"]["min"]),
                        limit_price_step="NULL" if res["tSymbol_price"]["step"]=='' else float(res["tSymbol_price"]["step"]),
                        limit_size_precision="NULL" if res["fSymbol_size"]["precision"]=='' else float(res["fSymbol_size"]["precision"]),
                        limit_size_max="NULL" if res["fSymbol_size"]["max"]=='' else float(res["fSymbol_size"]["max"]),
                        limit_size_min="NULL" if res["fSymbol_size"]["min"]=='' else float(res["fSymbol_size"]["min"]),
                        limit_size_step="NULL" if res["fSymbol_size"]["step"]=='' else float(res["fSymbol_size"]["step"]),
                        limit_min_notional="NULL" if res["min_notional"]=='' else float(res["min_notional"]),
                        fee_maker="NULL" if fees_key["maker"]=='' else float(fees_key["maker"]),
                        fee_taker="NULL" if fees_key["taker"]=='' else float(fees_key["taker"])
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

    def insertAccountInfo(self):
        try:
            curs = self.conn.cursor()
            # OKEX
            timeStamp = okex.getServerTime()
            base = okex.getAccountBalances()
            for b in base:
                if b["balance"]>0:
                    INSERT_OKEX_ACCOUNT_INFO_SQL = INSERT_ACCOUNT_INFO_SQL.substitute(
                        server=str(okexConf["exchange"]),
                        account="CCAT", # default
                        timeStamp=int(timeStamp),
                        asset=str(b["asset"]),
                        balance=float(b["balance"]),
                        free=float(b["free"]),
                        locked=float(b["locked"])
                    )
                    logger.debug(INSERT_OKEX_ACCOUNT_INFO_SQL)
                    curs.execute(INSERT_OKEX_ACCOUNT_INFO_SQL)
            # Binance
            timeStamp = binance.getServerTime()
            base = binance.getAccountBalances()
            for b in base:
                if b["balance"]>0:
                    INSERT_BINANCE_ACCOUNT_INFO_SQL = INSERT_ACCOUNT_INFO_SQL.substitute(
                        server=str(binanceConf["exchange"]),
                        account="CCAT", # default
                        timeStamp=int(timeStamp),
                        asset=b["asset"],
                        balance=b["balance"],
                        free=b["free"],
                        locked=b["locked"]
                    )
                    logger.debug(INSERT_BINANCE_ACCOUNT_INFO_SQL)
                    curs.execute(INSERT_BINANCE_ACCOUNT_INFO_SQL)
            # Huobi
            # to_be_continue
            # Gate
            # to_be_continue
            self.conn.commit()
            curs.close()
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
