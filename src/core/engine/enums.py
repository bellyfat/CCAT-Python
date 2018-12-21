# -*- coding: utf-8 -*-

from src.core.config import Config
from src.core.util.helper import MyTemplate

# CCAT signal
SIGNAL_AUTO = Config()._Signal_auto
SIGNAL_SIGNALS = Config()._Signal_signals

# CCAT types timeWindow
TYPE_DIS_TIMEWINDOW = Config()._Main_typeDisTimeWindow*1000
TYPE_TRA_TIMEWINDOW = Config()._Main_typeTraTimeWindow*1000
TYPE_PAIR_TIMEWINDOW = Config()._Main_typePairTimeWindow*1000

# CCAT types Threshold
TYPE_DIS_THRESHOLD = Config()._Main_typeDisThreshold
TYPE_TRA_THRESHOLD = Config()._Main_typeTraThreshold
TYPE_PAIR_THRESHOLD = Config()._Main_typePairThreshold

# CCAT types
TYPE_DIS = 'dis'
TYPE_TRA = 'tra'
TYPE_PAIR = 'pair'

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
    "args": ["$exchange"]
}
""")

LISTEN_ACCOUNT_WITHDRAW_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_ACCOUNT_WITHDRAW_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$asset"]
}
""")

LISTEN_MARKET_KLINE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_MARKET_KLINE_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$fSymbol", "$tSymbol", "$interval", "$start", "$end"]
}
""")

LISTEN_MARKET_TICKER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_MARKET_TICKER_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$fSymbol", "$tSymbol", "$aggDepth"]
}
""")

LISTEN_MARKET_DEPTH_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "LISTEN_MARKET_DEPTH_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": ["$exchange","$fSymbol", "$tSymbol", "$limit"]
}
""")

# judge event list
JUDGE_MARKET_DEPTH_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "JUDGE_MARKET_DEPTH_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

JUDGE_MARKET_KLINE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "JUDGE_MARKET_KLINE_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

JUDGE_MARKET_TICKER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "JUDGE_MARKET_TICKER_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$types"]
}
""")

# backtest event list
BACKTEST_HISTORY_CREAT_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "BACKTEST_HISTORY_CREAT_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$types"]
}
""")

# order event list
ORDER_HISTORY_INSERT_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "ORDER_HISTORY_INSERT_EVENT",
    "priority": "low",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$fSymbol", "$tSymbol", "$limit", "$ratio"]
}
""")

ORDER_HISTORY_CREAT_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "ORDER_HISTORY_CREAT_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$types"]
}
""")

ORDER_HISTORY_CHECK_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "ORDER_HISTORY_CHECK_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

ORDER_HISTORY_CANCEL_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "ORDER_HISTORY_CANCEL_EVENT",
    "priority": "high",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

# statistic event list
STATISTIC_JUDGE_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "STATISTIC_BACKTEST_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": ["$exchange", "$types"]
}
""")

STATISTIC_BACKTEST_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "STATISTIC_BACKTEST_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": []
}
""")

STATISTIC_ORDER_EVENT = MyTemplate("""
{
    "id": "$id",
    "type": "STATISTIC_ORDER_EVENT",
    "priority": "medium",
    "timeStamp": "$timeStamp",
    "args": []
}
""")
