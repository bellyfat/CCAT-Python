# -*- coding: utf-8 -*-

from string import Template

# get db view market ticker current tra sql
GET_VIEW_MARKET_TICKER_CURRENT_TRA_SQL = '''
    SELECT * FROM VIEW_MARKET_TICKER_CURRENT_TRA;
'''

# get db view market ticker current dis sql
GET_VIEW_MARKET_TICKER_CURRENT_DIS_SQL = '''
    SELECT * FROM VIEW_MARKET_TICKER_CURRENT_DIS;
'''

# get db view market ticker current sql
GET_VIEW_MARKET_TICKER_CURRENT_SQL = '''
    SELECT * FROM VIEW_MARKET_TICKER_CURRENT;
'''

# get db view market kline current sql
GET_VIEW_MARKET_KLINE_CURRENT_SQL = '''
    SELECT * FROM VIEW_MARKET_KLINE_CURRENT;
'''

# get db view market symbol sql
GET_VIEW_MARKET_TICKER_SYMBOL_SQL = '''
    SELECT V1.*
    FROM VIEW_MARKET_SYMBOL V1
    LEFT JOIN VIEW_MARKET_TICKER_CURRENT_DIS V2 ON (V1.server = V2.bid_server OR V1.server = V2.ask_server) AND V1.fSymbol = V2.fSymbol AND V1.tSymbol = V2.tSymbol
    WHERE V2.bid_server IS NOT NULL;
'''

# get db view market symbol sql
GET_VIEW_MARKET_SYMBOL_PAIRS_AGGDEPTH_SQL = Template('''
    SELECT max(limit_price_step) as aggDepth
    FROM INFO_SYMBOL
    WHERE server IN $server and fSymbol='$fSymbol' and tSymbol='$tSymbol';
''')


# get db view market symbol sql
GET_VIEW_MARKET_SYMBOL_PAIRS_SQL = Template('''
    SELECT * FROM VIEW_MARKET_SYMBOL WHERE server IN $server;
''')

# get db view info symbol sql
GET_VIEW_INFO_SYMBOL_PAIRS_SQL = Template('''
    SELECT * FROM VIEW_INFO_SYMBOL WHERE server IN $server;
''')

# get db view account balance current sql
GET_VIEW_ACCOUNT_BALANCE_CURRENT_SQL = '''
    SELECT * FROM VIEW_ACCOUNT_BALANCE_CURRENT;
'''

# get db view account withdraw current sql
GET_VIEW_ACCOUNT_WITHDRAW_CURRENT_SQL = '''
    SELECT * FROM VIEW_ACCOUNT_WITHDRAW_CURRENT;
'''

# get db account info sql
GET_ACCOUNT_BALANCE_HISTORY_SQL = Template('''
    SELECT DISTINCT server, asset FROM ACCOUNT_BALANCE_HISTORY WHERE server IN $server;
''')
# get db withdraw history sql
GET_ACCOUNT_WITHDRAW_HISTORY_SQL = '''
    SELECT * FROM ACCOUNT_WITHDRAW_HISTORY;
'''

# get db server info sql
GET_INFO_SERVER_SQL = '''
    SELECT * FROM INFO_SERVER;
'''
# get db symbol info sql
GET_INFO_SYMBOL_SQL = '''
    SELECT * FROM INFO_SYMBOL;
'''
# get db withdraw info sql
GET_INFO_WITHDRAW_SQL = Template('''
    SELECT * FROM INFO_WITHDRAW WHERE server IN $server;
''')

# get db market depth sql
GET_MARKET_DEPTH_SQL = '''
    SELECT * FROM MARKET_DEPTH;
'''
# get db market kline sql
GET_MARKET_KLINE_SQL = '''
    SELECT * FROM MARKET_KLINE;
'''
# delete db market kline sql
DEL_MARKET_KLINE_SQL = '''
    DELETE FROM MARKET_KLINE;
'''
# get db market ticker sql
GET_MARKET_TIKER_SQL = '''
    SELECT * FROM MARKET_TIKER;
'''

