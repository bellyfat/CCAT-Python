# -*- coding: utf-8 -*-

import json
import os
import sqlite3
import uuid

from src.core.coin.binance import Binance
from src.core.coin.enums import *
from src.core.coin.huobi import Huobi
from src.core.coin.okex import Okex
from src.core.config import Config
from src.core.db.sql import *
from src.core.util.exceptions import (BinanceException, DBException,
                                      HuobiException, OkexException)
from src.core.util.helper import dict_factory, sqlite_escape, utcnow_timestamp
from src.core.util.log import Logger


# db class
class DB(object):
    def __init__(self):
        # config init
        # exchanges
        self._exchanges = Config()._Main_exchanges
        self._excludeCoins = Config()._Main_excludeCoins
        self._baseCoin = Config()._Main_baseCoin
        self._basePriceVolume = Config()._Main_basePriceVolume
        self._basePriceTimeout = Config()._Main_basePriceTimeout
        self._baseJudgeTimeout = Config()._Main_baseJudgeTimeout
        self._baseStatisticTimeout = Config()._Main_baseStatisticTimeout
        self._judgeMarketTickerCycle = Config()._Main_judgeMarketTickerCycle
        self._statisticJudgeMarketTickerCycle = Config(
        )._Main_statisticJudgeMarketTickerCycle
        self._tradeHistoryCycle = Config()._Main_tradeHistoryCycle
        self._signalTradeCycle = Config()._Main_signalTradeCycle
        self._statisticSignalTradeCycle = Config()._Main_statisticSignalTradeCycle
        # proxies
        self._proxies = Config()._Proxies_url if Config(
        )._Proxies_proxies else None
        # DB
        self._dbStr = Config()._DB_url
        self._dbTimeout = Config()._DB_timeout
        self._dbSynchronous = Config()._DB_synchronous
        # Okex
        self._Okex_exchange = Config()._Okex_exchange
        self._Okex_api_key = Config()._Okex_api_key
        self._Okex_api_secret = Config()._Okex_api_secret
        self._Okex_passphrase = Config()._Okex_passphrase
        # Binance
        self._Binance_exchange = Config()._Binance_exchange
        self._Binance_api_key = Config()._Binance_api_key
        self._Binance_api_secret = Config()._Binance_api_secret
        # Huobi
        self._Huobi_exchange = Config()._Huobi_exchange
        self._Huobi_api_key = Config()._Huobi_api_key
        self._Huobi_api_secret = Config()._Huobi_api_secret
        self._Huobi_acct_id = Config()._Huobi_acct_id
        # 数据库 init
        self._conn = sqlite3.connect(
            self._dbStr, timeout=self._dbTimeout, check_same_thread=False)
        self._conn.row_factory = dict_factory
        if self._dbSynchronous:
            self._conn.execute("PRAGMA synchronous = 0")
        # Coin API init
        self._Okex = Okex(self._Okex_exchange, self._Okex_api_key,
                          self._Okex_api_secret, self._Okex_passphrase,
                          self._proxies)
        self._Binance = Binance(self._Binance_exchange, self._Binance_api_key,
                                self._Binance_api_secret, self._proxies)
        self._Huobi = Huobi(self._Huobi_exchange, self._Huobi_api_key,
                            self._Huobi_api_secret, self._Huobi_acct_id,
                            self._proxies)
        # logger
        self._logger = Logger()

    def __del__(self):
        self._conn.close()

    def initDB(self):
        self._logger.debug("src.core.db.db.DB.initDB")
        try:
            self._conn.close()
            os.chmod(self._dbStr, 0o664)  # 设置读写权限
            os.remove(self._dbStr)
            self._conn = sqlite3.connect(
                self._dbStr, timeout=self._dbTimeout, check_same_thread=False)
            self._conn.row_factory = dict_factory
            if self._dbSynchronous:
                self._conn.execute("PRAGMA synchronous = 0")
            os.chmod(self._dbStr, 0o664)  # 设置读写权限
        except (IOError, Exception) as err:
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
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def creatViews(self):
        self._logger.debug("src.core.db.db.DB.creatViews")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = CREATE_VIEWS_SQL.substitute(
                baseCoin=self._baseCoin,
                excludeCoins=self._excludeCoins,
                basePriceVolume=self._basePriceVolume,
                basePriceTimeout=self._basePriceTimeout,
                baseJudgeTimeout=self._baseJudgeTimeout,
                baseStatisticTimeout=self._baseStatisticTimeout).replace(
                    '[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.executescript(TEMP_SQL)
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewStatisticJudgeMarketTickerPairCurrentServer(self, server,
                                                      server_pair):
        self._logger.debug(
            "src.core.db.db.DB.getViewStatisticJudgeMarketTickerPairCurrentServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT_SERVER_SQL.substitute(
                server=server, server_pair=server_pair)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewStatisticJudgeMarketTickerPairCurrent(self):
        self._logger.debug(
            "src.core.db.db.DB.getViewStatisticJudgeMarketTickerPairCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewStatisticJudgeMarketTickerTraCurrentServer(self, exchange):
        self._logger.debug(
            "src.core.db.db.DB.getViewStatisticJudgeMarketTickerTraCurrentServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT_SERVER_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewStatisticJudgeMarketTickerTraCurrent(self):
        self._logger.debug(
            "src.core.db.db.DB.getViewStatisticJudgeMarketTickerTraCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewStatisticJudgeMarketTickerDisCurrentServer(self, server,
                                                     server_pair):
        self._logger.debug(
            "src.core.db.db.DB.getViewStatisticJudgeMarketTickerDisCurrentServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT_SERVER_SQL.substitute(
                server=server, server_pair=server_pair)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewStatisticJudgeMarketTickerDisCurrent(self):
        self._logger.debug(
            "src.core.db.db.DB.getViewStatisticJudgeMarketTickerDisCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewJudgeMarketTickerPairCurrentServer(self, server, server_pair):
        self._logger.debug(
            "src.core.db.db.DB.getViewJudgeMarketTickerPairCurrentServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT_SERVER_SQL.substitute(
                server=server, server_pair=server_pair)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewJudgeMarketTickerPairCurrent(self):
        self._logger.debug(
            "src.core.db.db.DB.getViewJudgeMarketTickerPairCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewJudgeMarketTickerTraCurrentServer(self, exchange):
        self._logger.debug(
            "src.core.db.db.DB.getViewJudgeMarketTickerTraCurrentServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT_SERVER_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewJudgeMarketTickerTraCurrent(self):
        self._logger.debug(
            "src.core.db.db.DB.getViewJudgeMarketTickerTraCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewJudgeMarketTickerDisCurrentServer(self, server, server_pair):
        self._logger.debug(
            "src.core.db.db.DB.getViewJudgeMarketTickerDisCurrentServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT_SERVER_SQL.substitute(
                server=server, server_pair=server_pair)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewJudgeMarketTickerDisCurrent(self):
        self._logger.debug(
            "src.core.db.db.DB.getViewJudgeMarketTickerDisCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrentPairServer(self, server, server_pair):
        self._logger.debug(
            "src.core.db.db.DB.getViewMarketTickerCurrentPairServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_PAIR_SERVER_SQL.substitute(
                server=server, server_pair=server_pair)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrentPair(self):
        self._logger.debug("src.core.db.db.DB.getViewMarketTickerCurrentPair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_PAIR_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrentTraServer(self, exchange):
        self._logger.debug(
            "src.core.db.db.DB.getViewMarketTickerCurrentTraServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_TRA_SERVER_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrentTra(self):
        self._logger.debug("src.core.db.db.DB.getViewMarketTickerCurrentTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_TRA_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrentDisServer(self, server, server_pair):
        self._logger.debug(
            "src.core.db.db.DB.getViewMarketTickerCurrentDisServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_DIS_SERVER_SQL.substitute(
                server=server, server_pair=server_pair)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrentDis(self):
        self._logger.debug("src.core.db.db.DB.getViewMarketTickerCurrentDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_DIS_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketTickerCurrent(self):
        self._logger.debug("src.core.db.db.DB.getViewMarketTickerCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_TICKER_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketKlineCurrent(self):
        self._logger.debug("src.core.db.db.DB.getViewMarketKlineCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_KLINE_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketSymbolPairsAggDepth(self, exchange, fSymbol, tSymbol):
        self._logger.debug("src.core.db.db.DB.getViewMarketSymbolPairs")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_SYMBOL_SERVER_AGGDEPTH_SQL.substitute(
                server=exchange, fSymbol=fSymbol, tSymbol=tSymbol).replace(
                    '[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewMarketSymbolPairs(self, exchange):
        self._logger.debug("src.core.db.db.DB.getViewMarketSymbolPairs")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_MARKET_SYMBOL_SERVER_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewInfoSymbolPairs(self, exchange):
        self._logger.debug("src.core.db.db.DB.getViewInfoSymbolPairs")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_INFO_SYMBOL_SERVER_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewAccountBalanceCurrent(self):
        self._logger.debug("src.core.db.db.DB.getViewAccountBalanceCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_ACCOUNT_BALANCE_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getViewAccountWithdrawCurrent(self):
        self._logger.debug("src.core.db.db.DB.getViewAccountWithdrawCurrent")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_VIEW_ACCOUNT_WITHDRAW_CURRENT_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getTables(self):
        self._logger.debug("src.core.db.db.DB.getTables")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_TABLES_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def creatTables(self):
        self._logger.debug("src.core.db.db.DB.creatTables")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = CREATE_TABELS_SQL
            self._logger.debug(TEMP_SQL)
            curs.executescript(TEMP_SQL)
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getAccountBalanceHistory(self):
        self._logger.debug("src.core.db.db.DB.getAccountBalanceHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_ACCOUNT_BALANCE_HISTORY_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getAccountWithdrawHistory(self):
        self._logger.debug("src.core.db.db.DB.getAccountWithdrawHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_ACCOUNT_WITHDRAW_HISTORY_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getInfoServer(self):
        self._logger.debug("src.core.db.db.DB.getInfoServer")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_INFO_SERVER_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getInfoSymbol(self, exchange):
        self._logger.debug("src.core.db.db.DB.getInfoSymbol")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_INFO_SYMBOL_SQL.substitute(server=exchange).replace(
                '[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getInfoWithdraw(self, exchange):
        self._logger.debug("src.core.db.db.DB.getInfoWithdraw")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_INFO_WITHDRAW_SQL.substitute(
                server=exchange).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getMarketDepth(self):
        self._logger.debug("src.core.db.db.DB.getMarketDepth")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_MARKET_DEPTH_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delMarketDepth(self):
        self._logger.debug("src.core.db.db.DB.delMarketDepth")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_MARKET_DEPTH_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getMarketKline(self):
        self._logger.debug("src.core.db.db.DB.getMarketKline")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_MARKET_KLINE_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delMarketKline(self):
        self._logger.debug("src.core.db.db.DB.delMarketKline")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_MARKET_KLINE_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getMarketTicker(self):
        self._logger.debug("src.core.db.db.DB.getMarketTicker")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_MARKET_TICKER_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delMarketTicker(self):
        self._logger.debug("src.core.db.db.DB.delMarketTicker")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_MARKET_TICKER_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getStatisticTradeOrderHistory(self):
        self._logger.debug("src.core.db.db.DB.getStatisticTradeOrderHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_STATISTIC_TRADE_ORDER_HISTORY_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delStatisticTradeOrderHistory(self):
        self._logger.debug("src.core.db.db.DB.delStatisticTradeOrderHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_STATISTIC_TRADE_ORDER_HISTORY_SQL.substitute(
                period=self._statisticSignalTradeCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getStatisticTradeBacktestHistory(self):
        self._logger.debug("src.core.db.db.DB.getStatisticTradeBacktestHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_STATISTIC_TRADE_BACKTEST_HISTORY_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delStatisticTradeBacktestHistory(self):
        self._logger.debug("src.core.db.db.DB.delStatisticTradeBacktestHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_STATISTIC_TRADE_BACKTEST_HISTORY_SQL.substitute(
                period=self._statisticSignalTradeCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getStatisticJudgeMarketTickerDis(self):
        self._logger.debug("src.core.db.db.DB.getStatisticJudgeMarketTickerDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_STATISTIC_JUDGE_MARKET_TICKER_DIS_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delStatisticJudgeMarketTickerDis(self):
        self._logger.debug("src.core.db.db.DB.delStatisticJudgeMarketTickerDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_STATISTIC_JUDGE_MARKET_TICKER_DIS_SQL.substitute(
                period=self._statisticJudgeMarketTickerCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getStatisticJudgeMarketTickerTra(self):
        self._logger.debug("src.core.db.db.DB.getStatisticJudgeMarketTickerTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_STATISTIC_JUDGE_MARKET_TICKER_TRA_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delStatisticJudgeMarketTickerTra(self):
        self._logger.debug("src.core.db.db.DB.delStatisticJudgeMarketTickerTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_STATISTIC_JUDGE_MARKET_TICKER_TRA_SQL.substitute(
                period=self._statisticJudgeMarketTickerCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getStatisticJudgeMarketTickerPair(self):
        self._logger.debug("src.core.db.db.DB.getStatisticJudgeMarketTickerPair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_STATISTIC_JUDGE_MARKET_TICKER_PAIR_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delStatisticJudgeMarketTickerPair(self):
        self._logger.debug("src.core.db.db.DB.delStatisticJudgeMarketTickerPair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_STATISTIC_JUDGE_MARKET_TICKER_PAIR_SQL.substitute(
                period=self._statisticJudgeMarketTickerCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getJudgeMarketTickerDis(self):
        self._logger.debug("src.core.db.db.DB.getJudgeMarketTickerDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_JUDGE_MARKET_TICKER_DIS_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delJudgeMarketTickerDis(self):
        self._logger.debug("src.core.db.db.DB.delJudgeMarketTickerDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_JUDGE_MARKET_TICKER_DIS_SQL.substitute(
                period=self._judgeMarketTickerCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getJudgeMarketTickerTra(self):
        self._logger.debug("src.core.db.db.DB.getJudgeMarketTickerTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_JUDGE_MARKET_TICKER_TRA_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delJudgeMarketTickerTra(self):
        self._logger.debug("src.core.db.db.DB.delJudgeMarketTickerTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_JUDGE_MARKET_TICKER_TRA_SQL.substitute(
                period=self._judgeMarketTickerCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getJudgeMarketTickerPair(self):
        self._logger.debug("src.core.db.db.DB.getJudgeMarketTickerPair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_JUDGE_MARKET_TICKER_PAIR_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delJudgeMarketTickerPair(self):
        self._logger.debug("src.core.db.db.DB.delJudgeMarketTickerPair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_JUDGE_MARKET_TICKER_PAIR_SQL.substitute(
                period=self._judgeMarketTickerCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getSignalTradeDis(self, signal_id):
        self._logger.debug("src.core.db.db.DB.getSignalTradeDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_SIGNAL_TRADE_DIS_SQL.substitute(
                signal_id= signal_id)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delSignalTradeDis(self):
        self._logger.debug("src.core.db.db.DB.delSignalTradeDis")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_SIGNAL_TRADE_DIS_SQL.substitute(
                period=self._signalTradeCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getSignalTradeTra(self, signal_id):
        self._logger.debug("src.core.db.db.DB.getSignalTradeTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_SIGNAL_TRADE_TRA_SQL.substitute(
                signal_id= signal_id)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delSignalTradeTra(self):
        self._logger.debug("src.core.db.db.DB.delSignalTradeTra")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_SIGNAL_TRADE_TRA_SQL.substitute(
                period=self._signalTradeCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getSignalTradePair(self, signal_id):
        self._logger.debug("src.core.db.db.DB.getSignalTradePair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_SIGNAL_TRADE_PAIR_SQL.substitute(
                signal_id= signal_id)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delSignalTradePair(self):
        self._logger.debug("src.core.db.db.DB.delSignalTradePair")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_SIGNAL_TRADE_PAIR_SQL.substitute(
                period=self._signalTradeCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getTradeBacktestHistory(self):
        self._logger.debug("src.core.db.db.DB.getTradeBacktestHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_TRADE_BACKTEST_HISTORY_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delTradeBacktestHistory(self):
        self._logger.debug("src.core.db.db.DB.delTradeBacktestHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_TRADE_BACKTEST_HISTORY_SQL.substitute(
                period=self._tradeHistoryCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getTradeOrderHistory(self):
        self._logger.debug("src.core.db.db.DB.getTradeOrderHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_TRADE_ORDER_HISTORY_SQL
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def delTradeOrderHistory(self):
        self._logger.debug("src.core.db.db.DB.delTradeOrderHistory")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = DEL_TRADE_ORDER_HISTORY_SQL.substitute(
                period=self._tradeHistoryCycle)
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            self._conn.commit()
            curs.close()
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getTradeBacktestHistoryServerOrder(self, exchange, orderIDs):
        self._logger.debug("src.core.db.db.DB.getTradeBacktestHistoryServerOrder")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_TRADE_BACKTEST_HISTORY_SERVER_ORDER_SQL.substitute(
                server=exchange,
                order_id=orderIDs).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def getTradeOrderHistoryServerOrder(self, exchange, orderIDs):
        self._logger.debug("src.core.db.db.DB.getTradeOrderHistoryServerOrder")
        try:
            curs = self._conn.cursor()
            TEMP_SQL = GET_TRADE_ORDER_HISTORY_SERVER_ORDER_SQL.substitute(
                server=exchange,
                order_id=orderIDs).replace('[', '(').replace(']', ')')
            self._logger.debug(TEMP_SQL)
            curs.execute(TEMP_SQL)
            res = curs.fetchall()
            curs.close()
            return res
        except (sqlite3.Error, Exception) as err:
            raise DBException(err)

    def insertAccountBalanceHistory(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertAccountBalanceHistory: { exchange=%s }" %
            exchange)
        try:
            timeStamp = utcnow_timestamp()
            TEMP_SQL_TITLE = INSERT_ACCOUNT_BALANCE_HISTORY_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        TEMP_SQL_VALUE.append((str(self._Okex_exchange),
                                               int(timeStamp), str(b["asset"]),
                                               float(b["balance"]),
                                               float(b["free"]),
                                               float(b["locked"])))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        TEMP_SQL_VALUE.append((str(self._Binance_exchange),
                                               int(timeStamp), str(b["asset"]),
                                               float(b["balance"]),
                                               float(b["free"]),
                                               float(b["locked"])))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getAccountBalances()
                for b in base:
                    if b["balance"] > 0:
                        TEMP_SQL_VALUE.append((str(self._Huobi_exchange),
                                               int(timeStamp), str(b["asset"]),
                                               float(b["balance"]),
                                               float(b["free"]),
                                               float(b["locked"])))
            # Others
            # if exchange == "all" or "Others" in exchange:
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertAccountWithdrawHistory(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertAccountWithdrawHistory: { exchange=%s }" %
            exchange)
        try:
            timeStamp = utcnow_timestamp()
            TEMP_SQL_TITLE = INSERT_ACCOUNT_WITHDRAW_HISTORY_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                res = self._Okex.getAccountDetail()
                for base in res:
                    TEMP_SQL_VALUE.append(
                        (str(self._Okex_exchange), int(timeStamp),
                         str(base["asset"]),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["deposit"]))),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["withdraw"])))))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                res = self._Binance.getAccountDetail()
                for base in res:
                    TEMP_SQL_VALUE.append(
                        (str(self._Binance_exchange), int(timeStamp),
                         str(base["asset"]),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["deposit"]))),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["withdraw"])))))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                res = self._Huobi.getAccountDetail()
                for base in res:
                    TEMP_SQL_VALUE.append(
                        (str(self._Huobi_exchange), int(timeStamp),
                         str(base["asset"]),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["deposit"]))),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["withdraw"])))))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertAccountWithdrawHistoryAsset(self, exchange, asset):
        self._logger.debug(
            "src.core.db.db.DB.insertAccountWithdrawHistoryAsset: { exchange=%s, asset=%s }"
            % (exchange, asset))
        try:
            timeStamp = utcnow_timestamp()
            TEMP_SQL_TITLE = INSERT_ACCOUNT_WITHDRAW_HISTORY_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getAccountAssetDetail(asset)
                if not base == {}:
                    TEMP_SQL_VALUE.append(
                        (str(self._Okex_exchange), int(timeStamp), str(asset),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["deposit"]))),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["withdraw"])))))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getAccountAssetDetail(asset)
                if not base == {}:
                    TEMP_SQL_VALUE.append(
                        (str(self._Binance_exchange), int(timeStamp),
                         str(asset),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["deposit"]))),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["withdraw"])))))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getAccountAssetDetail(asset)
                if not base == {}:
                    TEMP_SQL_VALUE.append(
                        (str(self._Huobi_exchange), int(timeStamp), str(asset),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["deposit"]))),
                         str(
                             sqlite_escape(','.join(
                                 json.dumps(b) for b in base["withdraw"])))))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertInfoServer(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertInfoServer: { exchange=%s }" % exchange)
        try:
            TEMP_SQL_TITLE = INSERT_INFO_SERVER_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                res = self._Okex.getServerLimits()
                TEMP_SQL_VALUE.append(
                    (str(self._Okex_exchange), "NULL" if
                     res["info_second"] == '' else float(res["info_second"]),
                     "NULL" if res["market_second"] == '' else float(
                         res["market_second"]),
                     "NULL" if res["orders_second"] == '' else float(
                         res["orders_second"]),
                     "NULL" if res["webSockets_second"] == '' else float(
                         res["webSockets_second"])))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                res = self._Binance.getServerLimits()
                TEMP_SQL_VALUE.append(
                    (str(self._Binance_exchange), "NULL" if
                     res["info_second"] == '' else float(res["info_second"]),
                     "NULL" if res["market_second"] == '' else float(
                         res["market_second"]),
                     "NULL" if res["orders_second"] == '' else float(
                         res["orders_second"]),
                     "NULL" if res["webSockets_second"] == '' else float(
                         res["webSockets_second"])))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                res = self._Huobi.getServerLimits()
                TEMP_SQL_VALUE.append(
                    (str(self._Huobi_exchange), "NULL" if
                     res["info_second"] == '' else float(res["info_second"]),
                     "NULL" if res["market_second"] == '' else float(
                         res["market_second"]),
                     "NULL" if res["orders_second"] == '' else float(
                         res["orders_second"]),
                     "NULL" if res["webSockets_second"] == '' else float(
                         res["webSockets_second"])))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertInfoSymbol(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertInfoSymbol: { exchange=%s }" % exchange)
        try:
            TEMP_SQL_TITLE = INSERT_INFO_SYMBOL_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getSymbolsLimits()
                fees = self._Okex.getTradeFees()
                for b in base:
                    fees_key = fees[0]
                    TEMP_SQL_VALUE.append(
                        (str(self._Okex_exchange), str(b["fSymbol"]),
                         str(b["tSymbol"]),
                         "NULL" if b["tSymbol_price"]["precision"] == '' else
                         float(b["tSymbol_price"]["precision"]),
                         "NULL" if b["tSymbol_price"]["max"] == '' else float(
                             b["tSymbol_price"]["max"]),
                         "NULL" if b["tSymbol_price"]["min"] == '' else float(
                             b["tSymbol_price"]["min"]),
                         "NULL" if b["tSymbol_price"]["step"] == '' else float(
                             b["tSymbol_price"]["step"]),
                         "NULL" if b["fSymbol_size"]["precision"] == '' else
                         float(b["fSymbol_size"]["precision"]),
                         "NULL" if b["fSymbol_size"]["max"] == '' else float(
                             b["fSymbol_size"]["max"]),
                         "NULL" if b["fSymbol_size"]["min"] == '' else float(
                             b["fSymbol_size"]["min"]),
                         "NULL" if b["fSymbol_size"]["step"] == '' else float(
                             b["fSymbol_size"]["step"]), "NULL" if
                         b["min_notional"] == '' else float(b["min_notional"]),
                         "NULL" if fees_key["maker"] == '' else float(
                             fees_key["maker"]),
                         "NULL" if fees_key["taker"] == '' else float(
                             fees_key["taker"])))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getSymbolsLimits()
                fees = self._Binance.getTradeFees()
                for b in base:
                    fees_key = ''
                    for f in fees:
                        if f["symbol"] == b["fSymbol"] + b["tSymbol"]:
                            fees_key = f
                            TEMP_SQL_VALUE.append(
                                (str(self._Binance_exchange), str(
                                    b["fSymbol"]), str(b["tSymbol"]), "NULL"
                                 if b["tSymbol_price"]["precision"] == '' else
                                 float(b["tSymbol_price"]["precision"]),
                                 "NULL" if b["tSymbol_price"]["max"] == '' else
                                 float(b["tSymbol_price"]["max"]),
                                 "NULL" if b["tSymbol_price"]["min"] == '' else
                                 float(b["tSymbol_price"]["min"]),
                                 "NULL" if b["tSymbol_price"]["step"] == ''
                                 else float(b["tSymbol_price"]["step"]),
                                 "NULL" if b["fSymbol_size"]["precision"] == ''
                                 else float(b["fSymbol_size"]["precision"]),
                                 "NULL" if b["fSymbol_size"]["max"] == '' else
                                 float(b["fSymbol_size"]["max"]),
                                 "NULL" if b["fSymbol_size"]["min"] == '' else
                                 float(b["fSymbol_size"]["min"]),
                                 "NULL" if b["fSymbol_size"]["step"] == '' else
                                 float(b["fSymbol_size"]["step"]),
                                 "NULL" if b["min_notional"] == '' else float(
                                     b["min_notional"]),
                                 "NULL" if fees_key["maker"] == '' else float(
                                     fees_key["maker"]),
                                 "NULL" if fees_key["taker"] == '' else float(
                                     fees_key["taker"])))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getSymbolsLimits()
                fees = self._Huobi.getTradeFees()
                for b in base:
                    fees_key = fees[0]
                    TEMP_SQL_VALUE.append(
                        (str(self._Huobi_exchange), str(b["fSymbol"]),
                         str(b["tSymbol"]),
                         "NULL" if b["tSymbol_price"]["precision"] == '' else
                         float(b["tSymbol_price"]["precision"]),
                         "NULL" if b["tSymbol_price"]["max"] == '' else float(
                             b["tSymbol_price"]["max"]),
                         "NULL" if b["tSymbol_price"]["min"] == '' else float(
                             b["tSymbol_price"]["min"]),
                         "NULL" if b["tSymbol_price"]["step"] == '' else float(
                             b["tSymbol_price"]["step"]),
                         "NULL" if b["fSymbol_size"]["precision"] == '' else
                         float(b["fSymbol_size"]["precision"]),
                         "NULL" if b["fSymbol_size"]["max"] == '' else float(
                             b["fSymbol_size"]["max"]),
                         "NULL" if b["fSymbol_size"]["min"] == '' else float(
                             b["fSymbol_size"]["min"]),
                         "NULL" if b["fSymbol_size"]["step"] == '' else float(
                             b["fSymbol_size"]["step"]), "NULL" if
                         b["min_notional"] == '' else float(b["min_notional"]),
                         "NULL" if fees_key["maker"] == '' else float(
                             fees_key["maker"]),
                         "NULL" if fees_key["taker"] == '' else float(
                             fees_key["taker"])))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertInfoWithdraw(self, exchange="all"):
        self._logger.debug(
            "src.core.db.db.DB.insertInfoWithdraw: { exchange=%s}" % exchange)
        try:
            TEMP_SQL_TITLE = INSERT_INFO_WITHDRAW_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getAccountLimits()
                for b in base:
                    TEMP_SQL_VALUE.append(
                        (str(self._Okex_exchange), str(b["asset"]), "NULL"
                         if b["can_deposit"] == '' else str(b["can_deposit"]),
                         "NULL" if b["can_withdraw"] == '' else str(
                             b["can_withdraw"]),
                         "NULL" if b["min_withdraw"] == '' else float(
                             b["min_withdraw"])))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getAccountLimits()
                for b in base:
                    TEMP_SQL_VALUE.append(
                        (str(self._Binance_exchange), str(b["asset"]), "NULL"
                         if b["can_deposit"] == '' else str(b["can_deposit"]),
                         "NULL" if b["can_withdraw"] == '' else str(
                             b["can_withdraw"]),
                         "NULL" if b["min_withdraw"] == '' else float(
                             b["min_withdraw"])))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getAccountLimits()
                for b in base:
                    TEMP_SQL_VALUE.append(
                        (str(self._Huobi_exchange), str(b["asset"]), "NULL"
                         if b["can_deposit"] == '' else str(b["can_deposit"]),
                         "NULL" if b["can_withdraw"] == '' else str(
                             b["can_withdraw"]),
                         "NULL" if b["min_withdraw"] == '' else float(
                             b["min_withdraw"])))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertMarketDepth(self, exchange, fSymbol, tSymbol, limit=100):
        self._logger.debug(
            "src.core.db.db.DB.insertMarketDepth: { exchange=%s, fSymbol=%s, tSymbol=%s, limit=%s }"
            % (exchange, fSymbol, tSymbol, limit))
        try:
            TEMP_SQL_TITLE = INSERT_MARKET_DEPTH_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getMarketOrderbookDepth(
                    fSymbol, tSymbol, limit)
                TEMP_SQL_VALUE.append(
                    (str(self._Okex_exchange), int(base["timeStamp"]),
                     str(base["fSymbol"]), str(base["tSymbol"]),
                     str(sqlite_escape(json.dumps(base["bid_price_size"]))),
                     str(sqlite_escape(json.dumps(base["ask_price_size"])))))
            # Binnance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getMarketOrderbookDepth(
                    fSymbol, tSymbol, limit)
                TEMP_SQL_VALUE.append(
                    (str(self._Binance_exchange), int(base["timeStamp"]),
                     str(base["fSymbol"]), str(base["tSymbol"]),
                     str(sqlite_escape(json.dumps(base["bid_price_size"]))),
                     str(sqlite_escape(json.dumps(base["ask_price_size"])))))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getMarketOrderbookDepth(
                    fSymbol, tSymbol, limit)
                TEMP_SQL_VALUE.append(
                    (str(self._Huobi_exchange), int(base["timeStamp"]),
                     str(base["fSymbol"]), str(base["tSymbol"]),
                     str(sqlite_escape(json.dumps(base["bid_price_size"]))),
                     str(sqlite_escape(json.dumps(base["ask_price_size"])))))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertMarketKline(self, exchange, fSymbol, tSymbol, interval, start,
                          end):
        self._logger.debug(
            "src.core.db.db.DB.insertMarketKline: { exchange=%s, fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s }"
            % (exchange, fSymbol, tSymbol, interval, start, end))
        try:
            TEMP_SQL_TITLE = INSERT_MARKET_KLINE_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getMarketKline(fSymbol, tSymbol, interval,
                                                 start, end)
                for b in base:
                    TEMP_SQL_VALUE.append(
                        (str(self._Okex_exchange), int(b["timeStamp"]),
                         str(b["fSymbol"]), str(b["tSymbol"]),
                         float(b["open"]), float(b["high"]), float(b["low"]),
                         float(b["close"]), float(b["volume"])))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getMarketKline(fSymbol, tSymbol, interval,
                                                    start, end)
                for b in base:
                    TEMP_SQL_VALUE.append(
                        (str(self._Binance_exchange), int(b["timeStamp"]),
                         str(b["fSymbol"]), str(b["tSymbol"]),
                         float(b["open"]), float(b["high"]), float(b["low"]),
                         float(b["close"]), float(b["volume"])))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getMarketKline(fSymbol, tSymbol, interval,
                                                  start, end)
                for b in base:
                    TEMP_SQL_VALUE.append(
                        (str(self._Huobi_exchange), int(b["timeStamp"]),
                         str(b["fSymbol"]), str(b["tSymbol"]),
                         float(b["open"]), float(b["high"]), float(b["low"]),
                         float(b["close"]), float(b["volume"])))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertMarketTicker(self, exchange, fSymbol, tSymbol, aggDepth=0):
        self._logger.debug(
            "src.core.db.db.DB.insertMarketTicker: { exchange=%s, fSymbol=%s, tSymbol=%s aggDepth=%s}"
            % (exchange, fSymbol, tSymbol, aggDepth))
        try:
            TEMP_SQL_TITLE = INSERT_MARKET_TICKER_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
                TEMP_SQL_VALUE.append((str(self._Okex_exchange),
                                       int(base["timeStamp"]),
                                       str(base["fSymbol"]),
                                       str(base["tSymbol"]),
                                       float(base["bid_one_price"]),
                                       float(base["bid_one_size"]),
                                       float(base["ask_one_price"]),
                                       float(base["ask_one_size"])))
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
                TEMP_SQL_VALUE.append((str(self._Binance_exchange),
                                       int(base["timeStamp"]),
                                       str(base["fSymbol"]),
                                       str(base["tSymbol"]),
                                       float(base["bid_one_price"]),
                                       float(base["bid_one_size"]),
                                       float(base["ask_one_price"]),
                                       float(base["ask_one_size"])))
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.getMarketOrderbookTicker(
                    fSymbol, tSymbol, aggDepth)
                TEMP_SQL_VALUE.append((str(self._Huobi_exchange),
                                       int(base["timeStamp"]),
                                       str(base["fSymbol"]),
                                       str(base["tSymbol"]),
                                       float(base["bid_one_price"]),
                                       float(base["bid_one_size"]),
                                       float(base["ask_one_price"]),
                                       float(base["ask_one_size"])))
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertJudgeMarketTickerDis(self, signal):
        self._logger.debug(
            "src.core.db.db.DB.insertJudgeMarketTickerDis: {signal=%s}" %
            signal)
        try:
            TEMP_SQL_TITLE = INSERT_JUDGE_MARKET_TICKER_DIS_SQL
            TEMP_SQL_VALUE = []
            for s in signal:
                TEMP_SQL_VALUE.append(
                    (int(s['timeStamp']), str(s['bid_server']),
                     str(s['ask_server']), str(s['fSymbol']),
                     str(s['tSymbol']), float(s['bid_price']),
                     float(s['bid_size']), float(s['bid_price_base']),
                     float(s['ask_price']), float(s['ask_size']),
                     float(s['ask_price_base']), float(s['bid_fee']),
                     float(s['ask_fee']), float(s['gain_base']),
                     float(s['gain_ratio'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertJudgeMarketTickerTra(self, signal):
        self._logger.debug(
            "src.core.db.db.DB.insertJudgeMarketTickerTra: {signal=%s}" %
            signal)
        try:
            TEMP_SQL_TITLE = INSERT_JUDGE_MARKET_TICKER_TRA_SQL
            TEMP_SQL_VALUE = []
            for s in signal:
                TEMP_SQL_VALUE.append((int(s['timeStamp']), str(s['server']),
                                       str(s['V1_fSymbol']),
                                       str(s['V1_tSymbol']),
                                       str(s['V2_fSymbol']),
                                       str(s['V2_tSymbol']),
                                       str(s['V3_fSymbol']),
                                       str(s['V3_tSymbol']),
                                       float(s['V1_bid_one_price']),
                                       float(s['V1_bid_one_size']),
                                       float(s['V1_bid_one_price_base']),
                                       float(s['V1_ask_one_price']),
                                       float(s['V1_ask_one_size']),
                                       float(s['V1_ask_one_price_base']),
                                       float(s['V2_bid_one_price']),
                                       float(s['V2_bid_one_size']),
                                       float(s['V2_bid_one_price_base']),
                                       float(s['V2_ask_one_price']),
                                       float(s['V2_ask_one_size']),
                                       float(s['V2_ask_one_price_base']),
                                       float(s['V3_bid_one_price']),
                                       float(s['V3_bid_one_size']),
                                       float(s['V3_bid_one_price_base']),
                                       float(s['V3_ask_one_price']),
                                       float(s['V3_ask_one_size']),
                                       float(s['V3_ask_one_price_base']),
                                       float(s['V1_fee']), float(s['V2_fee']),
                                       float(s['V3_fee']),
                                       float(s['V1_one_price']),
                                       str(s['V1_one_side']),
                                       float(s['V1_one_size']),
                                       float(s['V2_one_price']),
                                       str(s['V2_one_side']),
                                       float(s['V2_one_size']),
                                       float(s['V3_one_price']),
                                       str(s['V3_one_side']),
                                       float(s['V3_one_size']),
                                       float(s['gain_base']),
                                       float(s['gain_ratio'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertJudgeMarketTickerPair(self, signal):
        self._logger.debug(
            "src.core.db.db.DB.insertJudgeMarketTickerPair: {signal=%s}" %
            signal)
        try:
            TEMP_SQL_TITLE = INSERT_JUDGE_MARKET_TICKER_PAIR_SQL
            TEMP_SQL_VALUE = []
            for s in signal:
                TEMP_SQL_VALUE.append((int(s['timeStamp']), str(
                    s['J1_server']), str(s['J2_server']), str(s['V1_fSymbol']),
                                       str(s['V1_tSymbol']),
                                       str(s['V2_fSymbol']),
                                       str(s['V2_tSymbol']),
                                       str(s['V3_fSymbol']),
                                       str(s['V3_tSymbol']),
                                       float(s['J1_V1_bid_one_price']),
                                       float(s['J1_V1_bid_one_size']),
                                       float(s['J1_V1_bid_one_price_base']),
                                       float(s['J1_V1_ask_one_price']),
                                       float(s['J1_V1_ask_one_size']),
                                       float(s['J1_V1_ask_one_price_base']),
                                       float(s['J1_V2_bid_one_price']),
                                       float(s['J1_V2_bid_one_size']),
                                       float(s['J1_V2_bid_one_price_base']),
                                       float(s['J1_V2_ask_one_price']),
                                       float(s['J1_V2_ask_one_size']),
                                       float(s['J1_V2_ask_one_price_base']),
                                       float(s['J1_V3_bid_one_price']),
                                       float(s['J1_V3_bid_one_size']),
                                       float(s['J1_V3_bid_one_price_base']),
                                       float(s['J1_V3_ask_one_price']),
                                       float(s['J1_V3_ask_one_size']),
                                       float(s['J1_V3_ask_one_price_base']),
                                       float(s['J2_V1_bid_one_price']),
                                       float(s['J2_V1_bid_one_size']),
                                       float(s['J2_V1_bid_one_price_base']),
                                       float(s['J2_V1_ask_one_price']),
                                       float(s['J2_V1_ask_one_size']),
                                       float(s['J2_V1_ask_one_price_base']),
                                       float(s['J2_V2_bid_one_price']),
                                       float(s['J2_V2_bid_one_size']),
                                       float(s['J2_V2_bid_one_price_base']),
                                       float(s['J2_V2_ask_one_price']),
                                       float(s['J2_V2_ask_one_size']),
                                       float(s['J2_V2_ask_one_price_base']),
                                       float(s['J2_V3_bid_one_price']),
                                       float(s['J2_V3_bid_one_size']),
                                       float(s['J2_V3_bid_one_price_base']),
                                       float(s['J2_V3_ask_one_price']),
                                       float(s['J2_V3_ask_one_size']),
                                       float(s['J2_V3_ask_one_price_base']),
                                       float(s['J1_V1_fee']),
                                       float(s['J1_V2_fee']),
                                       float(s['J1_V3_fee']),
                                       float(s['J2_V1_fee']),
                                       float(s['J2_V2_fee']),
                                       float(s['J2_V3_fee']),
                                       float(s['J1_V1_one_price']),
                                       str(s['J1_V1_one_side']),
                                       float(s['J1_V1_one_size']),
                                       float(s['J2_V1_one_price']),
                                       str(s['J2_V1_one_side']),
                                       float(s['J2_V1_one_size']),
                                       float(s['J1_V2_one_price']),
                                       str(s['J1_V2_one_side']),
                                       float(s['J1_V2_one_size']),
                                       float(s['J2_V2_one_price']),
                                       str(s['J2_V2_one_side']),
                                       float(s['J2_V2_one_size']),
                                       float(s['J1_V3_one_price']),
                                       str(s['J1_V3_one_side']),
                                       float(s['J1_V3_one_size']),
                                       float(s['J2_V3_one_price']),
                                       str(s['J2_V3_one_side']),
                                       float(s['J2_V3_one_size']),
                                       float(s['gain_base']),
                                       float(s['gain_ratio'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertCreatTradeBacktestHistory(self,
                                   exchange,
                                   fSymbol,
                                   tSymbol,
                                   ask_or_bid,
                                   price,
                                   quantity,
                                   ratio='',
                                   type=CCAT_ORDER_TYPE_LIMIT,
                                   group_id='NULL',
                                   identify=0):
        self._logger.debug(
            "src.core.db.db.DB.insertCreatTradeBacktestHistory: { exchange=%s, fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, ratio=%s, type=%s, group_id=%s, identify=%s}"
            % (exchange, fSymbol, tSymbol, ask_or_bid, price, ratio, type,
               group_id, identify))
        try:
            result = []
            TEMP_SQL_TITLE = INSERT_TRADE_BACKTEST_HISTORY_SQL
            TEMP_SQL_VALUE = []
            pid = os.getpid()
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                timeStamp = utcnow_timestamp()
                id_str = 'Okex' + str(pid) + str(timeStamp) + str(identify)
                order_id = '0x1a-' + str(uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
                status = 'filled'
                if ratio == '':
                    ratio = self._Okex.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                TEMP_SQL_VALUE.append(
                    (str(self._Okex_exchange), int(timeStamp), str(order_id),
                     str(status), str(type), str(fSymbol), str(tSymbol),
                     str(ask_or_bid), float(price), float(quantity),
                     float(price), float(quantity), float(fee), str(group_id)))
                result.append({"server":str(self._Okex_exchange), "order_id":str(order_id), "status": str(status)})
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                timeStamp = utcnow_timestamp()
                id_str = 'Binance' + str(pid) + str(timeStamp) + str(identify)
                order_id = '0x2a-' + str(uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
                status = 'filled'
                if ratio == '':
                    ratio = self._Binance.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                TEMP_SQL_VALUE.append((str(self._Binance_exchange),
                                       int(timeStamp), str(order_id),
                                       str(status), str(type), str(fSymbol),
                                       str(tSymbol), str(ask_or_bid),
                                       float(price), float(quantity),
                                       float(price), float(quantity),
                                       float(fee), str(group_id)))
                result.append({"server":str(self._Binance_exchange), "order_id":str(order_id), "status": str(status)})
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                timeStamp = utcnow_timestamp()
                id_str = 'Huobi' + str(pid) + str(timeStamp) + str(identify)
                order_id = '0x3a-' + str(uuid.uuid3(uuid.NAMESPACE_DNS, id_str))
                status = 'filled'
                if ratio == '':
                    ratio = self._Huobi.getTradeFees()[0]["taker"]
                fee = float(ratio) * float(price) * float(quantity)
                TEMP_SQL_VALUE.append(
                    (str(self._Huobi_exchange), int(timeStamp), str(order_id),
                     str(status), str(type), str(fSymbol), str(tSymbol),
                     str(ask_or_bid), float(price), float(quantity),
                     float(price), float(quantity), float(fee), str(group_id)))
                result.append({"server":str(self._Huobi_exchange), "order_id":str(order_id), "status": str(status)})
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
            # return
            return result
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertSyncTradeOrderHistory(self,
                                exchange,
                                fSymbol,
                                tSymbol,
                                limit='100',
                                ratio='',
                                group_id='NULL'):
        self._logger.debug(
            "src.core.db.db.DB.insertSyncTradeOrderHistory: { exchange=%s, fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s, group_id=%s }"
            % (exchange, fSymbol, tSymbol, limit, ratio, group_id))
        try:
            result = []
            TEMP_SQL_TITLE = INSERT_TRADE_ORDER_HISTORY_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                res = self._Okex.getTradeHistory(fSymbol, tSymbol, limit,
                                                 ratio)
                if not res == []:
                    for base in res:
                        TEMP_SQL_VALUE.append((str(self._Okex_exchange),
                                               int(base["timeStamp"]),
                                               str(base["order_id"]),
                                               str(base["status"]),
                                               str(base["type"]),
                                               str(base["fSymbol"]),
                                               str(base["tSymbol"]),
                                               str(base["ask_or_bid"]),
                                               float(base["ask_bid_price"]),
                                               float(base["ask_bid_size"]),
                                               float(base["filled_price"]),
                                               float(base["filled_size"]),
                                               float(base["fee"]),
                                               str(group_id)))
                        result.append({"server":str(self._Okex_exchange), "order_id":str(base["order_id"]), "status":str(base["status"])})
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                res = self._Binance.getTradeHistory(fSymbol, tSymbol, limit,
                                                    ratio)
                if not res == []:
                    for base in res:
                        TEMP_SQL_VALUE.append((str(self._Binance_exchange),
                                               int(base["timeStamp"]),
                                               str(base["order_id"]),
                                               str(base["status"]),
                                               str(base["type"]),
                                               str(base["fSymbol"]),
                                               str(base["tSymbol"]),
                                               str(base["ask_or_bid"]),
                                               float(base["ask_bid_price"]),
                                               float(base["ask_bid_size"]),
                                               float(base["filled_price"]),
                                               float(base["filled_size"]),
                                               float(base["fee"]),
                                               str(group_id)))
                        result.append({"server":str(self._Binance_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                res = self._Huobi.getTradeHistory(fSymbol, tSymbol, limit,
                                                  ratio)
                if not res == []:
                    for base in res:
                        TEMP_SQL_VALUE.append((str(self._Huobi_exchange),
                                               int(base["timeStamp"]),
                                               str(base["order_id"]),
                                               str(base["status"]),
                                               str(base["type"]),
                                               str(base["fSymbol"]),
                                               str(base["tSymbol"]),
                                               str(base["ask_or_bid"]),
                                               float(base["ask_bid_price"]),
                                               float(base["ask_bid_size"]),
                                               float(base["filled_price"]),
                                               float(base["filled_size"]),
                                               float(base["fee"]),
                                               str(group_id)))
                        result.append({"server":str(self._Huobi_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
            # return
            return result
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertCreatTradeOrderHistory(self,
                                     exchange,
                                     fSymbol,
                                     tSymbol,
                                     ask_or_bid,
                                     price,
                                     quantity,
                                     ratio='',
                                     type=CCAT_ORDER_TYPE_LIMIT,
                                     group_id='NULL'):
        self._logger.debug(
            "src.core.db.db.DB.insertCreatTradeOrderHistory: { exchange=%s, fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, ratio=%s, type=%s, group_id=%s }"
            % (exchange, fSymbol, tSymbol, ask_or_bid, price, ratio, type,
               group_id))
        try:
            result = []
            TEMP_SQL_TITLE = UPDATE_CREAT_TRADE_ORDER_HISTORY_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                base = self._Okex.createOrder(fSymbol, tSymbol, ask_or_bid,
                                              price, quantity, ratio, type)
                TEMP_SQL_VALUE.append((str(self._Okex_exchange),
                                       int(base["timeStamp"]),
                                       str(base["order_id"]),
                                       str(base["status"]), str(base["type"]),
                                       str(base["fSymbol"]),
                                       str(base["tSymbol"]),
                                       str(base["ask_or_bid"]),
                                       float(base["ask_bid_price"]),
                                       float(base["ask_bid_size"]),
                                       float(base["filled_price"]),
                                       float(base["filled_size"]),
                                       float(base["fee"]), str(group_id)))
                result.append({"server":str(self._Okex_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                base = self._Binance.createOrder(fSymbol, tSymbol, ask_or_bid,
                                                 price, quantity, ratio, type)
                TEMP_SQL_VALUE.append((str(self._Binance_exchange),
                                       int(base["timeStamp"]),
                                       str(base["order_id"]),
                                       str(base["status"]), str(base["type"]),
                                       str(base["fSymbol"]),
                                       str(base["tSymbol"]),
                                       str(base["ask_or_bid"]),
                                       float(base["ask_bid_price"]),
                                       float(base["ask_bid_size"]),
                                       float(base["filled_price"]),
                                       float(base["filled_size"]),
                                       float(base["fee"]), str(group_id)))
                result.append({"server":str(self._Binance_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                base = self._Huobi.createOrder(fSymbol, tSymbol, ask_or_bid,
                                               price, quantity, ratio, type)
                TEMP_SQL_VALUE.append((str(self._Huobi_exchange),
                                       int(base["timeStamp"]),
                                       str(base["order_id"]),
                                       str(base["status"]), str(base["type"]),
                                       str(base["fSymbol"]),
                                       str(base["tSymbol"]),
                                       str(base["ask_or_bid"]),
                                       float(base["ask_bid_price"]),
                                       float(base["ask_bid_size"]),
                                       float(base["filled_price"]),
                                       float(base["filled_size"]),
                                       float(base["fee"]), str(group_id)))
                result.append({"server":str(self._Huobi_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
            # return
            return result
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertCheckTradeOrderHistory(self,
                                     exchange,
                                     orderIDs,
                                     fSymbol,
                                     tSymbol,
                                     ratio=''):
        self._logger.debug("src.core.db.db.DB.insertCheckTradeOrderHistory")
        try:
            result = []
            TEMP_SQL_TITLE = UPDATE_CHECK_TRADE_ORDER_HISTORY_SQL
            TEMP_SQL_VALUE = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                for orderID in orderIDs:
                    base = self._Okex.checkOrder(orderID, fSymbol, tSymbol,
                                                 ratio)
                    TEMP_SQL_VALUE.append((str(self._Okex_exchange),
                                           int(base["timeStamp"]),
                                           str(base["order_id"]),
                                           str(base["status"]),
                                           str(base["type"]),
                                           str(base["fSymbol"]),
                                           str(base["tSymbol"]),
                                           str(base["ask_or_bid"]),
                                           float(base["ask_bid_price"]),
                                           float(base["ask_bid_size"]),
                                           float(base["filled_price"]),
                                           float(base["filled_size"]),
                                           float(base["fee"])))
                    result.append({"server":str(self._Okex_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                for orderID in orderIDs:
                    base = self._Binance.checkOrder(orderID, fSymbol, tSymbol,
                                                    ratio)
                    TEMP_SQL_VALUE.append((str(self._Binance_exchange),
                                           int(base["timeStamp"]),
                                           str(base["order_id"]),
                                           str(base["status"]),
                                           str(base["type"]),
                                           str(base["fSymbol"]),
                                           str(base["tSymbol"]),
                                           str(base["ask_or_bid"]),
                                           float(base["ask_bid_price"]),
                                           float(base["ask_bid_size"]),
                                           float(base["filled_price"]),
                                           float(base["filled_size"]),
                                           float(base["fee"])))
                    result.append({"server":str(self._Binance_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                for orderID in orderIDs:
                    base = self._Huobi.checkOrder(orderID, fSymbol, tSymbol,
                                                  ratio)
                    TEMP_SQL_VALUE.append((str(self._Huobi_exchange),
                                           int(base["timeStamp"]),
                                           str(base["order_id"]),
                                           str(base["status"]),
                                           str(base["type"]),
                                           str(base["fSymbol"]),
                                           str(base["tSymbol"]),
                                           str(base["ask_or_bid"]),
                                           float(base["ask_bid_price"]),
                                           float(base["ask_bid_size"]),
                                           float(base["filled_price"]),
                                           float(base["filled_size"]),
                                           float(base["fee"])))
                    result.append({"server":str(self._Huobi_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Others
            # to_be_continue
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
            # return
            return result
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertCancleTradeOrderHistory(self,
                                      exchange,
                                      orderIDs,
                                      fSymbol,
                                      tSymbol,
                                      ratio=''):
        self._logger.debug("src.core.db.db.DB.insertCheckTradeOrderHistory")
        try:
            result = []
            TEMP_SQL = []
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                res = self._Okex.cancelBatchOrder(orderIDs, fSymbol, tSymbol)
                if not res == []:
                    for base in res:
                        if base['status'] == CCAT_ORDER_STATUS_CANCELED:
                            TEMP_SQL.append(
                                UPDATE_CANCLE_TRADE_ORDER_HISTORY_SQL.
                                substitute(
                                    order_id=base['order_id'],
                                    status=base['status']))
                        result.append({"server":str(self._Okex_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                res = self._Binance.cancelBatchOrder(orderIDs, fSymbol,
                                                     tSymbol)
                if not res == []:
                    for base in res:
                        if base['status'] == CCAT_ORDER_STATUS_CANCELED:
                            TEMP_SQL.append(
                                UPDATE_CANCLE_TRADE_ORDER_HISTORY_SQL.
                                substitute(
                                    order_id=base['order_id'],
                                    status=base['status']))
                        result.append({"server":str(self._Binance_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                res = self._Huobi.cancelBatchOrder(orderIDs, fSymbol, tSymbol)
                if not res == []:
                    for base in res:
                        if base['status'] == CCAT_ORDER_STATUS_CANCELED:
                            TEMP_SQL.append(
                                UPDATE_CANCLE_TRADE_ORDER_HISTORY_SQL.
                                substitute(
                                    order_id=base['order_id'],
                                    status=base['status']))
                        result.append({"server":str(self._Huobi_exchange), "order_id":str(base["order_id"]), "status": str(base["status"])})
            # Others
            # to_be_continue
            if not TEMP_SQL == []:
                for TEMP in TEMP_SQL:
                    self._logger.debug(TEMP)
                    curs = self._conn.cursor()
                    curs.execute(TEMP)
                self._conn.commit()
                curs.close()
            # return
            return result
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertStatisticJudgeMarketTickerDis(self, statistic):
        self._logger.debug(
            "src.core.db.db.DB.insertStatisticJudgeMarketTickerDis: {statistic=%s}"
            % statistic)
        try:
            TEMP_SQL_TITLE = INSERT_STATISTIC_JUDGE_MARKET_TICKER_DIS_SQL
            TEMP_SQL_VALUE = []
            for s in statistic:
                TEMP_SQL_VALUE.append((int(s['timeStamp']),
                                       str(s['bid_server']),
                                       str(s['ask_server']), str(s['fSymbol']),
                                       str(s['tSymbol']),
                                       int(s['timeStamp_start']),
                                       int(s['timeStamp_end']),
                                       float(s['timeStamp_times']),
                                       float(s['timeStamp_period_times']),
                                       float(s['timeStamp_period_longest']),
                                       float(s['count_total']),
                                       float(s['count_forward']),
                                       float(s['count_backward']),
                                       float(s['gain_base_max']),
                                       float(s['gain_base_min']),
                                       float(s['gain_base_mean']),
                                       float(s['gain_base_std']),
                                       float(s['gain_ratio_max']),
                                       float(s['gain_ratio_min']),
                                       float(s['gain_ratio_mean']),
                                       float(s['gain_ratio_std']),
                                       str(s['group_id'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertStatisticJudgeMarketTickerTra(self, statistic):
        self._logger.debug(
            "src.core.db.db.DB.insertStatisticJudgeMarketTickerTra: {statistic=%s}"
            % statistic)
        try:
            TEMP_SQL_TITLE = INSERT_STATISTIC_JUDGE_MARKET_TICKER_TRA_SQL
            TEMP_SQL_VALUE = []
            for s in statistic:
                TEMP_SQL_VALUE.append((int(s['timeStamp']), str(s['server']),
                                       str(s['symbol_pair']),
                                       int(s['timeStamp_start']),
                                       int(s['timeStamp_end']),
                                       float(s['timeStamp_times']),
                                       float(s['timeStamp_period_times']),
                                       float(s['timeStamp_period_longest']),
                                       float(s['count_total']),
                                       float(s['count_forward']),
                                       float(s['count_backward']),
                                       float(s['gain_base_max']),
                                       float(s['gain_base_min']),
                                       float(s['gain_base_mean']),
                                       float(s['gain_base_std']),
                                       float(s['gain_ratio_max']),
                                       float(s['gain_ratio_min']),
                                       float(s['gain_ratio_mean']),
                                       float(s['gain_ratio_std']),
                                       str(s['group_id'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertStatisticJudgeMarketTickerPair(self, statistic):
        self._logger.debug(
            "src.core.db.db.DB.insertStatisticJudgeMarketTickerPair: {statistic=%s}"
            % statistic)
        try:
            TEMP_SQL_TITLE = INSERT_STATISTIC_JUDGE_MARKET_TICKER_PAIR_SQL
            TEMP_SQL_VALUE = []
            for s in statistic:
                TEMP_SQL_VALUE.append(
                    (int(s['timeStamp']), str(s['J1_server']),
                     str(s['J2_server']), str(s['symbol_pair']),
                     int(s['timeStamp_start']), int(s['timeStamp_end']),
                     float(s['timeStamp_times']),
                     float(s['timeStamp_period_times']),
                     float(s['timeStamp_period_longest']),
                     float(s['count_total']), float(s['count_forward']),
                     float(s['count_backward']), float(s['gain_base_max']),
                     float(s['gain_base_min']), float(s['gain_base_mean']),
                     float(s['gain_base_std']), float(s['gain_ratio_max']),
                     float(s['gain_ratio_min']), float(s['gain_ratio_mean']),
                     float(s['gain_ratio_std']), str(s['group_id'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertStatisticTradeBacktestHistory(self, statistic):
        self._logger.debug(
            "src.core.db.db.DB.insertStatisticTradeBacktestHistory: {statistic=%s}"
            % statistic)
        try:
            TEMP_SQL_TITLE = INSERT_STATISTIC_TRADE_BACKTEST_HISTORY
            TEMP_SQL_VALUE = []
            for s in statistic:
                TEMP_SQL_VALUE.append((int(s['timeStamp']),
                                       str(s['signal_id']),
                                       int(s['timeStamp_start']),
                                       int(s['timeStamp_end']),
                                       float(s['base_start']),
                                       float(s['base_end']),
                                       float(s['status_gain']),
                                       float(s['status_gain_max']),
                                       float(s['status_gain_min']),
                                       float(s['status_gain_diff_max']),
                                       float(s['status_gain_diff_min']),
                                       float(s['status_gain_diff_std']),
                                       str(s['group_id'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    def insertStatisticTradeOrderHistory(self, statistic):
        self._logger.debug(
            "src.core.db.db.DB.insertStatisticTradeOrderHistory: {statistic=%s}"
            % statistic)
        try:
            TEMP_SQL_TITLE = INSERT_STATISTIC_TRADE_BACKTEST_HISTORY
            TEMP_SQL_VALUE = []
            for s in statistic:
                TEMP_SQL_VALUE.append((int(s['timeStamp']),
                                       str(s['signal_id']),
                                       int(s['timeStamp_start']),
                                       int(s['timeStamp_end']),
                                       float(s['base_start']),
                                       float(s['base_end']),
                                       float(s['status_gain']),
                                       float(s['status_gain_max']),
                                       float(s['status_gain_min']),
                                       float(s['status_gain_diff_max']),
                                       float(s['status_gain_diff_min']),
                                       float(s['status_gain_diff_std']),
                                       str(s['group_id'])))
            if not TEMP_SQL_VALUE == []:
                self._logger.debug(TEMP_SQL_TITLE)
                self._logger.debug(TEMP_SQL_VALUE)
                curs = self._conn.cursor()
                curs.executemany(TEMP_SQL_TITLE, TEMP_SQL_VALUE)
                self._conn.commit()
                curs.close()
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    # db 紧急功能 不更新数据库
    def oneClickCancleOrders(self, exchange):
        self._logger.debug("src.core.db.db.DB.oneClickCancleOrders")
        try:
            done = True
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                done = done and self._Okex.oneClickCancleOrders()
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                done = done and self._Binance.oneClickCancleOrders()
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                done = done and self._Huobi.oneClickCancleOrders()
            # Others
            # to_be_continue
            return done
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)

    # db 紧急功能 不更新数据库
    def oneClickTransToBaseCoin(self, exchange, baseCoin):
        self._logger.debug("src.core.db.db.DB.oneClickTransToBaseCoin")
        try:
            done = True
            # Okex
            if exchange == "all" or self._Okex_exchange in exchange:
                done = done and self._Okex.oneClickTransToBaseCoin(baseCoin)
            # Binance
            if exchange == "all" or self._Binance_exchange in exchange:
                done = done and self._Binance.oneClickTransToBaseCoin(baseCoin)
            # Huobi
            if exchange == "all" or self._Huobi_exchange in exchange:
                done = done and self._Huobi.oneClickTransToBaseCoin(baseCoin)
            # Others
            # to_be_continue
            return done
        except (OkexException, BinanceException, HuobiException, sqlite3.Error,
                Exception) as err:
            raise DBException(err)
