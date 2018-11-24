# -*- coding: utf-8 -*-

from string import Template

# get db view symbol info sql
GET_VIEW_INFO_SYMBOL_PAIRS_SQL = Template('''
    SELECT * FROM VIEW_INFO_SYMBOL WHERE server IN $server
''')

GET_VIEW_ACCOUNT_BALANCE_CURRENT_SQL = Template('''
    SELECT * FROM VIEW_ACCOUNT_BALANCE_CURRENT WHERE server IN $server;
''')

# get db account info sql
GET_ACCOUNT_INFO_SQL = '''
    SELECT * FROM ACCOUNT_BALANCE_HISTORY;
'''
# get db market depth sql
GET_MARKET_DEPTH_SQL = '''
    SELECT * FROM MARKET_DEPTH;
'''
# get db market kline sql
GET_MARKET_KLINE_SQL = '''
    SELECT * FROM MARKET_KLINE;
'''
# get db market ticker sql
GET_MARKET_TIKER_SQL = '''
    SELECT * FROM MARKET_TIKER;
'''
# get db server info sql
GET_INFO_SERVER_SQL = '''
    SELECT * FROM INFO_SERVER;
'''
# get db symbol info sql
GET_INFO_SYMBOL_SQL = '''
    SELECT * FROM INFO_SYMBOL;
'''
# get db trade backtest history sql
GET_TRADE_BACKTEST_HISTORY_SQL = '''
    SELECT * FROM TRADE_BACKTEST_HISTORY;
'''
# get db trade order history sql
GET_TRADE_ORDER_HISTORY_SQL = '''
    SELECT * FROM TRADE_ORDER_HISTORY;
'''
# get db withdraw history sql
GET_WITHDRAW_HISTORY_SQL = '''
    SELECT * FROM ACCOUNT_WITHDRAW_HISTORY;
'''
# get db withdraw info sql
GET_INFO_WITHDRAW_SQL = '''
    SELECT * FROM INFO_WITHDRAW;
'''

# insert db account balance history sql
INSERT_ACCOUNT_BALANCE_HISTORY_SQL_TITLE = '''
    INSERT INTO ACCOUNT_BALANCE_HISTORY (server, timeStamp, asset, balance, free, locked)
    VALUES (?, ?, ?, ?, ?, ?)'''
INSERT_ACCOUNT_BALANCE_HISTORY_SQL_VALUE = Template('''('$server', $timeStamp, '$asset', $balance, $free, $locked)''')

# insert db account withdraw history sql
INSERT_ACCOUNT_WITHDRAW_HISTORY_SQL_TITLE = '''
    INSERT INTO ACCOUNT_WITHDRAW_HISTORY (server, timeStamp, asset, deposite, withdraw)
    VALUES (?, ?, ?, ?, ?)'''
INSERT_ACCOUNT_WITHDRAW_HISTORY_SQL_VALUE = Template('''('$server', $timeStamp, '$asset', '$deposite', '$withdraw')''')

# insert db info server sql
INSERT_INFO_SERVER_SQL_TITLE = '''
    INSERT OR REPLACE INTO INFO_SERVER (server, requests_second, orders_second, orders_day, webSockets_second)
    VALUES (?, ?, ?, ?, ?)'''
INSERT_INFO_SERVER_SQL_VALUE = Template('''('$server', $requests_second, $orders_second, $orders_day, $webSockets_second)''')