# get db trade backtest history sql
GET_TRADE_BACKTEST_HISTORY_SQL = '''
    SELECT * FROM TRADE_BACKTEST_HISTORY;
'''
# get db trade order history sql
GET_TRADE_ORDER_HISTORY_SQL = '''
    SELECT * FROM TRADE_ORDER_HISTORY;
'''

# insert db account balance history sql
INSERT_ACCOUNT_BALANCE_HISTORY_SQL = '''
    INSERT OR REPLACE INTO ACCOUNT_BALANCE_HISTORY (server, timeStamp, asset, balance, free, locked)
    VALUES (?, ?, ?, ?, ?, ?)'''

# insert db account withdraw history sql
INSERT_ACCOUNT_WITHDRAW_HISTORY_SQL = '''
    INSERT OR REPLACE INTO ACCOUNT_WITHDRAW_HISTORY (server, timeStamp, asset, deposit, withdraw)
    VALUES (?, ?, ?, ?, ?)'''

# insert db info server sql
INSERT_INFO_SERVER_SQL = '''
    INSERT OR REPLACE INTO INFO_SERVER (server, info_second, market_second, orders_second, webSockets_second)
    VALUES (?, ?, ?, ?, ?)'''

# insert db info symbol sql
INSERT_INFO_SYMBOL_SQL = '''
    INSERT OR REPLACE INTO INFO_SYMBOL (server, fSymbol, tSymbol, limit_price_precision, limit_price_max, limit_price_min, limit_price_step, limit_size_precision, limit_size_max, limit_size_min, limit_size_step, limit_min_notional, fee_maker, fee_taker)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db info withdraw sql
INSERT_INFO_WITHDRAW_SQL = '''
    INSERT OR REPLACE INTO INFO_WITHDRAW (server, asset, can_deposit, can_withdraw, min_withdraw)
    VALUES (?, ?, ?, ?, ?)'''

# insert db market depth sql
INSERT_MARKET_DEPTH_SQL = '''
    INSERT OR REPLACE INTO MARKET_DEPTH (server, timeStamp, fSymbol, tSymbol, bid_price_size, ask_price_size)
    VALUES (?, ?, ?, ?, ?, ?)'''

# insert db market kline sql
INSERT_MARKET_KLINE_SQL = '''
    INSERT OR REPLACE INTO MARKET_KLINE (server, timeStamp, fSymbol, tSymbol, open, high, low, close, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db market tiker sql
INSERT_MARKET_TIKER_SQL = '''
    INSERT OR REPLACE INTO MARKET_TIKER (server, timeStamp, fSymbol, tSymbol, bid_one_price, bid_one_size, ask_one_price, ask_one_size)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db trade backtest history sql
INSERT_TRADE_BACKTEST_HISTORY_SQL = '''
    INSERT OR REPLACE INTO TRADE_BACKTEST_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db trade order history sql
INSERT_TRADE_ORDER_HISTORY_SQL = '''
    INSERT OR REPLACE INTO TRADE_ORDER_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

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
    	`fee`	REAL,
        PRIMARY KEY (order_id)
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
    	`fee`	REAL,
        PRIMARY KEY (order_id)
    );
    CREATE TABLE IF NOT EXISTS `MARKET_TIKER` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`bid_one_price`	REAL,
    	`bid_one_size`	REAL,
    	`ask_one_price`	REAL,
    	`ask_one_size`	REAL,
        PRIMARY KEY (server, timeStamp, fSymbol, tSymbol)
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
    	`volume`	REAL,
        PRIMARY KEY (server, timeStamp, fSymbol, tSymbol)
    );
    CREATE TABLE IF NOT EXISTS `MARKET_DEPTH` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`bid_price_size`	TEXT,
    	`ask_price_size`	TEXT,
        PRIMARY KEY (server, timeStamp, fSymbol, tSymbol)
    );
    CREATE TABLE IF NOT EXISTS `INFO_WITHDRAW` (
    	`server`	TEXT NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`can_deposit`	TEXT,
    	`can_withdraw`	TEXT,
    	`min_withdraw`	REAL,
        PRIMARY KEY (server, asset)
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
    	`fee_taker`	REAL,
        PRIMARY KEY (server, fSymbol, tSymbol)
    );
    CREATE TABLE IF NOT EXISTS `INFO_SERVER` (
    	`server`	TEXT NOT NULL,
    	`info_second`	REAL,
    	`market_second`	REAL,
    	`orders_second`	REAL,
    	`webSockets_second`	REAL,
        PRIMARY KEY (server)
    );
    CREATE TABLE IF NOT EXISTS `ACCOUNT_WITHDRAW_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`deposit`	TEXT,
    	`withdraw`	TEXT,
        PRIMARY KEY (server, timeStamp, asset)
    );
    CREATE TABLE IF NOT EXISTS `ACCOUNT_BALANCE_HISTORY` (
    	`server`	TEXT NOT NULL,
    	`timeStamp`	INTEGER NOT NULL,
    	`asset`	TEXT NOT NULL,
    	`balance`	REAL,
    	`free`	REAL,
    	`locked`	REAL,
        PRIMARY KEY (server, timeStamp, asset)
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
CREATE_VIEWS_SQL = Template('''
    BEGIN TRANSACTION;
    CREATE VIEW IF NOT EXISTS VIEW_INFO_SYMBOL
        AS
        	SELECT S1.*
            FROM INFO_SYMBOL S1,INFO_SYMBOL S2
            WHERE S1.server<>S2.server AND S1.fSymbol = S2.fSymbol AND S1.tSymbol = S2.tSymbol;
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
            WHERE (B1.deposit<>'' OR B1.withdraw <>'') and B2.server IS NULL;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_KLINE_CURRENT
    	AS
    			SELECT M1.*, M2.close as tSymbol_base, M1.close*M1.volume*M2.close as price_volume_base
    			FROM MARKET_KLINE M1
    			JOIN MARKET_KLINE M2 ON M1.server = M2.server AND M1.timeStamp = M2.timeStamp AND M1.tSymbol = M2.fSymbol AND M1.tSymbol<>'$baseCoin' AND M2.tSymbol ='$baseCoin'
    		UNION
    			SELECT M1.*, M1.close as tSymbol_base, M1.close*M1.volume as price_volume_base
    			FROM MARKET_KLINE M1
    			WHERE M1.tSymbol = '$baseCoin';
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_SYMBOL
    	AS
            SELECT J2.*
            FROM(
                SELECT DISTINCT V1.server, V1.fSymbol, V1.tSymbol
                FROM(
                        SELECT DISTINCT server, fSymbol, tSymbol
                        FROM VIEW_INFO_SYMBOL
                        EXCEPT
                        SELECT DISTINCT server, fSymbol, tSymbol
                        FROM VIEW_MARKET_KLINE_CURRENT
                        WHERE price_volume_base < $basePriceVolume
                    ) V1
                    LEFT JOIN(
                        SELECT DISTINCT server, fSymbol, tSymbol
                        FROM VIEW_INFO_SYMBOL
                        EXCEPT
                        SELECT DISTINCT server, fSymbol, tSymbol
                        FROM VIEW_MARKET_KLINE_CURRENT
                        WHERE price_volume_base < $basePriceVolume
                    ) V2 ON V1.server <> V2.server AND V1.fSymbol = V2.fSymbol AND V1.tSymbol = V2.tSymbol
                WHERE V2.server IS NOT NULL
            ) J1
            JOIN VIEW_INFO_SYMBOL J2 ON J1.server = J2.server AND J1.fSymbol = J2.fSymbol AND J1.tSymbol = J2.tSymbol;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_TICKER_CURRENT
    	AS
        		SELECT V1.*, V1.bid_one_price*(V2.bid_one_price+V2.ask_one_price)/2 as bid_one_price_base, V1.bid_one_size*V1.bid_one_price*(V2.bid_one_price+V2.ask_one_price)/2 as bid_one_price_size_base, V1.ask_one_price*(V2.bid_one_price+V2.ask_one_price)/2 as ask_one_price_base, V1.ask_one_size*V1.ask_one_price*(V2.bid_one_price+V2.ask_one_price)/2 as ask_one_price_size_base
        		FROM(
        			SELECT M1.*
        			FROM MARKET_TIKER M1
        			LEFT JOIN MARKET_TIKER M2 ON M1.server = M2.server AND M1.fSymbol = M2.fSymbol AND M1.tSymbol = M2.tSymbol AND M1.timeStamp < M2.timeStamp
        			WHERE M2.server IS NULL
        		) V1
        		JOIN(
        			SELECT M1.*
        			FROM MARKET_TIKER M1
        			LEFT JOIN MARKET_TIKER M2 ON M1.server = M2.server AND M1.fSymbol = M2.fSymbol AND M1.tSymbol = M2.tSymbol AND M1.timeStamp < M2.timeStamp
        			WHERE M2.server IS NULL
        		) V2 ON V1.server = V2.server AND V1.tSymbol = V2.fSymbol AND V1.tSymbol<>'$baseCoin' AND V2.tSymbol ='$baseCoin'
        	UNION
        		SELECT V3.*, V3.bid_one_price as bid_one_price_base, V3.bid_one_size*V3.bid_one_price as bid_one_price_size_base, V3.ask_one_price as ask_one_price_base, V3.ask_one_size*V3.ask_one_price as ask_one_price_size_base
        		FROM(
        			SELECT M1.*
        			FROM MARKET_TIKER M1
        			LEFT JOIN MARKET_TIKER M2 ON M1.server = M2.server AND M1.fSymbol = M2.fSymbol AND M1.tSymbol = M2.tSymbol AND M1.timeStamp < M2.timeStamp
        			WHERE M2.server IS NULL AND M1.tSymbol='$baseCoin'
        		) V3;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_TICKER_CURRENT_DIS
    	AS
    		SELECT V1.server as bid_server, V1.timeStamp as bid_timeStamp, V2.server as ask_server, V2.timeStamp as ask_timeStamp, V1.fSymbol, V1.tSymbol, V1.bid_one_price as bid_price, min(V1.bid_one_size, V2.ask_one_size) as bid_size,
    			V1.bid_one_price_base as bid_price_base, min(V1.bid_one_size, V2.ask_one_size)*V1.bid_one_price_base as bid_price_size_base, V2.ask_one_price as ask_price,
    			min(V1.bid_one_size, V2.ask_one_size) as ask_size, V2.ask_one_price_base as ask_price_base,	min(V1.bid_one_size, V2.ask_one_size)*V2.ask_one_price_base as ask_price_size_base,
    			min(V1.bid_one_size, V2.ask_one_size)*(V1.bid_one_price_base-V2.ask_one_price_base) as dis_price_size_base
    		FROM VIEW_MARKET_TICKER_CURRENT V1
    		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server <> V2.server AND V1.fSymbol = V2.fSymbol AND V1.tSymbol = V2.tSymbol
    		WHERE abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND (V1.ask_one_price-V2.bid_one_price) > ((V1.ask_one_price-V1.bid_one_price)+(V2.ask_one_price-V2.bid_one_price))
    		ORDER BY dis_price_size_base DESC;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_TICKER_CURRENT_TRA
    	AS
    	SELECT V1.server, V1.timeStamp, V1.fSymbol as bid_fSymbol, V1.tSymbol as bid_tSymbol, V2.fSymbol as ask_fSymbol, V2.tSymbol as ask_tSymbol,
    		V1.bid_one_price as bid_price, min(V1.bid_one_size, V2.ask_one_size) as bid_size,
    		V1.bid_one_price_base as bid_price_base, min(V1.bid_one_size, V2.ask_one_size)*V1.bid_one_price_base as bid_price_size_base, V2.ask_one_price as ask_price,
    		min(V1.bid_one_size, V2.ask_one_size) as ask_size, V2.ask_one_price_base as ask_price_base,	min(V1.bid_one_size, V2.ask_one_size)*V2.ask_one_price_base as ask_price_size_base,
    		min(V1.bid_one_size, V2.ask_one_size)*(V1.bid_one_price_base-V2.ask_one_price_base) as dis_price_size_base
    	FROM VIEW_MARKET_TICKER_CURRENT V1
    	LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol=V2.fSymbol AND V1.tSymbol <> V2.tSymbol
    	WHERE abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V1.bid_one_price_base > V2.ask_one_price_base
    	ORDER BY dis_price_size_base DESC;
    COMMIT;
''')
