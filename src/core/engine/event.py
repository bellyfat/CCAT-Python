# -*- coding: utf-8 -*-

from string import Template

# listen event list
LISTEN_ACCOUNT_BALANCE_EVENT = Template('''
{
    "type": "LISTEN_ACCOUNT_BALANCE_EVENT",
    "dict": {
        "args": ["$server"],
        "remark": "account balance history, run as need"
    }
}
''')
LISTEN_ACCOUNT_WITHDRAW_EVENT = Template('''
{
    "type": "LISTEN_ACCOUNT_WITHDRAW_EVENT",
    "dict": {
        "args": ["$server", "$asset"],
        "remark": "account withdraw history, run as need"
    }
}
''')
LISTEN_DEPTH_EVENT = Template('''
{
    "type": "LISTEN_DEPTH_EVENT",
    "dict": {
        "args": ["$server","$fSymbol", "$tSymbol", "$limit"],
        "remark": "symbols info, run as need"
    }
}
''')
LISTEN_KLINE_EVENT = Template('''
{
    "type": "LISTEN_KLINE_EVENT",
    "dict": {
        "args": ["$server", "$fSymbol", "$tSymbol", "$interval", "$start", "$end"],
        "remark": "symbols filter, run first and frequent"
    }
}
''')
LISTEN_TICKER_EVENT = Template('''
{
    "type": "LISTEN_TICKER_EVENT",
    "dict": {
        "args": ["$server", "$fSymbol", "$tSymbol"],
        "remark": "ccat filter, run as frequent as possible"
    }
}
''')

# judge event list
JUDGE_KLINE_EVENT = Template('''
{
    "type": "JUDGE_KLINE_EVENT",
    "dict": {
        "args": [],
        "remark": ""
    }
}
''')
JUDGE_TICKER_EVENT = Template('''
{
    "type": "JUDGE_TICKER_EVENT",
    "dict": {
        "args": [],
        "remark": ""
    }
}
''')

# backtest event list
BACKTEST_EVENT = Template('''
{
    "type": "BACKTEST_EVENT",
    "dict": {
        "args": [],
        "remark": ""
    }
}
''')

# execute event list
EXECUTE_EVENT = Template('''
{
    "type": "EXECUTE_EVENT",
    "dict": {
        "args": [],
        "remark": ""
    }
}
''')

# statistic event list
STATISTIC_EVENT = Template('''
{
    "type": "BACKTEST_EVENT",
    "dict": {
        "args": [],
        "remark": ""
    }
}
''')
