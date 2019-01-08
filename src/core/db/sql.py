# -*- coding: utf-8 -*-

from string import Template

# get db signal trade current sql
GET_VIEW_SIGNAL_TRADE_CURRENT_SQL = Template('''
    SELECT *
    FROM VIEW_SIGNAL_TRADE_CURRENT
    WHERE timeStamp>(strftime('%s', 'now')-$timeout)*1000;
''')

# get db statistic judge market ticker pair current server sql
GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT_SERVER_SQL = Template('''
        SELECT *
        FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT
        WHERE J1_server='$server' AND J2_server='$server_pair'
    UNION
        SELECT *
        FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT
        WHERE J1_server='$server_pair' AND J2_server='$server';
''')
# get db statistic judge market ticker pair current sql
GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT_SQL = '''
    SELECT * FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT;
'''

# get db statistic judge market ticker tra current server sql
GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT_SERVER_SQL = Template('''
    SELECT * FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT WHERE server IN $server;
''')
# get db statistic judge market ticker tra current sql
GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT_SQL = '''
    SELECT * FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT;
'''

# get db statistic judge market ticker dis current server sql
GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT_SERVER_SQL = Template('''
        SELECT *
        FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT
        WHERE bid_server='$server' AND ask_server='$server_pair'
    UNION
        SELECT *
        FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT
        WHERE bid_server='$server_pair' AND ask_server='$server';
''')
# get db statistic judge market ticker dis current sql
GET_VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT_SQL = '''
    SELECT * FROM VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT;
'''

# get db judge market ticker pair current server sql
GET_VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT_SERVER_SQL = Template('''
        SELECT *
        FROM VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT
        WHERE J1_server='$server' AND J2_server='$server_pair'
    UNION
        SELECT *
        FROM VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT
        WHERE J1_server='$server_pair' AND J2_server='$server';
''')
# get db judge market ticker pair current sql
GET_VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT_SQL = '''
    SELECT * FROM VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT;
'''

# get db judge market ticker tra current server sql
GET_VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT_SERVER_SQL = Template('''
    SELECT * FROM VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT WHERE server IN $server;
''')
# get db judge signal ticker tra current sql
GET_VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT_SQL = '''
    SELECT * FROM VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT;
'''

# get db judge market ticker dis current server sql
GET_VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT_SERVER_SQL = Template('''
        SELECT *
        FROM VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT
        WHERE bid_server='$server' AND ask_server='$server_pair'
    UNION
        SELECT *
        FROM VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT
        WHERE bid_server='$server_pair' AND ask_server='$server';
''')
# get db judge market ticker dis current sql
GET_VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT_SQL = '''
    SELECT * FROM VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT;
'''

# get db view market ticker current pair server sql
GET_VIEW_MARKET_TICKER_CURRENT_PAIR_SERVER_SQL = Template('''
        SELECT *
        FROM VIEW_MARKET_TICKER_CURRENT_PAIR
        WHERE J1_server='$server_pair' AND J2_server='$server'
    UNION
        SELECT *
        FROM VIEW_MARKET_TICKER_CURRENT_PAIR
        WHERE J1_server='$server_pair' AND J2_server='$server';
''')
# get db view market ticker current pair sql
GET_VIEW_MARKET_TICKER_CURRENT_PAIR_SQL = '''
    SELECT * FROM VIEW_MARKET_TICKER_CURRENT_PAIR;
'''

# get db view market ticker current tra server sql
GET_VIEW_MARKET_TICKER_CURRENT_TRA_SERVER_SQL = Template('''
    SELECT * FROM VIEW_MARKET_TICKER_CURRENT_TRA WHERE server IN $server;
''')
# get db view market ticker current tra sql
GET_VIEW_MARKET_TICKER_CURRENT_TRA_SQL = '''
    SELECT * FROM VIEW_MARKET_TICKER_CURRENT_TRA;
'''

# get db view market ticker current dis server sql
GET_VIEW_MARKET_TICKER_CURRENT_DIS_SERVER_SQL = Template('''
        SELECT *
        FROM VIEW_MARKET_TICKER_CURRENT_DIS
        WHERE bid_server='$server' AND ask_server='$server_pair'
    UNION
        SELECT *
        FROM VIEW_MARKET_TICKER_CURRENT_DIS
        WHERE bid_server='$server_pair' AND ask_server='$server';
''')
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

# get db view market symbol server aggDepth sql
GET_VIEW_MARKET_SYMBOL_SERVER_AGGDEPTH_SQL = Template('''
    SELECT max(limit_price_step) as aggDepth
    FROM INFO_SYMBOL
    WHERE server IN $server and fSymbol='$fSymbol' and tSymbol='$tSymbol';
''')

# get db view market symbol server sql
GET_VIEW_MARKET_SYMBOL_SERVER_SQL = Template('''
    SELECT * FROM VIEW_MARKET_SYMBOL WHERE server IN $server;
''')

