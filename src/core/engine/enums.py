# -*- coding: utf-8 -*-

from string import Template

# event priority
LOW_PRIORITY_ENVENT = "low" # p.start()
MEDIUM_PRIORITY_ENVENT = "medium" # p.start()
HIGH_PRIORITY_ENVENT = "high" # p.join()运行

LOW_PRIORITY_ENVENT_TIMEOUT = 30
MEDIUM_PRIORITY_ENVENT_TIMEOUT = 10
HIGH_PRIORITY_ENVENT_TIMEOUT = 5


# listen event list
LISTEN_ACCOUNT_BALANCE_EVENT = Template("""
{
    "type": "LISTEN_ACCOUNT_BALANCE_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": ["$server"]
}
""")

LISTEN_ACCOUNT_WITHDRAW_EVENT = Template("""
{
    "type": "LISTEN_ACCOUNT_WITHDRAW_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": ["$server", "$asset"]
}
""")

LISTEN_MARKET_KLINE_EVENT = Template("""
{
    "type": "LISTEN_MARKET_KLINE_EVENT",
    "priority": "medium",
    "timeStamp": $timeStamp,
    "args": ["$server", "$fSymbol", "$tSymbol", "$interval", "$start", "$end"]
}
""")

LISTEN_MARKET_TICKER_EVENT = Template("""
{
    "type": "LISTEN_MARKET_TICKER_EVENT",
    "priority": "medium",
    "timeStamp": $timeStamp,
    "args": ["$server", "$fSymbol", "$tSymbol"]
}
""")

LISTEN_MARKET_DEPTH_EVENT = Template("""
{
    "type": "LISTEN_MARKET_DEPTH_EVENT",
    "priority": "medium",
    "timeStamp": $timeStamp,
    "args": ["$server","$fSymbol", "$tSymbol", "$limit"]
}
""")

# judge event list
JUDGE_MARKET_KLINE_EVENT = Template("""
{
    "type": "JUDGE_MARKET_KLINE_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

JUDGE_MARKET_TICKER_EVENT = Template("""
{
    "type": "JUDGE_MARKET_TICKER_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

# backtest event list
BACKTEST_MARKET_KLINE_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")

BACKTEST_MARKET_TICKER_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")

# order event list
ORDER_MARKET_KLINE_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

ORDER_MARKET_TICKER_EVENT = Template("""
{
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

ORDER_CONFIRM_EVENT = Template("""
{
    "type": "ORDER_CONFIRM_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

ORDER_CANCEL_EVENT = Template("""
{
    "type": "ORDER_CANCEL_EVENT",
    "priority": "high",
    "timeStamp": $timeStamp,
    "args": []
}
""")

# statistic event list
STATISTIC_BACKTEST_EVENT = Template("""
{
    "type": "STATISTIC_BACKTEST_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")

STATISTIC_ORDER_EVENT = Template("""
{
    "type": "STATISTIC_ORDER_EVENT",
    "priority": "low",
    "timeStamp": $timeStamp,
    "args": []
}
""")
