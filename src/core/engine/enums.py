# -*- coding: utf-8 -*-

from src.core.config import Config
from src.core.util.helper import MyTemplate

# event status
QUEUE_STATUS_EVENT = "queue"
ACTIVE_STATUS_EVENT = "active"
DONE_STATUS_EVENT = "done"

# event priority
LOW_PRIORITY_EVENT = "low" # p.start()
MEDIUM_PRIORITY_EVENT = "medium" # p.start()
HIGH_PRIORITY_EVENT = "high" # p.join()运行

# event timeout in millisenconds
LOW_PRIORITY_EVENT_TIMEOUT = Config()._Event_lowTimeout*1000
MEDIUM_PRIORITY_EVENT_TIMEOUT = Config()._Event_mediumTimeout*1000
HIGH_PRIORITY_EVENT_TIMEOUT = Config()._Event_highTimeout*1000


# listen event list
LISTEN_ACCOUNT_BALANCE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_ACCOUNT_BALANCE_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$server"]
}
""")

LISTEN_ACCOUNT_WITHDRAW_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_ACCOUNT_WITHDRAW_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$server", "$asset"]
}
""")

LISTEN_MARKET_KLINE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_MARKET_KLINE_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$server", "$fSymbol", "$tSymbol", "$interval", "$start", "$end"]
}
""")

LISTEN_MARKET_TICKER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_MARKET_TICKER_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": ["$server", "$fSymbol", "$tSymbol", "$aggDepth"]
}
""")

LISTEN_MARKET_DEPTH_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_MARKET_DEPTH_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": ["$server","$fSymbol", "$tSymbol", "$limit"]
}
""")

# judge event list
JUDGE_MARKET_KLINE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "JUDGE_MARKET_KLINE_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

JUDGE_MARKET_TICKER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "JUDGE_MARKET_TICKER_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": ["$excludeCoins", "$baseCoin", "$symbolStartBaseCoin", "$symbolEndBaseCoin", "$symbolEndTimeout"]
}
""")

# backtest event list
BACKTEST_MARKET_KLINE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

BACKTEST_MARKET_TICKER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

# order event list
ORDER_MARKET_KLINE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "BACKTEST_MARKET_KLINE_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

ORDER_MARKET_TICKER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "BACKTEST_MARKET_TICKER_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

ORDER_CONFIRM_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "ORDER_CONFIRM_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

ORDER_CANCEL_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "ORDER_CANCEL_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

# statistic event list
STATISTIC_BACKTEST_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "STATISTIC_BACKTEST_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

STATISTIC_ORDER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "STATISTIC_ORDER_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": []
}
""")
