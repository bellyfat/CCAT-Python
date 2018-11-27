# -*- coding: utf-8 -*-

# Exception Tables

# okexException, code = -1001, message = err
# binanceException, code = -1002, message = err
# huobiException, code = -1003, message = err
# gateException, code = -1004, message = err
# DBException, code = -2000, message = err
# EngineException, code = -3000, message = err
# RouterException, code = -4000, message = err
# ApplicationException, code = -5000, message = err

class ApplicationException(Exception):

    def __init__(self, err):
        self.code = -5000
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'ApplicationException(code=%s): %s' % (self.code, self.message)

class RouterException(Exception):

    def __init__(self, err):
        self.code = -4000
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'RouterException(code=%s): %s' % (self.code, self.message)

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

    def __init__(self, err):
        self.code = -1003
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'HuobiException(code=%s): %s' % (self.code, self.message)

class GateException(Exception):

    def __init__(self, err):
        self.code = -1004
        self.message = err

    def __str__(self):  # pragma: no cover
        return 'GateException(code=%s): %s' % (self.code, self.message)
