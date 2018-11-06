# encoding:utf8

# Exception Tables
# exceptions, code, message, detail
# okexException, code=-1001, message = exceptions throwed related to okex exchange
# binanceException, code=-1002, message = exceptions throwed related to binance exchange
# huobiException, code=-1003, message = exceptions throwed related to huobi exchange
# gateException, code=-1004, message = exceptions throwed related to gate exchange

class OkexException(Exception):

    def __init__(self):
        self.code = -1001
        self.message = "exceptions throwed related to okex exchange"

    def __str__(self):  # pragma: no cover
        return 'Exception(code=%s): %s' % (self.code, self.message)

class BinanceException(Exception):

    def __init__(self):
        self.code = -1002
        self.message = "exceptions throwed related to binance exchange"

    def __str__(self):  # pragma: no cover
        return 'Exception(code=%s): %s' % (self.code, self.message)

class HuobiException(Exception):

    def __init__(self):
        self.code = -1003
        self.message = "exceptions throwed related to huobi exchange"

    def __str__(self):  # pragma: no cover
        return 'Exception(code=%s): %s' % (self.code, self.message)

class GateException(Exception):

    def __init__(self):
        self.code = -1004
        self.message = "exceptions throwed related to gate exchange"

    def __str__(self):  # pragma: no cover
        return 'Exception(code=%s): %s' % (self.code, self.message)
