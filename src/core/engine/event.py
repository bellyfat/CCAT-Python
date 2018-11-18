# -*- coding: utf-8 -*-

from string import Template

# listen event list
LISTEN_DEPTH_EVENT = Template('''
{
    "type": "LISTEN_DEPTH_EVENT"
    "dict": {
        "servers": $servers,
        "args": [$fSymbol, $tSymbol, $limit],
        "remark": "symbols info, run as need"
    }
}
''')
LISTEN_KLINE_EVENT = Template('''
{
    "type": "LISTEN_KLINE_EVENT"
    "dict": {
        "servers": $servers,
        "args": [$fSymbol, $tSymbol, $interval, $start, $end],
        "remark": "symbols filter, run first and frequent"
    }
}
''')
LISTEN_TICKER_EVENT = Template('''
{
    "type": "LISTEN_TICKER_EVENT"
    "dict": {
        "servers": $servers,
        "args": [$fSymbol, $tSymbol],
        "remark": "ccat filter, run as frequent as possible"
    }
}
''')

# judge event list
JUDGE_KLINE_EVENT = Template('''
{
    "type": "JUDGE_KLINE_EVENT"
    "dict": {
        "servers": $servers,
        "args": [],
        "remark": ""
    }
}
''')
JUDGE_TICKER_EVENT = Template('''
{
    "type": "JUDGE_TICKER_EVENT"
    "dict": {
        "servers": $servers,
        "args": [],
        "remark": ""
    }
}
''')

# backtest event list
BACKTEST_EVENT = Template('''
{
    "type": "BACKTEST_EVENT"
    "dict": {
        "servers": $servers,
        "args": [],
        "remark": ""
    }
}
''')

# execute event list
EXECUTE_EVENT = Template('''
{
    "type": "EXECUTE_EVENT"
    "dict": {
        "servers": $servers,
        "args": [],
        "remark": ""
    }
}
''')

# statistic event list
STATISTIC_EVENT = Template('''
{
    "type": "BACKTEST_EVENT"
    "dict": {
        "servers": $servers,
        "args": [],
        "remark": ""
    }
}
''')
