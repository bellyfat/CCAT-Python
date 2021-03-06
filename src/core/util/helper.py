# -*- coding: utf-8 -*-

import ast
import decimal
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Context, Decimal
from string import Template

import pytz

import dateparser


def float_to_str(f):
    ctx = Context()
    ctx.prec = 50
    d1 = ctx.create_decimal(repr(f))
    f1 = format(d1, 'f')
    if f1[::-1][:2][::-1] == '.0':
        f1 = f1[::-1][2:][::-1]
    return f1


def num_to_precision(num, precision, rounding=ROUND_HALF_UP):
    if precision == 0:
        return str(num)
    if '.' in float_to_str(precision):
        numStr = Decimal(float_to_str(num)).quantize(
            Decimal(float_to_str(precision)), rounding=rounding)
    else:
        idx = '1'
        for s in float_to_str(precision)[::-1]:
            if s == '0':
                idx = idx + '0'
        numStr = Decimal(float_to_str(num / float(idx))).quantize(
            Decimal('1'), rounding=rounding)
        if not str(numStr) == '0':
            numStr = str(numStr) + idx[1:]
    return str(numStr)


def tuple_str_to_list(str):
    return ast.literal_eval(str)


def str_to_list(str):
    return ast.literal_eval(str)


def dict_factory(cursor, row):
    return dict(
        (col[0], row[idx]) for idx, col in enumerate(cursor.description))


def utcnow_timestamp():
    dt = datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp * 1000)


def timestamp_to_isoformat(timeStamp):
    [dt, micro] = datetime.fromtimestamp(
        timeStamp / 1000,
        tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    dt = "%s.%03d" % (dt, int(micro) / 1000)
    return dt + "Z"


def sqlite_escape(sqlStr):
    sqlStr = sqlStr.replace("/", "//")
    sqlStr = sqlStr.replace("'", '"')
    sqlStr = sqlStr.replace("[", "/[")
    sqlStr = sqlStr.replace("]", "/]")
    sqlStr = sqlStr.replace("%", "/%")
    sqlStr = sqlStr.replace("&", "/&")
    sqlStr = sqlStr.replace("_", "/_")
    sqlStr = sqlStr.replace("(", "/(")
    sqlStr = sqlStr.replace(")", "/)")
    return sqlStr


def sqlite_reverse(sqlStr):
    sqlStr = sqlStr.replace("/", "")
    return sqlStr


def json_escape(jsonStr):
    jsonStr = jsonStr.replace("'", "u0022")
    jsonStr = jsonStr.replace('"', "u0022")
    jsonStr = jsonStr.replace(":", "u003a")
    jsonStr = jsonStr.replace("\\", "u005c")
    jsonStr = jsonStr.replace("{", "u007b")
    jsonStr = jsonStr.replace("}", "u007d")
    jsonStr = jsonStr.replace("[", "u005b")
    jsonStr = jsonStr.replace("]", "u005d")
    return jsonStr


def json_reverse(jsonStr):
    jsonStr = jsonStr.replace("u0022", '"')
    jsonStr = jsonStr.replace("u003a", ":")
    jsonStr = jsonStr.replace("u005c", "\\")
    jsonStr = jsonStr.replace("u007b", "{")
    jsonStr = jsonStr.replace("u007d", "}")
    jsonStr = jsonStr.replace("u005b", "[")
    jsonStr = jsonStr.replace("u005d", "]")
    return jsonStr


def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds

    :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str

    :return:
         int value of interval in milliseconds
         None if interval prefix is not a decimal integer
         None if interval suffix is not one of m, h, d, w

    """
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None


class MyTemplate(Template):
    def substitute(self, *args, **kwds):
        try:
            return super().substitute(*args, **kwds)
        except KeyError as err:
            key = str(err.args[0])
            kwds[key] = key
            return self.substitute(*args, **kwds)