# get db view info symbol sql
GET_VIEW_INFO_SYMBOL_SERVER_SQL = Template('''
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
GET_ACCOUNT_BALANCE_HISTORY_SQL = '''
    SELECT * FROM ACCOUNT_BALANCE_HISTORY;
'''
# get db withdraw history sql
GET_ACCOUNT_WITHDRAW_HISTORY_SQL = '''
    SELECT * FROM ACCOUNT_WITHDRAW_HISTORY;
'''

# get db server info sql
GET_INFO_SERVER_SQL = '''
    SELECT * FROM INFO_SERVER;
'''
# get db symbol info sql
GET_INFO_SYMBOL_SQL = Template('''
    SELECT * FROM INFO_SYMBOL WHERE server IN $server;
''')
# get db withdraw info sql
GET_INFO_WITHDRAW_SQL = Template('''
    SELECT * FROM INFO_WITHDRAW WHERE server IN $server;
''')

# get db market depth sql
GET_MARKET_DEPTH_SQL = '''
    SELECT * FROM MARKET_DEPTH;
'''
# delete db market depth sql
DEL_MARKET_DEPTH_SQL = '''
    DELETE FROM MARKET_DEPTH;
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
GET_MARKET_TICKER_SQL = '''
    SELECT * FROM MARKET_TICKER;
'''
# delete db market ticker sql
DEL_MARKET_TICKER_SQL = '''
    DELETE FROM MARKET_TICKER;
'''

# get db judge signal ticker dis sql
GET_JUDGE_MARKET_TICKER_DIS_SQL = '''
    SELECT * FROM JUDGE_MARKET_TICKER_DIS;
'''
# delete db judge signal ticker dis sql
DEL_JUDGE_MARKET_TICKER_DIS_SQL = Template('''
    DELETE FROM JUDGE_MARKET_TICKER_DIS WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db judge signal ticker tra sql
GET_JUDGE_MARKET_TICKER_TRA_SQL = '''
    SELECT * FROM JUDGE_MARKET_TICKER_TRA;
'''
# delete db judge signal ticker tra sql
DEL_JUDGE_MARKET_TICKER_TRA_SQL = Template('''
    DELETE FROM JUDGE_MARKET_TICKER_TRA WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db judge signal ticker pair sql
GET_JUDGE_MARKET_TICKER_PAIR_SQL = '''
    SELECT * FROM JUDGE_MARKET_TICKER_PAIR;
'''
# delete db judge signal ticker pair sql
DEL_JUDGE_MARKET_TICKER_PAIR_SQL = Template('''
    DELETE FROM JUDGE_MARKET_TICKER_PAIR WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')

# get db signal trade dis sql
GET_SIGNAL_TRADE_DIS_SQL = Template('''
    SELECT * FROM SIGNAL_TRADE_DIS WHERE signal_id IN $signal_id;
''')
# delete db signal trade dis sql
DEL_SIGNAL_TRADE_DIS_SQL = Template('''
    DELETE FROM SIGNAL_TRADE_DIS WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db signal trade tra sql
GET_SIGNAL_TRADE_TRA_SQL = Template('''
    SELECT * FROM SIGNAL_TRADE_TRA WHERE signal_id IN $signal_id;
''')
# delete db signal trade tra sql
DEL_SIGNAL_TRADE_TRA_SQL = Template('''
    DELETE FROM SIGNAL_TRADE_TRA WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db signal trade pair sql
GET_SIGNAL_TRADE_PAIR_SQL = Template('''
    SELECT * FROM SIGNAL_TRADE_PAIR WHERE signal_id IN $signal_id;
''')
# delete db signal trade pair sql
DEL_SIGNAL_TRADE_PAIR_SQL = Template('''
    DELETE FROM SIGNAL_TRADE_PAIR WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')

# get db trade backtest history server orders sql
GET_TRADE_BACKTEST_HISTORY_SERVER_ORDER_SQL = Template('''
    SELECT * FROM TRADE_BACKTEST_HISTORY WHERE server in $server and order_id in $order_id;
''')
# get db trade order history sql
GET_TRADE_ORDER_HISTORY_SERVER_ORDER_SQL = Template('''
    SELECT * FROM TRADE_ORDER_HISTORY WHERE server in $server and order_id in $order_id;
''')

# get db trade backtest history sql
GET_TRADE_BACKTEST_HISTORY_SQL = '''
    SELECT * FROM TRADE_BACKTEST_HISTORY;
'''
# delete db trade backtest history sql
DEL_TRADE_BACKTEST_HISTORY_SQL = Template('''
    DELETE FROM TRADE_BACKTEST_HISTORY WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db trade order history sql
GET_TRADE_ORDER_HISTORY_SQL = '''
    SELECT * FROM TRADE_ORDER_HISTORY;
'''
# delete db trade order history sql
DEL_TRADE_ORDER_HISTORY_SQL = Template('''
    DELETE FROM TRADE_ORDER_HISTORY WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')

# get db statistic signal ticker dis sql
GET_STATISTIC_JUDGE_MARKET_TICKER_DIS_SQL = '''
    SELECT * FROM STATISTIC_JUDGE_MARKET_TICKER_DIS;
'''
# delete db statistic signal ticker dis sql
DEL_STATISTIC_JUDGE_MARKET_TICKER_DIS_SQL = Template('''
    DELETE FROM STATISTIC_JUDGE_MARKET_TICKER_DIS WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db statistic signal ticker tra sql
GET_STATISTIC_JUDGE_MARKET_TICKER_TRA_SQL = '''
    SELECT * FROM STATISTIC_JUDGE_MARKET_TICKER_TRA;
'''
# delete db statistic signal ticker tra sql
DEL_STATISTIC_JUDGE_MARKET_TICKER_TRA_SQL = Template('''
    DELETE FROM STATISTIC_JUDGE_MARKET_TICKER_TRA WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db statistic signal ticker pair sql
GET_STATISTIC_JUDGE_MARKET_TICKER_PAIR_SQL = '''
    SELECT * FROM STATISTIC_JUDGE_MARKET_TICKER_PAIR;
'''
# delete db statistic signal ticker pair sql
DEL_STATISTIC_JUDGE_MARKET_TICKER_PAIR_SQL = Template('''
    DELETE FROM STATISTIC_JUDGE_MARKET_TICKER_PAIR WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')

# get db statistic trade order history sql
GET_STATISTIC_TRADE_ORDER_HISTORY_SQL = '''
    SELECT * FROM STATISTIC_TRADE_ORDER_HISTORY;
'''
# delete db statistic trade order history sql
DEL_STATISTIC_TRADE_ORDER_HISTORY_SQL = Template('''
    DELETE FROM STATISTIC_TRADE_ORDER_HISTORY WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')
# get db statistic trade backtest history sql
GET_STATISTIC_TRADE_BACKTEST_HISTORY_SQL = '''
    SELECT * FROM STATISTIC_TRADE_BACKTEST_HISTORY;
'''
# delete db statistic trade backtest history sql
DEL_STATISTIC_TRADE_BACKTEST_HISTORY_SQL = Template('''
    DELETE FROM STATISTIC_TRADE_BACKTEST_HISTORY WHERE timeStamp < (strftime('%s', 'now')-$period)*1000;
''')

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
INSERT_MARKET_TICKER_SQL = '''
    INSERT OR REPLACE INTO MARKET_TICKER (server, timeStamp, fSymbol, tSymbol, bid_one_price, bid_one_size, ask_one_price, ask_one_size)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db judge signal ticker dis sql
INSERT_JUDGE_MARKET_TICKER_DIS_SQL = '''
    INSERT OR REPLACE INTO JUDGE_MARKET_TICKER_DIS (timeStamp, bid_server, ask_server, fSymbol, tSymbol, bid_price, bid_size, bid_price_base, ask_price, ask_size, ask_price_base, bid_fee, ask_fee, gain_base, gain_ratio)
    VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?)'''

# insert db judge signal ticker dis sql
INSERT_JUDGE_MARKET_TICKER_TRA_SQL = '''
    INSERT OR REPLACE INTO JUDGE_MARKET_TICKER_TRA (timeStamp, server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol, V3_fSymbol, V3_tSymbol, V1_bid_one_price, V1_bid_one_size, V1_bid_one_price_base, V1_ask_one_price, V1_ask_one_size, V1_ask_one_price_base, V2_bid_one_price, V2_bid_one_size, V2_bid_one_price_base, V2_ask_one_price, V2_ask_one_size, V2_ask_one_price_base, V3_bid_one_price, V3_bid_one_size, V3_bid_one_price_base, V3_ask_one_price, V3_ask_one_size, V3_ask_one_price_base, V1_fee, V2_fee, V3_fee, V1_one_price, V1_one_side, V1_one_size, V2_one_price, V2_one_side, V2_one_size, V3_one_price, V3_one_side, V3_one_size, gain_base, gain_ratio)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db judge signal ticker dis sql
INSERT_JUDGE_MARKET_TICKER_PAIR_SQL = '''
    INSERT OR REPLACE INTO JUDGE_MARKET_TICKER_PAIR (timeStamp, J1_server, J2_server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol, V3_fSymbol, V3_tSymbol, J1_V1_bid_one_price, J1_V1_bid_one_size, J1_V1_bid_one_price_base, J1_V1_ask_one_price, J1_V1_ask_one_size, J1_V1_ask_one_price_base, J1_V2_bid_one_price, J1_V2_bid_one_size, J1_V2_bid_one_price_base, J1_V2_ask_one_price, J1_V2_ask_one_size, J1_V2_ask_one_price_base, J1_V3_bid_one_price, J1_V3_bid_one_size, J1_V3_bid_one_price_base, J1_V3_ask_one_price, J1_V3_ask_one_size, J1_V3_ask_one_price_base, J2_V1_bid_one_price, J2_V1_bid_one_size, J2_V1_bid_one_price_base, J2_V1_ask_one_price, J2_V1_ask_one_size, J2_V1_ask_one_price_base, J2_V2_bid_one_price, J2_V2_bid_one_size, J2_V2_bid_one_price_base, J2_V2_ask_one_price, J2_V2_ask_one_size, J2_V2_ask_one_price_base, J2_V3_bid_one_price, J2_V3_bid_one_size, J2_V3_bid_one_price_base, J2_V3_ask_one_price, J2_V3_ask_one_size, J2_V3_ask_one_price_base, J1_V1_fee, J1_V2_fee, J1_V3_fee, J2_V1_fee, J2_V2_fee, J2_V3_fee, J1_V1_one_price, J1_V1_one_side, J1_V1_one_size, J2_V1_one_price, J2_V1_one_side, J2_V1_one_size, J1_V2_one_price, J1_V2_one_side, J1_V2_one_size, J2_V2_one_price, J2_V2_one_side, J2_V2_one_size, J1_V3_one_price, J1_V3_one_side, J1_V3_one_size, J2_V3_one_price, J2_V3_one_side, J2_V3_one_size, gain_base, gain_ratio)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db signal trade dis sql
INSERT_SIGNAL_TRADE_DIS = '''
    INSERT OR REPLACE INTO SIGNAL_TRADE_DIS(timeStamp, signal_id, type, bid_server, ask_server, fSymbol, tSymbol, forward_ratio, backward_ratio, base_start, base_gain, group_id, status_done, status_assets, status_gain)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db signal trade tra sql
INSERT_SIGNAL_TRADE_TRA = '''
    INSERT OR REPLACE INTO SIGNAL_TRADE_TRA(timeStamp, signal_id, type, server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol, V3_fSymbol, V3_tSymbol, forward_ratio, base_start, base_gain, group_id, status_done, status_assets, status_gain)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db signal trade pair sql
INSERT_SIGNAL_TRADE_PAIR = '''
    INSERT OR REPLACE INTO SIGNAL_TRADE_PAIR(timeStamp, signal_id, type, J1_server, J2_server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol, V3_fSymbol, V3_tSymbol, forward_ratio, base_start, base_gain, group_id, status_done, status_assets, status_gain)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db trade backtest history sql
INSERT_TRADE_BACKTEST_HISTORY_SQL = '''
    INSERT OR REPLACE INTO TRADE_BACKTEST_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee, group_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db trade order history sql
INSERT_TRADE_ORDER_HISTORY_SQL = '''
    INSERT OR REPLACE INTO TRADE_ORDER_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee, group_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# update db creat trade order history sql
UPDATE_CREAT_TRADE_ORDER_HISTORY_SQL = '''
    INSERT OR REPLACE INTO TRADE_ORDER_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# update db check trade order history sql
UPDATE_CHECK_TRADE_ORDER_HISTORY_SQL = '''
    INSERT OR REPLACE INTO TRADE_ORDER_HISTORY (server, timeStamp, order_id, status, type, fSymbol, tSymbol, ask_or_bid, ask_bid_price, ask_bid_size, filled_price, filled_size, fee)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# update db cancle trade order history sql
UPDATE_CANCLE_TRADE_ORDER_HISTORY_SQL = Template('''
    UPDATE TRADE_ORDER_HISTORY SET status = '$status' WHERE order_id='$order_id';
''')

# insert db statistic signal ticker dis sql
INSERT_STATISTIC_JUDGE_MARKET_TICKER_DIS_SQL = '''
    INSERT OR REPLACE INTO STATISTIC_JUDGE_MARKET_TICKER_DIS (timeStamp, bid_server, ask_server, fSymbol, tSymbol, timeStamp_start, timeStamp_end, timeStamp_times, timeStamp_period_times, timeStamp_period_longest, count_total, count_forward, count_backward, gain_base_max, gain_base_min, gain_base_mean, gain_base_std, gain_ratio_max, gain_ratio_min, gain_ratio_mean, gain_ratio_std, group_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db statistic signal ticker tra sql
INSERT_STATISTIC_JUDGE_MARKET_TICKER_TRA_SQL = '''
    INSERT OR REPLACE INTO STATISTIC_JUDGE_MARKET_TICKER_TRA (timeStamp, server, symbol_pair, timeStamp_start, timeStamp_end, timeStamp_times, timeStamp_period_times, timeStamp_period_longest, count_total, count_forward, count_backward, gain_base_max, gain_base_min, gain_base_mean, gain_base_std, gain_ratio_max, gain_ratio_min, gain_ratio_mean, gain_ratio_std, group_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db statistic signal ticker pair sql
INSERT_STATISTIC_JUDGE_MARKET_TICKER_PAIR_SQL = '''
    INSERT OR REPLACE INTO STATISTIC_JUDGE_MARKET_TICKER_PAIR (timeStamp, J1_server, J2_server, symbol_pair, timeStamp_start, timeStamp_end, timeStamp_times, timeStamp_period_times, timeStamp_period_longest, count_total, count_forward, count_backward, gain_base_max, gain_base_min, gain_base_mean, gain_base_std, gain_ratio_max, gain_ratio_min, gain_ratio_mean, gain_ratio_std, group_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db statistic trade backtest history sql
INSERT_STATISTIC_TRADE_BACKTEST_HISTORY = '''
    INSERT OR REPLACE INTO STATISTIC_TRADE_BACKTEST_HISTORY (timeStamp, signal_id, group_id, timeStamp_start, timeStamp_end, base_start, base_end, status_gain, status_gain_max, status_gain_min, status_gain_diff_max, status_gain_diff_min, status_gain_diff_std)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

# insert db statistic trade order history sql
INSERT_STATISTIC_TRADE_ORDER_HISTORY = '''
    INSERT OR REPLACE INTO STATISTIC_TRADE_ORDER_HISTORY (timeStamp, signal_id, group_id, timeStamp_start, timeStamp_end, base_start, base_end, status_gain, status_gain_max, status_gain_min, status_gain_diff_max, status_gain_diff_min, status_gain_diff_std)
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
    CREATE TABLE IF NOT EXISTS `STATISTIC_TRADE_ORDER_HISTORY` (
        `timeStamp` INTEGER,
        `signal_id` TEXT NOT NULL,
        `group_id` TEXT NOT NULL,
    	`timeStamp_start` INTEGER,
    	`timeStamp_end`	INTEGER,
        `base_start` REAL,
        `base_end` REAL,
        `base_gain` REAL,
        `status_gain` REAL,
        `status_gain_max` REAL,
        `status_gain_min` REAL,
        `status_gain_diff_max` REAL,
        `status_gain_diff_min` REAL,
        `status_gain_diff_std` REAL,
        PRIMARY KEY (signal_id, group_id)
    );
    CREATE TABLE IF NOT EXISTS `STATISTIC_TRADE_BACKTEST_HISTORY` (
        `timeStamp` INTEGER,
        `signal_id` TEXT NOT NULL,
        `group_id` TEXT NOT NULL,
    	`timeStamp_start` INTEGER,
    	`timeStamp_end`	INTEGER,
        `base_start` REAL,
        `base_end` REAL,
        `base_gain` REAL,
        `status_gain` REAL,
        `status_gain_max` REAL,
        `status_gain_min` REAL,
        `status_gain_diff_max` REAL,
        `status_gain_diff_min` REAL,
        `status_gain_diff_std` REAL,
        PRIMARY KEY (signal_id, group_id)
    );
    CREATE TABLE IF NOT EXISTS `STATISTIC_JUDGE_MARKET_TICKER_PAIR` (
    	`timeStamp`	INTEGER NOT NULL,
    	`J1_server`	TEXT NOT NULL,
    	`J2_server`	TEXT NOT NULL,
    	`symbol_pair`	TEXT NOT NULL,
    	`timeStamp_start`	INTEGER,
    	`timeStamp_end`	INTEGER,
    	`timeStamp_times`	REAL,
    	`timeStamp_period_times`	REAL,
    	`timeStamp_period_longest`	REAL,
    	`count_total`	REAL,
    	`count_forward`	REAL,
    	`count_backward`	REAL,
    	`gain_base_max`	REAL,
    	`gain_base_min`	REAL,
    	`gain_base_mean`	REAL,
    	`gain_base_std`	REAL,
    	`gain_ratio_max`	REAL,
    	`gain_ratio_min`	REAL,
    	`gain_ratio_mean`	REAL,
    	`gain_ratio_std`	REAL,
        `group_id`  TEXT NOT NULL,
        PRIMARY KEY (timeStamp, J1_server, J2_server, symbol_pair)
    );
    CREATE TABLE IF NOT EXISTS `STATISTIC_JUDGE_MARKET_TICKER_TRA` (
    	`timeStamp`	INTEGER NOT NULL,
    	`server`	TEXT NOT NULL,
    	`symbol_pair`	TEXT NOT NULL,
    	`timeStamp_start`	INTEGER,
    	`timeStamp_end`	INTEGER,
    	`timeStamp_times`	REAL,
    	`timeStamp_period_times`	REAL,
    	`timeStamp_period_longest`	REAL,
    	`count_total`	REAL,
    	`count_forward`	REAL,
    	`count_backward`	REAL,
    	`gain_base_max`	REAL,
    	`gain_base_min`	REAL,
    	`gain_base_mean`	REAL,
    	`gain_base_std`	REAL,
    	`gain_ratio_max`	REAL,
    	`gain_ratio_min`	REAL,
    	`gain_ratio_mean`	REAL,
    	`gain_ratio_std`	REAL,
        `group_id`  TEXT NOT NULL,
        PRIMARY KEY (timeStamp, server, symbol_pair)
    );
    CREATE TABLE IF NOT EXISTS `STATISTIC_JUDGE_MARKET_TICKER_DIS` (
    	`timeStamp`	INTEGER NOT NULL,
    	`bid_server`	TEXT NOT NULL,
    	`ask_server`	TEXT NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`timeStamp_start`	INTEGER,
    	`timeStamp_end`	INTEGER,
    	`timeStamp_times`	REAL,
    	`timeStamp_period_times`	REAL,
    	`timeStamp_period_longest`	REAL,
    	`count_total`	REAL,
    	`count_forward`	REAL,
    	`count_backward`	REAL,
    	`gain_base_max`	REAL,
    	`gain_base_min`	REAL,
    	`gain_base_mean`	REAL,
    	`gain_base_std`	REAL,
    	`gain_ratio_max`	REAL,
    	`gain_ratio_min`	REAL,
    	`gain_ratio_mean`	REAL,
    	`gain_ratio_std`	REAL,
        `group_id`  TEXT NOT NULL,
        PRIMARY KEY (timeStamp, bid_server, ask_server, fSymbol, tSymbol)
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
    	`fee`	REAL,
        `signal_id`  TEXT,
        `group_id`  TEXT,
        PRIMARY KEY (server, order_id)
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
        `signal_id`  TEXT,
        `group_id`  TEXT,
        PRIMARY KEY (server, order_id)
    );
    CREATE TABLE IF NOT EXISTS `SIGNAL_TRADE_PAIR` (
        `timeStamp` INTEGER NOT NULL,
        `signal_id` TEXT NOT NULL,
        `type` TEXT NOT NULL,
        `J1_server` TEXT NOT NULL,
        `J2_server` TEXT NOT NULL,
        `V1_fSymbol` TEXT NOT NULL,
        `V1_tSymbol` TEXT NOT NULL,
        `V2_fSymbol` TEXT NOT NULL,
        `V2_tSymbol` TEXT NOT NULL,
        `V3_fSymbol` TEXT NOT NULL,
        `V3_tSymbol` TEXT NOT NULL,
        `forward_ratio` REAL NOT NULL,
        `base_start` REAL NOT NULL,
        `base_gain` REAL NOT NULL,
        `group_id` TEXT NOT NULL,
        `status_done` TEXT,
        `status_assets` TEXT,
        `status_gain` REAL,
        PRIMARY KEY (timeStamp, signal_id)
    );
    CREATE TABLE IF NOT EXISTS `SIGNAL_TRADE_TRA` (
        `timeStamp` INTEGER NOT NULL,
        `signal_id` TEXT NOT NULL,
        `type` TEXT NOT NULL,
        `server` TEXT NOT NULL,
        `V1_fSymbol` TEXT NOT NULL,
        `V1_tSymbol` TEXT NOT NULL,
        `V2_fSymbol` TEXT NOT NULL,
        `V2_tSymbol` TEXT NOT NULL,
        `V3_fSymbol` TEXT NOT NULL,
        `V3_tSymbol` TEXT NOT NULL,
        `forward_ratio` REAL NOT NULL,
        `base_start` REAL NOT NULL,
        `base_gain` REAL NOT NULL,
        `group_id` TEXT NOT NULL,
        `status_done` TEXT,
        `status_assets` TEXT,
        `status_gain` REAL,
        PRIMARY KEY (timeStamp, signal_id)
    );
    CREATE TABLE IF NOT EXISTS `SIGNAL_TRADE_DIS` (
        `timeStamp` INTEGER NOT NULL,
        `signal_id` TEXT NOT NULL,
        `type` TEXT NOT NULL,
        `bid_server` TEXT NOT NULL,
        `ask_server` TEXT NOT NULL,
        `fSymbol` TEXT NOT NULL,
        `tSymbol` TEXT NOT NULL,
        `forward_ratio` REAL NOT NULL,
        `backward_ratio` REAL NOT NULL,
        `base_start` REAL NOT NULL,
        `base_gain` REAL NOT NULL,
        `group_id` TEXT NOT NULL,
        `status_done` TEXT,
        `status_assets` TEXT,
        `status_gain` REAL,
        PRIMARY KEY (timeStamp, signal_id)
    );
    CREATE TABLE IF NOT EXISTS `JUDGE_MARKET_TICKER_PAIR` (
    	`timeStamp`	INTEGER NOT NULL,
        `J1_server`	TEXT NOT NULL,
        `J2_server`	TEXT NOT NULL,
        `V1_fSymbol`	TEXT NOT NULL,
        `V1_tSymbol`	TEXT NOT NULL,
        `V2_fSymbol`	TEXT NOT NULL,
        `V2_tSymbol`	TEXT NOT NULL,
        `V3_fSymbol`	TEXT NOT NULL,
        `V3_tSymbol`	TEXT NOT NULL,
        `J1_V1_bid_one_price`	REAL,
        `J1_V1_bid_one_size`	REAL,
        `J1_V1_bid_one_price_base`	REAL,
        `J1_V1_ask_one_price`	REAL,
        `J1_V1_ask_one_size`	REAL,
        `J1_V1_ask_one_price_base`	REAL,
        `J1_V2_bid_one_price`	REAL,
        `J1_V2_bid_one_size`	REAL,
        `J1_V2_bid_one_price_base`	REAL,
        `J1_V2_ask_one_price`	REAL,
        `J1_V2_ask_one_size`	REAL,
        `J1_V2_ask_one_price_base`	REAL,
        `J1_V3_bid_one_price`	REAL,
        `J1_V3_bid_one_size`	REAL,
        `J1_V3_bid_one_price_base`	REAL,
        `J1_V3_ask_one_price`	REAL,
        `J1_V3_ask_one_size`	REAL,
        `J1_V3_ask_one_price_base`	REAL,
        `J2_V1_bid_one_price`	REAL,
        `J2_V1_bid_one_size`	REAL,
        `J2_V1_bid_one_price_base`	REAL,
        `J2_V1_ask_one_price`	REAL,
        `J2_V1_ask_one_size`	REAL,
        `J2_V1_ask_one_price_base`	REAL,
        `J2_V2_bid_one_price`	REAL,
        `J2_V2_bid_one_size`	REAL,
        `J2_V2_bid_one_price_base`	REAL,
        `J2_V2_ask_one_price`	REAL,
        `J2_V2_ask_one_size`	REAL,
        `J2_V2_ask_one_price_base`	REAL,
        `J2_V3_bid_one_price`	REAL,
        `J2_V3_bid_one_size`	REAL,
        `J2_V3_bid_one_price_base`	REAL,
        `J2_V3_ask_one_price`	REAL,
        `J2_V3_ask_one_size`	REAL,
        `J2_V3_ask_one_price_base`	REAL,
        `J1_V1_fee`	REAL,
        `J1_V2_fee`	REAL,
        `J1_V3_fee`	REAL,
        `J2_V1_fee`	REAL,
        `J2_V2_fee`	REAL,
        `J2_V3_fee`	REAL,
        `J1_V1_one_price`	REAL,
        `J1_V1_one_side`	TEXT,
        `J1_V1_one_size`	REAL,
        `J2_V1_one_price`	REAL,
        `J2_V1_one_side`	TEXT,
        `J2_V1_one_size`	REAL,
        `J1_V2_one_price`	REAL,
        `J1_V2_one_side`	TEXT,
        `J1_V2_one_size`	REAL,
        `J2_V2_one_price`	REAL,
        `J2_V2_one_side`	TEXT,
        `J2_V2_one_size`	REAL,
        `J1_V3_one_price`	REAL,
        `J1_V3_one_side`	TEXT,
        `J1_V3_one_size`	REAL,
        `J2_V3_one_price`	REAL,
        `J2_V3_one_side`	TEXT,
        `J2_V3_one_size`	REAL,
        `gain_base`	REAL,
        `gain_ratio`	REAL,
        PRIMARY KEY (timeStamp, J1_server, J2_server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol, V3_fSymbol, V3_tSymbol)
    );
    CREATE TABLE IF NOT EXISTS `JUDGE_MARKET_TICKER_TRA` (
    	`timeStamp`	INTEGER NOT NULL,
        `server`	TEXT NOT NULL,
    	`V1_fSymbol`	TEXT NOT NULL,
    	`V1_tSymbol`	TEXT NOT NULL,
    	`V2_fSymbol`	TEXT NOT NULL,
    	`V2_tSymbol`	TEXT NOT NULL,
    	`V3_fSymbol`	TEXT NOT NULL,
    	`V3_tSymbol`	TEXT NOT NULL,
    	`V1_bid_one_price`	REAL,
    	`V1_bid_one_size`	REAL,
    	`V1_bid_one_price_base`	REAL,
    	`V1_ask_one_price`	REAL,
    	`V1_ask_one_size`	REAL,
    	`V1_ask_one_price_base`	REAL,
    	`V2_bid_one_price`	REAL,
    	`V2_bid_one_size`	REAL,
    	`V2_bid_one_price_base`	REAL,
    	`V2_ask_one_price`	REAL,
    	`V2_ask_one_size`	REAL,
    	`V2_ask_one_price_base`	REAL,
    	`V3_bid_one_price`	REAL,
    	`V3_bid_one_size`	REAL,
    	`V3_bid_one_price_base`	REAL,
    	`V3_ask_one_price`	REAL,
    	`V3_ask_one_size`	REAL,
    	`V3_ask_one_price_base`	REAL,
    	`V1_fee`	REAL,
    	`V2_fee`	REAL,
    	`V3_fee`	REAL,
    	`V1_one_price`	REAL,
    	`V1_one_side`	TEXT,
    	`V1_one_size`	REAL,
    	`V2_one_price`	REAL,
    	`V2_one_side`	TEXT,
    	`V2_one_size`	REAL,
    	`V3_one_price`	REAL,
    	`V3_one_side`	TEXT,
    	`V3_one_size`	REAL,
    	`gain_base`	REAL,
    	`gain_ratio`	REAL,
        PRIMARY KEY (timeStamp, server, V1_fSymbol, V1_tSymbol, V2_fSymbol, V2_tSymbol, V3_fSymbol, V3_tSymbol)
    );
    CREATE TABLE IF NOT EXISTS `JUDGE_MARKET_TICKER_DIS` (
    	`timeStamp`	INTEGER NOT NULL,
        `bid_server`	TEXT NOT NULL,
        `ask_server`	TEXT NOT NULL,
    	`fSymbol`	TEXT NOT NULL,
    	`tSymbol`	TEXT NOT NULL,
    	`bid_price`	REAL,
    	`bid_size`	REAL,
    	`bid_price_base`	REAL,
    	`ask_price`	REAL,
    	`ask_size`	REAL,
    	`ask_price_base`	REAL,
    	`bid_fee`	REAL,
    	`ask_fee`	REAL,
    	`gain_base`	REAL,
    	`gain_ratio`	REAL,
        PRIMARY KEY (timeStamp, bid_server, ask_server, fSymbol, tSymbol)
    );
    CREATE TABLE IF NOT EXISTS `MARKET_TICKER` (
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
            SELECT DISTINCT *
            FROM INFO_SYMBOL
            WHERE fSymbol NOT IN $excludeCoins AND tSymbol NOT IN $excludeCoins;
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
            WHERE B2.server IS NULL;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_KLINE_CURRENT
    	AS
    			SELECT M1.*, M1.close*M2.close as price_base, M1.close*M1.volume*M2.close as price_volume_base
    			FROM MARKET_KLINE M1
    			JOIN MARKET_KLINE M2 ON M1.server = M2.server AND M1.timeStamp = M2.timeStamp AND M1.tSymbol = M2.fSymbol AND M1.tSymbol<>'$baseCoin' AND M2.tSymbol ='$baseCoin'
    		UNION
    			SELECT M1.*, M1.close as price_base, M1.close*M1.volume as price_volume_base
    			FROM MARKET_KLINE M1
    			WHERE M1.tSymbol = '$baseCoin';
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_SYMBOL
    	AS
            SELECT J2.*
            FROM(
                SELECT DISTINCT V1.server, V1.fSymbol, V1.tSymbol
                FROM(
						SELECT DISTINCT server, fSymbol, tSymbol
						FROM VIEW_INFO_SYMBOL M1
					EXCEPT
						SELECT DISTINCT server, fSymbol, tSymbol
						FROM VIEW_MARKET_KLINE_CURRENT
						WHERE price_volume_base < $basePriceVolume
				) V1
				LEFT JOIN(
						SELECT DISTINCT server, fSymbol, tSymbol
						FROM VIEW_INFO_SYMBOL M1
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
        	SELECT V1.*, V1.bid_one_price*(V2.bid_one_price+V2.ask_one_price)/2 as bid_one_price_base, V1.ask_one_price*(V2.bid_one_price+V2.ask_one_price)/2 as ask_one_price_base
        	FROM(
        		SELECT M1.*
        		FROM MARKET_TICKER M1
        		LEFT JOIN MARKET_TICKER M2 ON M1.server = M2.server AND M1.fSymbol = M2.fSymbol AND M1.tSymbol = M2.tSymbol AND M1.timeStamp < M2.timeStamp
        		WHERE M2.server IS NULL
        	) V1
        	JOIN(
        		SELECT M1.*
        		FROM MARKET_TICKER M1
        		LEFT JOIN MARKET_TICKER M2 ON M1.server = M2.server AND M1.fSymbol = M2.fSymbol AND M1.tSymbol = M2.tSymbol AND M1.timeStamp < M2.timeStamp
        		WHERE M2.server IS NULL
        	) V2 ON V1.server = V2.server AND V1.tSymbol = V2.fSymbol AND V1.tSymbol<>'$baseCoin' AND V2.tSymbol ='$baseCoin'
        UNION
        	SELECT V3.*, V3.bid_one_price as bid_one_price_base, V3.ask_one_price as ask_one_price_base
        	FROM(
        		SELECT M1.*
        		FROM MARKET_TICKER M1
        		LEFT JOIN MARKET_TICKER M2 ON M1.server = M2.server AND M1.fSymbol = M2.fSymbol AND M1.tSymbol = M2.tSymbol AND M1.timeStamp < M2.timeStamp
        		WHERE M2.server IS NULL AND M1.tSymbol='$baseCoin'
        	) V3;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_TICKER_CURRENT_DIS
    	AS
    		SELECT V1.timeStamp, V1.server as bid_server, V2.server as ask_server, V1.fSymbol, V1.tSymbol,
                V1.bid_one_price as bid_price, V1.bid_one_size as bid_size, V1.bid_one_price_base as bid_price_base,
                V2.ask_one_price as ask_price, V2.ask_one_size as ask_size, V2.ask_one_price_base as ask_price_base
    		FROM VIEW_MARKET_TICKER_CURRENT V1
    		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server <> V2.server AND V1.fSymbol = V2.fSymbol AND V1.tSymbol = V2.tSymbol
    		WHERE abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_TICKER_CURRENT_TRA
    	AS
        	SELECT V1.timeStamp, V1.server,
                V1.fSymbol as V1_fSymbol, V1.tSymbol as V1_tSymbol,
                V2.fSymbol as V2_fSymbol, V2.tSymbol as V2_tSymbol,
                V3.fSymbol as V3_fSymbol, V3.tSymbol as V3_tSymbol,
        		V1.bid_one_price as V1_bid_one_price, V1.bid_one_size as V1_bid_one_size, V1.bid_one_price_base as V1_bid_one_price_base,
        		V1.ask_one_price as V1_ask_one_price, V1.ask_one_size as V1_ask_one_size, V1.ask_one_price_base as V1_ask_one_price_base,
        		V2.bid_one_price as V2_bid_one_price, V2.bid_one_size as V2_bid_one_size, V2.bid_one_price_base as V2_bid_one_price_base,
        		V2.ask_one_price as V2_ask_one_price, V2.ask_one_size as V2_ask_one_size, V2.ask_one_price_base as V2_ask_one_price_base,
        		V3.bid_one_price as V3_bid_one_price, V3.bid_one_size as V3_bid_one_size, V3.bid_one_price_base as V3_bid_one_price_base,
        		V3.ask_one_price as V3_ask_one_price, V3.ask_one_size as V3_ask_one_size, V3.ask_one_price_base as V3_ask_one_price_base
        	FROM VIEW_MARKET_TICKER_CURRENT V1
        	LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol <> V2.fSymbol AND V1.tSymbol = V2.tSymbol
        	LEFT JOIN VIEW_MARKET_TICKER_CURRENT V3 ON V2.server = V3.server AND V1.fSymbol = V3.fSymbol AND V2.fSymbol = V3.tSymbol
            WHERE V2.server IS NOT NULL AND abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V3.server IS NOT NULL AND abs(V2.timeStamp - V3.timeStamp) < 1000*$basePriceTimeout
        UNION
        	SELECT V1.timeStamp, V1.server,
                V1.fSymbol as V1_fSymbol, V1.tSymbol as V1_tSymbol,
                V2.fSymbol as V2_fSymbol, V2.tSymbol as V2_tSymbol,
                V3.fSymbol as V3_fSymbol, V3.tSymbol as V3_tSymbol,
        		V1.bid_one_price as V1_bid_one_price, V1.bid_one_size as V1_bid_one_size, V1.bid_one_price_base as V1_bid_one_price_base,
        		V1.ask_one_price as V1_ask_one_price, V1.ask_one_size as V1_ask_one_size, V1.ask_one_price_base as V1_ask_one_price_base,
        		V2.bid_one_price as V2_bid_one_price, V2.bid_one_size as V2_bid_one_size, V2.bid_one_price_base as V2_bid_one_price_base,
        		V2.ask_one_price as V2_ask_one_price, V2.ask_one_size as V2_ask_one_size, V2.ask_one_price_base as V2_ask_one_price_base,
        		V3.bid_one_price as V3_bid_one_price, V3.bid_one_size as V3_bid_one_size, V3.bid_one_price_base as V3_bid_one_price_base,
        		V3.ask_one_price as V3_ask_one_price, V3.ask_one_size as V3_ask_one_size, V3.ask_one_price_base as V3_ask_one_price_base
        	FROM VIEW_MARKET_TICKER_CURRENT V1
        	LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol <> V2.fSymbol AND V1.tSymbol = V2.tSymbol
        	LEFT JOIN VIEW_MARKET_TICKER_CURRENT V3 ON V2.server = V3.server AND V1.fSymbol = V3.tSymbol AND V2.fSymbol = V3.fSymbol
            WHERE V2.server IS NOT NULL AND abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V3.server IS NOT NULL AND abs(V2.timeStamp - V3.timeStamp) < 1000*$basePriceTimeout;
    CREATE VIEW IF NOT EXISTS VIEW_MARKET_TICKER_CURRENT_PAIR
    	AS
            SELECT J1.timeStamp, J1.server as J1_server, J2.server as J2_server,
                J1.V1_fSymbol as V1_fSymbol, J1.V1_tSymbol as V1_tSymbol,
                J1.V2_fSymbol as V2_fSymbol, J1.V2_tSymbol as V2_tSymbol,
                J1.V3_fSymbol as V3_fSymbol, J1.V3_tSymbol as V3_tSymbol,
            	J1.V1_bid_one_price as J1_V1_bid_one_price, J1.V1_bid_one_size as J1_V1_bid_one_size, J1.V1_bid_one_price_base as J1_V1_bid_one_price_base,
            	J1.V1_ask_one_price as J1_V1_ask_one_price, J1.V1_ask_one_size as J1_V1_ask_one_size, J1.V1_ask_one_price_base as J1_V1_ask_one_price_base,
            	J1.V2_bid_one_price as J1_V2_bid_one_price, J1.V2_bid_one_size as J1_V2_bid_one_size, J1.V2_bid_one_price_base as J1_V2_bid_one_price_base,
            	J1.V2_ask_one_price as J1_V2_ask_one_price, J1.V2_ask_one_size as J1_V2_ask_one_size, J1.V2_ask_one_price_base as J1_V2_ask_one_price_base,
            	J1.V3_bid_one_price as J1_V3_bid_one_price, J1.V3_bid_one_size as J1_V3_bid_one_size, J1.V3_bid_one_price_base as J1_V3_bid_one_price_base,
            	J1.V3_ask_one_price as J1_V3_ask_one_price, J1.V3_ask_one_size as J1_V3_ask_one_size, J1.V3_ask_one_price_base as J1_V3_ask_one_price_base,
            	J2.V1_bid_one_price as J2_V1_bid_one_price, J2.V1_bid_one_size as J2_V1_bid_one_size, J2.V1_bid_one_price_base as J2_V1_bid_one_price_base,
            	J2.V1_ask_one_price as J2_V1_ask_one_price, J2.V1_ask_one_size as J2_V1_ask_one_size, J2.V1_ask_one_price_base as J2_V1_ask_one_price_base,
            	J2.V2_bid_one_price as J2_V2_bid_one_price, J2.V2_bid_one_size as J2_V2_bid_one_size, J2.V2_bid_one_price_base as J2_V2_bid_one_price_base,
            	J2.V2_ask_one_price as J2_V2_ask_one_price, J2.V2_ask_one_size as J2_V2_ask_one_size, J2.V2_ask_one_price_base as J2_V2_ask_one_price_base,
            	J2.V3_bid_one_price as J2_V3_bid_one_price, J2.V3_bid_one_size as J2_V3_bid_one_size, J2.V3_bid_one_price_base as J2_V3_bid_one_price_base,
            	J2.V3_ask_one_price as J2_V3_ask_one_price, J2.V3_ask_one_size as J2_V3_ask_one_size, J2.V3_ask_one_price_base as J2_V3_ask_one_price_base
            FROM (
            		SELECT V1.timeStamp, V1.server,
                        V1.fSymbol as V1_fSymbol, V1.tSymbol as V1_tSymbol,
                        V2.fSymbol as V2_fSymbol, V2.tSymbol as V2_tSymbol,
                        V3.fSymbol as V3_fSymbol, V3.tSymbol as V3_tSymbol,
        				V1.bid_one_price as V1_bid_one_price, V1.bid_one_size as V1_bid_one_size, V1.bid_one_price_base as V1_bid_one_price_base,
        				V1.ask_one_price as V1_ask_one_price, V1.ask_one_size as V1_ask_one_size, V1.ask_one_price_base as V1_ask_one_price_base,
        				V2.bid_one_price as V2_bid_one_price, V2.bid_one_size as V2_bid_one_size, V2.bid_one_price_base as V2_bid_one_price_base,
        				V2.ask_one_price as V2_ask_one_price, V2.ask_one_size as V2_ask_one_size, V2.ask_one_price_base as V2_ask_one_price_base,
        				V3.bid_one_price as V3_bid_one_price, V3.bid_one_size as V3_bid_one_size, V3.bid_one_price_base as V3_bid_one_price_base,
        				V3.ask_one_price as V3_ask_one_price, V3.ask_one_size as V3_ask_one_size, V3.ask_one_price_base as V3_ask_one_price_base
            		FROM VIEW_MARKET_TICKER_CURRENT V1
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol <> V2.fSymbol AND V1.tSymbol = V2.tSymbol
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V3 ON V2.server = V3.server AND V1.fSymbol = V3.fSymbol AND V2.fSymbol = V3.tSymbol
                    WHERE V2.server IS NOT NULL AND abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V3.server IS NOT NULL AND abs(V2.timeStamp - V3.timeStamp) < 1000*$basePriceTimeout
        		UNION
        			SELECT V1.timeStamp, V1.server,
                        V1.fSymbol as V1_fSymbol, V1.tSymbol as V1_tSymbol,
                        V2.fSymbol as V2_fSymbol, V2.tSymbol as V2_tSymbol,
                        V3.fSymbol as V3_fSymbol, V3.tSymbol as V3_tSymbol,
        				V1.bid_one_price as V1_bid_one_price, V1.bid_one_size as V1_bid_one_size, V1.bid_one_price_base as V1_bid_one_price_base,
        				V1.ask_one_price as V1_ask_one_price, V1.ask_one_size as V1_ask_one_size, V1.ask_one_price_base as V1_ask_one_price_base,
        				V2.bid_one_price as V2_bid_one_price, V2.bid_one_size as V2_bid_one_size, V2.bid_one_price_base as V2_bid_one_price_base,
        				V2.ask_one_price as V2_ask_one_price, V2.ask_one_size as V2_ask_one_size, V2.ask_one_price_base as V2_ask_one_price_base,
        				V3.bid_one_price as V3_bid_one_price, V3.bid_one_size as V3_bid_one_size, V3.bid_one_price_base as V3_bid_one_price_base,
        				V3.ask_one_price as V3_ask_one_price, V3.ask_one_size as V3_ask_one_size, V3.ask_one_price_base as V3_ask_one_price_base
            		FROM VIEW_MARKET_TICKER_CURRENT V1
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol <> V2.fSymbol AND V1.tSymbol = V2.tSymbol
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V3 ON V2.server = V3.server AND V1.fSymbol = V3.tSymbol AND V2.fSymbol = V3.fSymbol
                    WHERE V2.server IS NOT NULL AND abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V3.server IS NOT NULL AND abs(V2.timeStamp - V3.timeStamp) < 1000*$basePriceTimeout
            	) J1
            	LEFT JOIN (
            		SELECT V1.timeStamp, V1.server,
                        V1.fSymbol as V1_fSymbol, V1.tSymbol as V1_tSymbol,
                        V2.fSymbol as V2_fSymbol, V2.tSymbol as V2_tSymbol,
                        V3.fSymbol as V3_fSymbol, V3.tSymbol as V3_tSymbol,
        				V1.bid_one_price as V1_bid_one_price, V1.bid_one_size as V1_bid_one_size, V1.bid_one_price_base as V1_bid_one_price_base,
        				V1.ask_one_price as V1_ask_one_price, V1.ask_one_size as V1_ask_one_size, V1.ask_one_price_base as V1_ask_one_price_base,
        				V2.bid_one_price as V2_bid_one_price, V2.bid_one_size as V2_bid_one_size, V2.bid_one_price_base as V2_bid_one_price_base,
        				V2.ask_one_price as V2_ask_one_price, V2.ask_one_size as V2_ask_one_size, V2.ask_one_price_base as V2_ask_one_price_base,
        				V3.bid_one_price as V3_bid_one_price, V3.bid_one_size as V3_bid_one_size, V3.bid_one_price_base as V3_bid_one_price_base,
        				V3.ask_one_price as V3_ask_one_price, V3.ask_one_size as V3_ask_one_size, V3.ask_one_price_base as V3_ask_one_price_base
            		FROM VIEW_MARKET_TICKER_CURRENT V1
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol <> V2.fSymbol AND V1.tSymbol = V2.tSymbol
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V3 ON V2.server = V3.server AND V1.fSymbol = V3.fSymbol AND V2.fSymbol = V3.tSymbol
                    WHERE V2.server IS NOT NULL AND abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V3.server IS NOT NULL AND abs(V2.timeStamp - V3.timeStamp) < 1000*$basePriceTimeout
        		UNION
        			SELECT V1.timeStamp, V1.server,
                        V1.fSymbol as V1_fSymbol, V1.tSymbol as V1_tSymbol,
                        V2.fSymbol as V2_fSymbol, V2.tSymbol as V2_tSymbol,
                        V3.fSymbol as V3_fSymbol, V3.tSymbol as V3_tSymbol,
        				V1.bid_one_price as V1_bid_one_price, V1.bid_one_size as V1_bid_one_size, V1.bid_one_price_base as V1_bid_one_price_base,
        				V1.ask_one_price as V1_ask_one_price, V1.ask_one_size as V1_ask_one_size, V1.ask_one_price_base as V1_ask_one_price_base,
        				V2.bid_one_price as V2_bid_one_price, V2.bid_one_size as V2_bid_one_size, V2.bid_one_price_base as V2_bid_one_price_base,
        				V2.ask_one_price as V2_ask_one_price, V2.ask_one_size as V2_ask_one_size, V2.ask_one_price_base as V2_ask_one_price_base,
        				V3.bid_one_price as V3_bid_one_price, V3.bid_one_size as V3_bid_one_size, V3.bid_one_price_base as V3_bid_one_price_base,
        				V3.ask_one_price as V3_ask_one_price, V3.ask_one_size as V3_ask_one_size, V3.ask_one_price_base as V3_ask_one_price_base
            		FROM VIEW_MARKET_TICKER_CURRENT V1
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server = V2.server AND V1.fSymbol <> V2.fSymbol AND V1.tSymbol = V2.tSymbol
            		LEFT JOIN VIEW_MARKET_TICKER_CURRENT V3 ON V2.server = V3.server AND V1.fSymbol = V3.tSymbol AND V2.fSymbol = V3.fSymbol
                    WHERE V2.server IS NOT NULL AND abs(V1.timeStamp - V2.timeStamp) < 1000*$basePriceTimeout AND V3.server IS NOT NULL AND abs(V2.timeStamp - V3.timeStamp) < 1000*$basePriceTimeout
            	) J2 ON J1.server<>J2.server AND J1.V1_fSymbol = J2.V1_fSymbol AND J1.V1_tSymbol = J2.V1_tSymbol AND J1.V2_fSymbol = J2.V2_fSymbol AND J1.V2_tSymbol = J2.V2_tSymbol AND J1.V3_fSymbol = J2.V3_fSymbol AND J1.V3_tSymbol = J2.V3_tSymbol
            	WHERE J2.server IS NOT NULL AND abs(J1.timeStamp - J2.timeStamp) < 1000*$basePriceTimeout;
    CREATE VIEW IF NOT EXISTS VIEW_JUDGE_MARKET_TICKER_DIS_CURRENT
        AS
			SELECT *
			FROM JUDGE_MARKET_TICKER_DIS
			WHERE timeStamp > (strftime('%s', 'now')-$baseJudgeTimeout)*1000;
    CREATE VIEW IF NOT EXISTS VIEW_JUDGE_MARKET_TICKER_TRA_CURRENT
        AS
			SELECT *
			FROM JUDGE_MARKET_TICKER_TRA
			WHERE timeStamp > (strftime('%s', 'now')-$baseJudgeTimeout)*1000;
    CREATE VIEW IF NOT EXISTS VIEW_JUDGE_MARKET_TICKER_PAIR_CURRENT
        AS
			SELECT *
			FROM JUDGE_MARKET_TICKER_PAIR
			WHERE timeStamp > (strftime('%s', 'now')-$baseJudgeTimeout)*1000;
    CREATE VIEW IF NOT EXISTS VIEW_STATISTIC_JUDGE_MARKET_TICKER_DIS_CURRENT
        AS
			SELECT *
			FROM STATISTIC_JUDGE_MARKET_TICKER_DIS
			WHERE timeStamp > (strftime('%s', 'now')-$baseStatisticJudgeTimeout)*1000;
    CREATE VIEW IF NOT EXISTS VIEW_STATISTIC_JUDGE_MARKET_TICKER_TRA_CURRENT
        AS
			SELECT *
			FROM STATISTIC_JUDGE_MARKET_TICKER_TRA
			WHERE timeStamp > (strftime('%s', 'now')-$baseStatisticJudgeTimeout)*1000;
    CREATE VIEW IF NOT EXISTS VIEW_STATISTIC_JUDGE_MARKET_TICKER_PAIR_CURRENT
        AS
			SELECT *
			FROM STATISTIC_JUDGE_MARKET_TICKER_PAIR
			WHERE timeStamp > (strftime('%s', 'now')-$baseStatisticJudgeTimeout)*1000;
    CREATE VIEW IF NOT EXISTS VIEW_SIGNAL_TRADE_CURRENT
        AS
				SELECT timeStamp, signal_id, group_id, base_start, base_gain, status_assets, status_gain
				FROM SIGNAL_TRADE_DIS
				WHERE timeStamp > (strftime('%s', 'now')-$baseStatisticTradeTimeout)*1000
			UNION
				SELECT timeStamp, signal_id, group_id, base_start, base_gain, status_assets, status_gain
				FROM SIGNAL_TRADE_TRA
				WHERE timeStamp > (strftime('%s', 'now')-$baseStatisticTradeTimeout)*1000
			UNION
				SELECT timeStamp, signal_id, group_id, base_start, base_gain, status_assets, status_gain
				FROM SIGNAL_TRADE_PAIR
				WHERE timeStamp > (strftime('%s', 'now')-$baseStatisticTradeTimeout)*1000;
    COMMIT;
''')
