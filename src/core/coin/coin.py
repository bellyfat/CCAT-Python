# coin class
# super class of all coins

 from abc import ABCMeta, abstractmethod

Class Coin:
    __metaclass__ = ABCMeta

    def __init__(self, exchange, api_key, api_secret, **kwargs):
        self.exchange = exchange
        self.api_key = api_key
        self.api_secret = api_secret
        if "proxies" in kwargs.keys():
            self.proxies = kwargs["proxies"]
        else:
            self.proxies = ""

    def getConfig(self): # get config
        return {"exchange":self.exchange, "api_key":self.api_key, "api_secret":self.api_secret, "proxies":self.proxies}

    @abstractmethod
    def getServerTime(**kwargs): # UTC Zone, Unix timestamp in millseconds
        pass

    @abstractmethod
    def getServerLimits(**kwargs): # perseconds qurry and orders rate limits
        pass

    @abstractmethod
    def getSymbols(**kwargs): # all symbols in pairs list baseSymbol quoteSymbol
        pass

    @abstractmethod
    def getSymbolsLimits(symbol, **kwargs): # buy or sell a specific symbol's rate limits
        pass

    @abstractmethod
    def getMarketOrderbookTicker(symbol, **kwargs): # a specific symbol's tiker with bid 1 and ask 1 info
        pass

    @abstractmethod
    def getMarketOrderbookDepth(symbol, **kwargs): # a specific symbol's orderbook with depth
        pass

    @abstractmethod
    def getMarketKline(symbol, **kwargs): # a specific symbols kline/candlesticks
        pass

    @abstractmethod
    def getTradeOpen(**kwargs): # get current trade

    @abstractmethod
    def getTradeHistory(**kwargs): # get history trade

    @abstractmethod
    def getTradeSucceed(**kwargs): # get succeed trade
        pass

    @abstractmethod
    def getAccountBalances(**kwargs): # get account all asset balance
        pass

    @abstractmethod
    def getAccountAssetBalance(asset, **kwargs): # get account asset balance
        pass

    @abstractmethod
    def getAccountAssetDetail(asset, **kwargs): # get account asset deposit and withdraw detail
        pass

    def setProxy(self, proxies): # set proxy
        self.proxies = proxies

    @abstractmethod
    def createOrder(symbol, quantity, price, type="limit", **kwargs):
        pass

    @abstractmethod
    def checkOrder(symbol, orderID, **kwargs):
        pass

    @abstractmethod
    def cancleOrder(symbol, orderID, **kwargs):
        pass
