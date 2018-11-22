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
	`server`	TEXT NOT NULL UNIQUE,
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
CREATE VIEW VIEW_INFO_SYMBOL
    AS
    	SELECT S1.*
        FROM INFO_SYMBOL S1,INFO_SYMBOL S2
        WHERE S1.server<>S2.server AND S1.fSymbol = S2.fSymbol AND S1.tSymbol = S2.tSymbol
        ORDER BY fSymbol, tSymbol;
COMMIT;
