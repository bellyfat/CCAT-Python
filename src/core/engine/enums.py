# -*- coding: utf-8 -*-

from src.core.config import Config
from src.core.util.helper import MyTemplate


# event priority
LOW_PRIORITY_ENVENT = "low" # p.start()
MEDIUM_PRIORITY_ENVENT = "medium" # p.start()
HIGH_PRIORITY_ENVENT = "high" # p.join()运行

LOW_PRIORITY_ENVENT_TIMEOUT = float(Config()._event["lowTimeout"])
MEDIUM_PRIORITY_ENVENT_TIMEOUT = float(Config()._event["mediumTimeout"])
HIGH_PRIORITY_ENVENT_TIMEOUT = float(Config()._event["highTimeout"])


# listen event list
LISTEN_ACCOUNT_BALANCE_EVENT = MyTemplate("""
{
    "type": "LISTEN_ACCOUNT_BALANCE_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": ["$server"]
}
""")

LISTEN_ACCOUNT_WITHDRAW_EVENT = MyTemplate("""
{
    "type": "LISTEN_ACCOUNT_WITHDRAW_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": ["$server", "$asset"]
}
""")

LISTEN_MARKET_KLINE_EVENT = MyTemplate("""
{
    "type": "LISTEN_MARKET_KLINE_EVENT",
    "priority": "medium",
    "timeStamp": $timeStamp,
    "args": ["$server", "$fSymbol", "$tSymbol", "$interval", "$start", "$end"]
}
""")

LISTEN_MARKET_TICKER_EVENT = MyTemplate("""
{
    "type": "LISTEN_MARKET_TICKER_EVENT",
    "priority": "medium",
    "timeStamp": $timeStamp,
    "args": ["$server", "$fSymbol", "$tSymbol"]
}
""")

LISTEN_MARKET_DEPTH_EVENT = MyTemplate("""
{
    "type": "LISTEN_MARKET_DEPTH_EVENT",
    "priority": "medium",
    "timeStamp": $timeStamp,
    "args": ["$server","$fSymbol", "$tSymbol", "$limit"]
}
""")

# judge event list
JUDGE_MARKET_KLINE_EVENT = MyTemplate("""
{
    "type": "JUDGE_MARKET_KLINE_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

JUDGE_MARKET_TICKER_EVENT = MyTemplate("""
{
    "type": "JUDGE_MARKET_TICKER_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

# backtest event list
BACKTEST_MARKET_KLINE_EVENT = MyTemplate("""
{
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")

BACKTEST_MARKET_TICKER_EVENT = MyTemplate("""
{
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")

# order event list
ORDER_MARKET_KLINE_EVENT = MyTemplate("""
{
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

ORDER_MARKET_TICKER_EVENT = MyTemplate("""
{
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

ORDER_CONFIRM_EVENT = MyTemplate("""
{
    "type": "ORDER_CONFIRM_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

ORDER_CANCEL_EVENT = MyTemplate("""
{
    "type": "ORDER_CANCEL_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

# statistic event list
STATISTIC_BACKTEST_EVENT = MyTemplate("""
{
    "type": "STATISTIC_BACKTEST_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")

STATISTIC_ORDER_EVENT = MyTemplate("""
{
    "type": "STATISTIC_ORDER_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")