# insert db info symbol sql
INSERT_INFO_SYMBOL_SQL_TITLE = '''
    INSERT INTO INFO_SYMBOL (server, fSymbol, tSymbol, limit_price_precision, limit_price_max, limit_price_min, limit_price_step, limit_size_precision, limit_size_max, limit_size_min, limit_size_step, limit_min_notional, fee_maker, fee_taker)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_INFO_SYMBOL_SQL_VALUE = Template('''('$server', '$fSymbol', '$tSymbol', $limit_price_precision, $limit_price_max, $limit_price_min, $limit_price_step, $limit_size_precision, $limit_size_max, $limit_size_min, $limit_size_step, $limit_min_notional, $fee_maker, $fee_taker)''')

# insert db info withdraw sql
INSERT_INFO_WITHDRAW_SQL_TITLE = '''
    INSERT INTO INFO_WITHDRAW (server, asset, can_deposite, can_withdraw, min_withdraw)
    VALUES (?, ?, ?, ?, ?)'''
INSERT_INFO_WITHDRAW_SQL_VALUE = Template('''('$server', '$asset', '$can_deposite', '$can_withdraw', $min_withdraw)''')


# insert db market depth sql
INSERT_MARKET_DEPTH_SQL_TITLE = '''
    INSERT INTO MARKET_DEPTH (server, timeStamp, fSymbol, tSymbol, bid_price_size, ask_price_size)
    VALUES (?, ?, ?, ?, ?, ?)'''
INSERT_MARKET_DEPTH_SQL_VALUE = Template('''('$server', $timeStamp, '$fSymbol', '$tSymbol', '$bid_price_size', '$ask_price_size')''')

# insert db market kline sql
INSERT_MARKET_KLINE_SQL_TITLE = '''
    INSERT INTO MARKET_KLINE (server, timeStamp, fSymbol, tSymbol, open, high, low, close, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_MARKET_KLINE_SQL_VALUE = Template('''('$server', $timeStamp, '$fSymbol', '$tSymbol', $open, $high, $low, $close, $volume)''')

# insert db market tiker sql
INSERT_MARKET_TIKER_SQL_TITLE = '''
    INSERT INTO MARKET_TIKER (server, timeStamp, fSymbol, tSymbol, bid_one_price, bid_one_size, ask_one_price, ask_one_size)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_MARKET_TIKER_SQL_VALUE = Template('''('$server', $timeStamp, '$fSymbol', '$tSymbol', $bid_one_price, $bid_one_size, $ask_one_price, $ask_one_size)''')

# insert db trade backtest history sql
INSERT_TRADE_BACKTEST_HISTORY_SQL_TITLE = '''
    INSERT OR REPLACE INTO TRADE_BACKTEST_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_TRADE_BACKTEST_HISTORY_SQL_VALUE = Template('''('$server', $timeStamp, '$order_id', '$status', '$type', '$fSymbol', '$tSymbol', '$ask_or_bid', $ask_bid_price, $ask_bid_size, $filled_price, $filled_size, $fee)''')

# insert db trade order history sql
INSERT_TRADE_ORDER_HISTORY_SQL_TITLE = '''
    INSERT OR REPLACE INTO TRADE_ORDER_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
INSERT_TRADE_ORDER_HISTORY_SQL_VALUE = Template('''('$server', $timeStamp, '$order_id', '$status', '$type', '$fSymbol', '$tSymbol', '$ask_or_bid', $ask_bid_price, $ask_bid_size, $filled_price, $filled_size, $fee)''')


# get db talbes sql
GET_TABLES_SQL = '''
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
'''
# creat db tables sql
CREATE_TABELS_SQL = '''
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS `TRADE_ORDER_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`order_id`	TEXT NOT NULL UNIQUE,
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
    	`order_id`	TEXT NOT NULL UNIQUE,
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
    	`bid_price_size`	BLOB,
    	`ask_price_size`	BLOB
    );
    CREATE TABLE IF NOT EXISTS `INFO_WITHDRAW` (
    	`server`	TEXT NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`can_deposite`	TEXT NOT NULL,
    	`can_withdraw`	TEXT NOT NULL,
    	`min_withdraw`	REAL
    );
    CREATE TABLE IF NOT EXISTS `INFO_SYMBOL` (
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
    CREATE TABLE IF NOT EXISTS `INFO_SERVER` (
    	`server`	TEXT NOT NULL UNIQUE,
    	`requests_second`	REAL,
    	`orders_second`	REAL,
    	`orders_day`	REAL,
    	`webSockets_second`	REAL
    );
    CREATE TABLE IF NOT EXISTS `ACCOUNT_WITHDRAW_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`deposite`	TEXT,
    	`withdraw`	TEXT
    );
    CREATE TABLE IF NOT EXISTS `ACCOUNT_BALANCE_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`balance`	REAL,
    	`free`	REAL,
    	`locked`	REAL
    );
    COMMIT;
'''

# get db talbes sql
GET_VIEWS_SQL = '''
    SELECT name FROM sqlite_master
    WHERE type='view'
    ORDER BY name;
'''
# creat view sql
CREATE_VIEWS_SQL = '''
    BEGIN TRANSACTION;
    CREATE VIEW IF NOT EXISTS VIEW_INFO_SYMBOL
        AS
        	SELECT S1.*
            FROM INFO_SYMBOL S1,INFO_SYMBOL S2
            WHERE S1.server<>S2.server AND S1.fSymbol = S2.fSymbol AND S1.tSymbol = S2.tSymbol
            ORDER BY fSymbol, tSymbol;
    CREATE VIEW IF NOT EXISTS VIEW_ACCOUNT_BALANCE_CURRENT
        AS
			SELECT B1.*
			FROM ACCOUNT_BALANCE_HISTORY B1
			LEFT JOIN ACCOUNT_BALANCE_HISTORY B2 ON B1.server = B2.server AND B1.asset = B2.asset AND B1.timeStamp < B2.timeStamp
			WHERE B2.server IS NULL;
    CREATE VIEW IF NOT EXISTS VIEW_ACCOUNT_WITHDRAW_CURRENT
        AS
            SELECT B1.*
            FROM ACCOUNT_WITHDRAW_HISTORY B1
            LEFT JOIN ACCOUNT_WITHDRAW_HISTORY B2 ON B1.server = B2.server AND B1.asset = B2.asset AND B1.timeStamp < B2.timeStamp
            WHERE (B1.deposite<>'' OR B1.withdraw <>'') and B2.server IS NULL;
    COMMIT;
'''
