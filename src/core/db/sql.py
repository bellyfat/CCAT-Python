# -*- coding: utf-8 -*-

from string import Template


# insert db withdraw info sql
INSERT_WITHDRAW_INFO_SQL = Template("""
    INSERT INTO WITHDRAW_INFO (server, asset, can_deposite, can_withdraw, min_withdraw)
    VALUES ("$server", "$asset", "$can_deposite", "$can_withdraw", $min_withdraw)
""")

# get db withdraw info sql
GET_WITHDRAW_INFO_SQL = """
    SELECT * FROM WITHDRAW_INFO
"""
# insert db account info sql
INSERT_ACCOUNT_INFO_SQL = Template("""
    INSERT INTO ACCOUNT_INFO (server, account, timeStamp, asset, balance, free, locked)
    VALUES ("$server", "$account", $timeStamp, "$asset", $balance, $free, $locked)
""")

# get db account info sql
GET_ACCOUNT_INFO_SQL = """
    SELECT * FROM ACCOUNT_INFO
"""

# insert db symbol info sql
INSERT_SYMBOL_INFO_SQL = Template("""
    INSERT INTO SYMBOL_INFO (server, fSymbol, tSymbol, limit_price_precision, limit_price_max, limit_price_min, limit_price_step, limit_size_precision, limit_size_max, limit_size_min, limit_size_step, limit_min_notional, fee_maker, fee_taker)
    VALUES ("$server", "$fSymbol", "$tSymbol", $limit_price_precision, $limit_price_max, $limit_price_min, $limit_price_step, $limit_size_precision, $limit_size_max, $limit_size_min, $limit_size_step, $limit_min_notional, $fee_maker, $fee_taker)
""")

# get db symbol info sql
GET_SYMBOL_INFO_SQL = """
    SELECT * FROM SYMBOL_INFO
"""

# insert db server info sql
INSERT_SERVER_INFO_SQL = Template("""
    INSERT INTO SERVER_INFO (server, requests_second, orders_second, orders_day, webSockets_second)
    VALUES ("$server", $requests_second, $orders_second, $orders_day, $webSockets_second)
""")

# get db server info sql
GET_SERVER_INFO_SQL = """
    SELECT * FROM SERVER_INFO
"""

# get db talbes sql
GET_TABLES_SQL = """
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
"""

# creat db tables sql
CREATE_TABELS_SQL = """
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS `WITHDRAW_INFO` (
    	`server`	TEXT NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`can_deposite`	TEXT NOT NULL,
    	`can_withdraw`	TEXT NOT NULL,
    	`min_withdraw`	REAL
    );
    CREATE TABLE IF NOT EXISTS `WITHDRAW_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
        `deposite`  TEXT,
        `withdraw`  TEXT
    );
    CREATE TABLE IF NOT EXISTS `TRADE_ORDER_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`order_id`	TEXT NOT NULL,
    	`status`	TEXT,
    	`type`	TEXT NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`ask_or_bid`	TEXT NOT NULL,
    	`ask_bid_price`	REAL NOT NULL,
    	`ask_bid_size`	REAL NOT NULL,
    	`filled_price`	REAL,
    	`filled_size`	REAL,
    	`fee`	REAL
    );
    CREATE TABLE IF NOT EXISTS `TRADE_BACKTEST_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`order_id`	TEXT NOT NULL,
    	`status`	TEXT,
    	`type`	TEXT NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`ask_or_bid`	TEXT NOT NULL,
    	`ask_bid_price`	REAL NOT NULL,
    	`ask_bid_size`	REAL NOT NULL,
    	`filled_price`	REAL,
    	`filled_size`	REAL,
    	`fee`	REAL
    );
    CREATE TABLE IF NOT EXISTS `SYMBOL_INFO` (
    	`server`	TEXT NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`limit_price_precision`	REAL,
    	`limit_price_max`	REAL,
    	`limit_price_min`	REAL,
    	`limit_price_step`	REAL,
    	`limit_size_precision`	REAL,
    	`limit_size_max`	REAL,
    	`limit_size_min`	REAL,
    	`limit_size_step`	REAL,
    	`limit_min_notional`	REAL,
    	`fee_maker`	REAL,
    	`fee_taker`	REAL
    );
    CREATE TABLE IF NOT EXISTS `SERVER_INFO` (
    	`server`	TEXT NOT NULL UNIQUE,
    	`requests_second`	REAL,
    	`orders_second`	REAL,
    	`orders_day`	REAL,
    	`webSockets_second`	REAL
    );
    CREATE TABLE IF NOT EXISTS `MARKET_TIKER` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`bid_one_price`	REAL,
    	`bid_one_size`	REAL,
    	`ask_one_price`	REAL,
    	`ask_one_size`	REAL
    );
    CREATE TABLE IF NOT EXISTS `MARKET_KLINE` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	TEXT NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`open`	REAL,
    	`high`	REAL,
    	`low`	REAL,
    	`close`	REAL,
    	`volume`	REAL
    );
    CREATE TABLE IF NOT EXISTS `MARKET_DEPTH` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`bid_price_size`	TEXT,
    	`ask_price_size`	TEXT
    );
    CREATE TABLE IF NOT EXISTS `ACCOUNT_INFO` (
    	`server`	TEXT NOT NULL,
    	`account`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`balance`	REAL,
    	`free`	REAL,
    	`locked`	REAL
    );
    COMMIT;
"""

# creat view sql
