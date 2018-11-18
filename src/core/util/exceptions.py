# -*- coding: utf-8 -*-

# Exception Tables
# exceptions, code, message, detail
# okexException, code = -1001, message = okex exchange exceptions throwed
# binanceException, code = -1002, message = binance exchange exceptions throwed
# huobiException, code = -1003, message = huobi exchange exceptions throwed
# gateException, code = -1004, message = gate exchange exceptions throwed

# DBException, code = -2000, message =

# EngineException, code = -3000, message =

# ApplicationException, code = -4000

class ApplicationException(Exception):

    def __init__(self, err):
        self.code = -4000
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'ApplicationException(code=%s): %s' % (self.code, self.message)


class EngineException(Exception):

    def __init__(self, err):
        self.code = -3000
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'EngineException(code=%s): %s' % (self.code, self.message)


class DBException(Exception):

    def __init__(self, err):
        self.code = -2000
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'DBException(code=%s): %s' % (self.code, self.message)


class OkexException(Exception):

    def __init__(self, err):
        self.code = -1001
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'OkexException(code=%s): %s' % (self.code, self.message)

class BinanceException(Exception):

    def __init__(self, err):
        self.code = -1002
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'BinanceException(code=%s): %s' % (self.code, self.message)

class HuobiException(Exception):

    def __init__(self):
        self.code = -1003
        self.message = "huobi exchange exceptions throwed"

    def __str__(self):  # pragma: no cover
        return 'HuobiException(code=%s): %s' % (self.code, self.message)

class GateException(Exception):

    def __init__(self):
        self.code = -1004
        self.message = "gate exchange exceptions throwed"

    def __str__(self):  # pragma: no cover
        return 'GateException(code=%s): %s' % (self.code, self.message)
