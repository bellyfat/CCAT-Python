BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `WITHDRAW_INFO` (
	`server`	TEXT NOT NULL,
	`asset`	TEXT NOT NULL,
	`can_deposite`	INTEGER,
	`can_withdraw`	INTEGER,
	`min_withdraw`	REAL
);
CREATE TABLE IF NOT EXISTS `WITHDRAW_HISTORY` (
	`to_be_continue`	TEXT
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
	`server_name`	TEXT NOT NULL,
	`fSymbol`	TEXT NOT NULL,
	`tSymbol`	TEXT NOT NULL,
	`limit_price_precision`	REAL,
	`limit_price_max`	REAL,
	`limit_price_min`	REAL,
	`limit_price_step`	REAL,
	`limit_size_precision`	REAL,
	`limit_size_max`	REAL,
	`limit_size_min`	REAL,
	`limit_min_notional`	REAL,
	`fee_maker`	REAL,
	`fee_taker`	REAL
);
CREATE TABLE IF NOT EXISTS `SERVER_INFO` (
	`server_name`	TEXT NOT NULL UNIQUE,
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
	`account`	TEXT NOT NULL DEFAULT 'CCAT',
	`timeStamp`	INTEGER NOT NULL,
	`asset`	TEXT NOT NULL,
	`balance`	INTEGER,
	`free`	INTEGER,
	`locked`	INTEGER
);
COMMIT;
