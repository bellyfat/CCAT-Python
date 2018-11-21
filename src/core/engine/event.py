# -*- coding: utf-8 -*-

from string import Template

# listen event list
LISTEN_ACCOUNT_BALANCE_EVENT = Template("""
{
    "type": "LISTEN_ACCOUNT_BALANCE_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": ["$server"],
        "remark": "account balance history, run as need"
    }
}
""")

LISTEN_ACCOUNT_WITHDRAW_EVENT = Template("""
{
    "type": "LISTEN_ACCOUNT_WITHDRAW_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": ["$server", "$asset"],
        "remark": "account withdraw history, run as need"
    }
}
""")

LISTEN_MARKET_KLINE_EVENT = Template("""
{
    "type": "LISTEN_MARKET_KLINE_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": ["$server", "$fSymbol", "$tSymbol", "$interval", "$start", "$end"],
        "remark": "symbols filter, run first and frequent"
    }
}
""")

LISTEN_MARKET_TICKER_EVENT = Template("""
{
    "type": "LISTEN_MARKET_TICKER_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": ["$server", "$fSymbol", "$tSymbol"],
        "remark": "ccat filter, run as frequent as possible"
    }
}
""")

LISTEN_MARKET_DEPTH_EVENT = Template("""
{
    "type": "LISTEN_MARKET_DEPTH_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": ["$server","$fSymbol", "$tSymbol", "$limit"],
        "remark": "symbols info, run as need"
    }
}
""")

# judge event list
JUDGE_MARKET_KLINE_EVENT = Template("""
{
    "type": "JUDGE_MARKET_KLINE_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

JUDGE_MARKET_TICKER_EVENT = Template("""
{
    "type": "JUDGE_MARKET_TICKER_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

# backtest event list
BACKTEST_MARKET_KLINE_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

BACKTEST_MARKET_TICKER_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

# order event list
ORDER_MARKET_KLINE_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

ORDER_MARKET_TICKER_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

# statistic event list
STATISTIC_BACKTEST_EVENT = Template("""
{
    "type": "STATISTIC_BACKTEST_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")

STATISTIC_ORDER_EVENT = Template("""
{
    "type": "STATISTIC_ORDER_EVENT",
    "dict": {
        "timeStamp": $timeStamp,
        "args": [],
        "remark": ""
    }
}
""")
