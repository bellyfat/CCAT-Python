# -*- coding: utf-8 -*-

# Huobi Class

import math
from decimal import ROUND_DOWN, ROUND_HALF_UP, ROUND_UP, Decimal

import requests
from requests.exceptions import ConnectionError, ReadTimeout

import pandas as pd
from src.core.coin.coin import Coin
from src.core.coin.enums import *
from src.core.coin.lib.huobipro_api.HuobiService import Huobi as HuobiAPI
from src.core.util.exceptions import HuobiException
from src.core.util.helper import (date_to_milliseconds,
                                  interval_to_milliseconds, num_to_precision,
                                  utcnow_timestamp)


class Huobi(Coin):

    __STATUS = {
        "submitting": CCAT_ORDER_STATUS_ORDERING,
        "submitted": CCAT_ORDER_STATUS_OPEN,
        "partial-filled": CCAT_ORDER_STATUS_PART_FILLED,
        "partial-canceled": CCAT_ORDER_STATUS_CANCELING,
        "filled": CCAT_ORDER_STATUS_FILLED,
        "canceled": CCAT_ORDER_STATUS_CANCELED
    }

    __TYPE = {
        "buy-market": CCAT_ORDER_TYPE_MARKET,
        "sell-market": CCAT_ORDER_TYPE_MARKET,
        "buy-limit": CCAT_ORDER_TYPE_LIMIT,
        "sell-limit": CCAT_ORDER_TYPE_LIMIT
    }

    __SIDE = {
        "buy-market": CCAT_ORDER_SIDE_BUY,
        "sell-market": CCAT_ORDER_SIDE_SELL,
        "buy-limit": CCAT_ORDER_SIDE_BUY,
        "sell-limit": CCAT_ORDER_SIDE_SELL
    }

    def __init__(self,
                 exchange,
                 api_key,
                 api_secret,
                 acct_id=None,
                 proxies=None):
        super(Huobi, self).__init__(exchange, api_key, api_secret, proxies)
        self._acct_id = acct_id
        self._huobiAPI = HuobiAPI(self._api_key, self._api_secret,
                                  self._acct_id, self._proxies)

    # get config
    def getConfig(self):
        return {
            "exchange": self._exchange,
            "api_key": self._api_key,
            "api_secret": self._api_secret,
            "acct_id": self._acct_id,
            "proxies": self._proxies
        }

    # set proxy
    def setProxy(self, proxies):
        self._proxies = proxies
        self._huobiAPI = HuobiAPI(self._api_key, self._api_secret,
                                  self._acct_id, self._proxies)

    # UTC Zone, Unix timestamp in millseconds
    def getServerTime(self):
        try:
            base = self._huobiAPI.get_timestamp()
            if not base['status'] == 'ok':
                raise Exception(base)
            res = int(base["data"])
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getServerTime: exception err=%s" % err
            raise HuobiException(errStr)

    # per seconds qurry and orders rate limits
    def getServerLimits(self):
        '''
        REST API
        限制频率每个API,为10秒100次。
        '''
        res = {
            "info_second": 5,
            "market_second": 5,
            "orders_second": 10,
            "webSockets_second": ''
        }
        return res

    # all symbols in pairs list baseSymbol quoteSymbol
    def getServerSymbols(self):
        try:
            base = self._huobiAPI.get_symbols()
            if not base['status'] == 'ok':
                raise Exception(base)
            fSymbol = ''
            tSymbol = ''
            res = []
            for b in base['data']:
                fSymbol = b["base-currency"].upper()
                tSymbol = b["quote-currency"].upper()
                res.append({"fSymbol": fSymbol, "tSymbol": tSymbol})
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getServerSymbols: exception err=%s" % err
            raise HuobiException(errStr)

    # def getServerSymbols(self):
    #     # not all api defined, get form cryptoCompare
    #     try:
    #         querry = "https://min-api.cryptocompare.com/data/all/exchanges"
    #         res = requests.request("GET", querry)
    #         if res.status_code == requests.codes.ok:
    #             return res.json()["Huobipro"]
    #         else:
    #             raise HuobiException(err)
    #     except requests.exceptions.RequestException:
    #         raise HuobiException(err)

    # buy or sell a specific symbol's rate limits
    def getSymbolsLimits(self):
        '''
        BTC Pair
        Trading Pair	Minimum Amount of Limit Order	Maximum Amount of Limit Order	Minimum Buy of Market Order	Maximum Buy of Market Order	Minimum Sell of Market Order	Maximum Sell of Market Order
        AST/BTC	1	1,000,000	0.0001	100	1	100,000
        ACT/BTC	0.1	500,000	0.0001	100	0.1	50,000
        ADX/BTC	0.01	100,000	0.0001	100	0.01	10,000
        ABT/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        APPC/BTC	0.01	100,000	0.0001	100	0.01	10,000
        AIDOC/BTC	1	5,000,000	0.0001	100	1	1,000,000
        BAT/BTC	1	5,000,000	0.0001	100	1	500,000
        BCH/BTC	0.001	10,000	0.001	1000	0.001	10000
        BCX/BTC	1	100,000,000	0.0001	100	1	1000000
        BTG/BTC	0.001	10,000	0.0001	100	0.001	1,000
        BCD/BTC	0.001	10,000	0.0001	100	0.001	100
        BTM/BTC	1	1,000,000	0.0001	100	1	100,000
        BIFI/BTC	0.01	50,000	0.0001	50	0.01	5,000
        BLZ/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        CMT/BTC	0.1	10,000,000	0.0001	100	0.1	1,000,000
        CVC/BTC	0.1	2,000,000	0.0001	100	0.1	200,000
        CHAT/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        DASH/BTC	0.001	10,000	0.0001	100	0.001	1000
        DGD/BTC	0.001	10,000	0.0001	100	0.001	1000
        DBC/BTC	0.1	1,000,000	0.0001	100	0.1	100000
        DAT/BTC	1	5,000,000	0.0001	100	1	500000
        DTA/BTC	1	100,000,000	0.0001	100	1	10000000
        ETC/BTC	0.01	10,000	0.0001	1000	0.01	10000
        ETH/BTC	0.001	10,000	0.001	1000	0.001	10000
        ELF/BTC	1	1,000,000	0.0001	100	1	100000
        EOS/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        EKO/BTC	1	10,000,000	0.0001	100	1	10,000,000
        EVX/BTC	0.01	100,000	0.0001	100	0.01	10,000
        ELA/BTC	0.01	50,000	0.0001	100	0.01	5,000
        ENG/BTC	0.001	200,000	0.0001	100	0.01	20,000
        EDU/BTC	1	100,000,000	0.0001	100	1	10,000,000
        GNT/BTC	0.1	5,000,000	0.0001	100	0.1	500,000
        GNX/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        GAS/BTC	0.001	10,000	0.0001	100	0.001	1,000
        HT/BTC	0.1	1,000,000	0.0001	1000	0.1	100,000
        HSR/BTC	0.01	20,000	0.0001	100	0.01	2,000
        ITC/BTC	0.1	5,000,000	0.0001	100	0.1	500,000
        ICX/BTC	0.1	100,000	0.0001	100	0.1	10,000
        IOST/BTC	1	10,000,000	0.0001	100	1	1,000,000
        KNC/BTC	0.1	2,000,000	0.0001	100	0.1	200,000
        LTC/BTC	0.01	10,000	0.0001	1000	0.01	10000
        LET/BTC	1	10,000,000	0.0001	100	1	1000000
        LUN/BTC	0.001	20,000	0.0001	100	0.001	2000
        LSK/BTC	0.001	50,000	0.0001	100	0.001	5000
        LINK/BTC	0.1	1,000,000	0.0001	100	0.1	100000
        MANA/BTC	1	10,000,000	0.0001	100	1	500,000
        MTL/BTC	0.01	300,000	0.0001	100	0.01	30,000
        MCO/BTC	0.01	100,000	0.0001	100	0.01	10,000
        MDS/BTC	1	10,000,000	0.0001	100	1	1,000,000
        MEE/BTC	1	5,000,000	0.0001	100	1	500,000
        MTN/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        MTX/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        NEO/BTC	0.001	10,000	0.0001	100	0.001	1,000
        NAS/BTC	0.01	100,000	0.0001	50	0.01	10,000
        OMG/BTC	0.01	200,000	0.0001	100	0.01	20,000
        OST/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        OCN/BTC	1	10,000,000	0.0001	100	1	1,000,000
        ONT/BTC	0.01	100,000	0.0001	50	0.01	10,000
        PAY/BTC	0.1	500,000	0.0001	100	0.1	50,000
        POWR/BTC	0.1	500,000	0.0001	100	0.1	50,000
        PROPY/BTC	0.01	100,000	0.0001	100	0.01	10,000
        QASH/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        QSP/BTC	1	10,000,000	0.0001	100	1	1,000,000
        QTUM/BTC	0.01	100,000	0.0001	100	0.01	10,000
        QUN/BTC	1	10,000,000	0.0001	100	1	1,000,000
        RDN/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        RCN/BTC	1	10,000,000	0.0001	100	1	1,000,000
        REQ/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        RPX/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        RUFF/BTC	1	10,000,000	0.0001	100	1	1,000,000
        SALT/BTC	0.1	100,000	0.0001	100	0.1	10,000
        SBTC/BTC	0.0001	10,000	0.0001	100	0.0001	100
        SMT/BTC	1	10,000,000	0.0001	100	1	1,000,000
        SNT/BTC	0.1	2,000,000	0.0001	100	0.1	200,000
        STORJ/BTC	0.1	2,000,000	0.0001	100	0.1	2,000,000
        SWFTC/BTC	1	10,000,000	0.0001	100	1	1,000,000
        SOC/BTC	1	5,000,000	0.0001	100	1	500,000
        STK/BTC	1	10,000,000	0.0001	100	1	1,000,000
        SRN/BTC	0.01	300,000	0.0001	100	0.01	30,000
        SNC/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        TNB/BTC	1	50,000,000	0.0001	100	1	10,000,000
        TNT/BTC	1	10,000,000	0.0001	100	1	1,000,000
        TRX/BTC	1	10,000,000	0.0001	100	1	1,000,000
        TOPC/BTC	1	10,000,000	0.0001	100	1	1,000,000
        THETA/BTC	1	10,000,000	0.0001	100	1	1,000,000
        UTK/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        VEN/BTC	0.1	500,000	0.0001	100	0.1	50,000
        WAX/BTC	0.001	1,000,000	0.0001	100	0.01	100,000
        WPR/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        WICC/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        XRP/BTC	1	5,000,000	0.0001	100	1	500,000
        XEM/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        YEE/BTC	1	10,000,000	0.0001	100	1	1,000,000
        ZEC/BTC	0.001	5,000	0.0001	100	0.001	500
        ZRX/BTC	1	1,000,000	0.0001	100	1	100,000
        ZIL/BTC	1	10,000,000	0.0001	100	1	1,000,000
        ZLA/BTC	0.1	1,000,000	0.0001	100	0.1	100,000
        CTXC/BTC	0.1	1,000,000　	0.0001　	50	0.1	100000　

        USDT Pair	　	　	　
        Trading Pair	Minimum Amount of Limit Order	Maximum Amount of Limit Order	Minimum Buy of Market Order	Maximum Buy of Market Order	Minimum Sell of Market Order	Maximum Sell of Market Order
        BTC/USDT	0.001	1000	1	1,000,000	0.001	100
        BCH/USDT	0.001	10,000	1	1,000,000	0.001	1,000
        CVC/USDT	0.1	1,000,000	0.1	1,000,000	0.1	100,000
        DTA/USDT	1	20,000,000	0.1	100,000	1	2,000,000
        DASH/USDT	0.001	10,000	1	1,000,000	0.001	1,000
        DBC/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        ETH/USDT 	0.001	1,000	1	100	0.001	100
        ETC/USDT 	0.01	200,000	1	1,000,000	0.01	20,000
        EOS/USDT	0.01	1,000,000	0.1	1,000,000	0.01	100,000
        ELF/USDT	0.1	500,000	0.1	100,000	0.1	50,000
        ELA/USDT	0.001	10,000	0.1	100,000	0.001	1,000
        GNT/USDT	0.1	1,000,000	0.1	100,000	0.1	100,000
        HT/USDT	0.1	1,000,000	0.1	100,000	0.1	100,000
        HSR/USDT	0.01	20,000	1	1,000,000	0.01	2,000
        ITC/USDT	0.01	500,000	0.1	100,000	0.01	100,000
        IOST/USDT	1	20,000,000	0.1	100,000	1	2,000,000
        LET/USDT	1	10,000,000	0.1	100,000	1	1,000,000
        LTC/USDT	0.001	100,000	1	1,000,000	0.001	10,000
        MDS/USDT	0.1	5,000,000	0.1	100,000	0.1	500,000
        NEO/USDT	0.001	10,000	0.1	50,000	0.001	1,000
        NAS/USDT	0.01	100,000	0.1	100,000	0.01	10,000
        OMG/USDT	0.01	1,000,000	0.1	1,000,000	0.01	100,000
        QTUM/USDT	0.01	1,000,000	0.1	200,000	0.01	10,000
        RUFF/USDT	1	5,000,000	0.1	100,000	1	500,000
        SNT/USDT	0.1	1,000,000	0.1	100,000	0.1	100,000
        STORJ/USDT	0.01	100,000	0.1	100,000	0.01	10,000
        SMT/USDT	1	10,000,000	0.1	100,000	1	1,000,000
        TRX/USDT	1	10,000,000	0.1	100,000	1	1,000,000
        THETA/USDT	0.1	3,000,000	0.1	100,000	0.1	300,000
        VEN/USDT	0.1	500,000	0.1	50,000	0.1	50,000
        XRP/USDT	1	5,000,000	1	100,000	1	500,000
        XEM/USDT	0.1	1,000,000	0.1	100,000	0.1	100,000
        ZEC/USDT	0.001	5,000	0.1	10,000,000	0.001	500
        ZIL/USDT	1	10,000,000	0.1	100,000	1	1,000,000
        　	　	　	 	　	　	　
        ETH Pair	　	　	　
        Trading Pair	Minimum Amount of Limit Order	Maximum Amount of Limit Order	Minimum Buy of Market Order	Maximum Buy of Market Order	Minimum Sell of Market Order	Maximum Sell of Market Order
        ACT/ETH	0.1	500,000	0.001	500	0.1	5,000
        ADX/ETH	0.01	100,000	0.001	500	0.01	10,000
        ABT/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        APPC/ETH	0.1	100,000	0.001	500	0.01	100,000
        AIDOC/ETH	1	5,000,000	0.001	500	1	500,000
        BAT/ETH	1	5,000,000	0.001	1,000	1	500,000
        BTM/ETH	1	1,000,000	0.001	500	1	100,000
        BLZ/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        CMT/ETH	0.1	10,000,000	0.001	1,000	0.1	1,000,000
        CVC/ETH	0.1	2,000,000	0.001	100	0.1	200,000
        CHAT/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        DGD/ETH	0.001	10,000	0.0001	1,000	0.001	1,000
        DBC/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        DAT/ETH	1	5,000,000	0.001	500	1	500,000
        DTA/ETH	1	100,000,000	0.001	500	1	10,000,000
        EOS/ETH	0.1	1,000,000	0.001	1,000	0.1	100,000
        ELF/ETH	1	1,000,000	0.001	500	1	100,000
        EVX/ETH	0.01	100,000	0.001	500	0.01	10,000
        EKO/ETH	1	10,000,000	0.001	500	1	10,000,000
        ELA/ETH	0.01	50,000	0.001	500	0.01	5,000
        ENG/ETH	0.01	200,000	0.001	500	0.01	20,000
        EDU/ETH	1	100,000,000	0.001	500	1	10,000,000
        GNT/ETH	0.1	5,000,000	0.001	1,000	0.1	500,000
        GAS/ETH	0.001	10,000	0.001	500	0.001	1,000
        GNX/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        HT/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        HSR/ETH	0.01	20,000	0.001	500	0.01	2,000
        ITC/ETH	0.1	5,000,000	0.001	1,000	1	500,000
        ICX/ETH	0.1	100,000	0.001	500	0.1	10,000
        IOST/ETH	1	1,000,000	0.001	500	1	1,000,000
        LET/ETH	1	10,000,000	0.001	500	1	1,000,000
        LUN/ETH	0.001	20,000	0.001	500	0.001	2,000
        LSK/ETH	0.001	50,000	0.001	500	0.001	5,000
        LINK/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        MANA/ETH	1	10,000,000	0.001	100	1	500,000
        MCO/ETH	0.01	100,000	0.001	1,000	0.01	10,000
        MDS/ETH	1	10,000,000	0.001	500	1	1,000,000
        MEE/ETH	1	5,000,000	0.001	500	1	500,000
        MTN/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        MTX/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        NAS/ETH	0.01	100,000	0.001	500	0.01	10,000
        OMG/ETH	0.01	200,000	0.001	1,000	0.01	20,000
        OST/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        OCN/ETH	1	10,000,000	0.001	500	1	1,000,000
        ONT/ETH	0.01	100,000	0.001	500	0.01	10,000
        PAY/ETH	0.1	500,000	0.001	1,000	0.1	50,000
        POWR/ETH	0.1	500,000	0.001	500	0.1	50,000
        PROPY/ETH	0.01	100,000	0.001	500	0.01	10,000
        QASH/ETH	0.1	1,000,000	0.001	1,000	0.1	100,000
        QSP/ETH	1	10,000,000	0.001	1,000	1	1,000,000
        QTUM/ETH	0.01	100,000	0.0001	100	0.01	10,000
        QUN/ETH	1	10,000,000	0.001	500	1	1,000,000
        RDN/ETH	0.1	1,000,000	0.001	1,000	0.1	100,000
        RCN/ETH	1	10,000,000	0.001	1,000	1	1,000,000
        REQ/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        RUFF/ETH	1	10,000,000	0.001	500	1	1,000,000
        SALT/ETH	0.1	100,000	0.001	500	0.1	10,000
        SMT/ETH	1	10,000,000	0.001	1,000	1	1,000,000
        SWFTC/ETH	1	10,000,000	0.001	500	1	1,000,000
        SOC/ETH	1	5,000,000	0.001	500	1	500,000
        STK/ETH	1	10,000,000	0.001	500	1	1,000,000
        SRN/ETH	0.01	300,000	0.001	500	0.01	30,000
        SNC/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        TNT/ETH	1	10,000,000	0.001	1,000	1	1,000,000
        TNB/ETH	1	50,000,000	0.001	1,000	1	10,000,000
        TRX/ETH	1	10,000,000	0.001	500	1	1,000,000
        TOPC/ETH	1	10,000,000	0.001	500	1	1,000,000
        THETA/ETH	1	10,000,000	0.001	500	1	1,000,000
        UTK/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        VEN/ETH	0.1	500,000	0.001	500	0.1	50,000
        WICC/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        WPR/ETH	0.01	1,000,000	0.001	500	0.1	100,000
        WAX/ETH	0.01	1,000,000	0.001	100	0.1	5,000
        YEE/ETH	1	10,000,000	0.001	500	1	1,000,000
        ZIL/ETH	1	10000000	0.001	500	1	1000000
        ZLA/ETH	0.1	1000000	0.001	500	0.1	100000
        CTXC/ETH	0.1	1,000,000	0.001	500	0.1	100,000
        '''
        dataTable = pd.DataFrame([{
                                      "fSymbol": "AST",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ACT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "ADX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "ABT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "APPC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "AIDOC",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "BAT",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "BCH",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "BCX",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 100000000.00
                                  },
                                  {
                                      "fSymbol": "BTG",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "BCD",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "BTM",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "BIFI",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 50000.00
                                  },
                                  {
                                      "fSymbol": "BLZ",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "CMT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "CVC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 2000000.00
                                  },
                                  {
                                      "fSymbol": "CHAT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "DASH",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "DGD",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "DBC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "DAT",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "DTA",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 100000000.00
                                  },
                                  {
                                      "fSymbol": "ETC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "ETH",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "ELF",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "EOS",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "EKO",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "EVX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "ELA",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 50000.00
                                  },
                                  {
                                      "fSymbol": "ENG",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 200000.00
                                  },
                                  {
                                      "fSymbol": "EDU",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 100000000.00
                                  },
                                  {
                                      "fSymbol": "GNT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "GNX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "GAS",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "HT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "HSR",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 20000.00
                                  },
                                  {
                                      "fSymbol": "ITC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "ICX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "IOST",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "KNC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 2000000.00
                                  },
                                  {
                                      "fSymbol": "LTC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "LET",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "LUN",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 20000.00
                                  },
                                  {
                                      "fSymbol": "LSK",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 50000.00
                                  },
                                  {
                                      "fSymbol": "LINK",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "MANA",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "MTL",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 300000.00
                                  },
                                  {
                                      "fSymbol": "MCO",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "MDS",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "MEE",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "MTN",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "MTX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "NEO",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "NAS",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "OMG",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 200000.00
                                  },
                                  {
                                      "fSymbol": "OST",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "OCN",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ONT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "PAY",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "POWR",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "PROPY",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "QASH",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "QSP",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "QTUM",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "QUN",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "RDN",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "RCN",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "REQ",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "RPX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "RUFF",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SALT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "SBTC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "SMT",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SNT",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 2000000.00
                                  },
                                  {
                                      "fSymbol": "STORJ",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 2000000.00
                                  },
                                  {
                                      "fSymbol": "SWFTC",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SOC",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "STK",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SRN",
                                      "tSymbol": "BTC",
                                      "size_min": 0.01,
                                      "size_max": 300000.00
                                  },
                                  {
                                      "fSymbol": "SNC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "TNB",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 50000000.00
                                  },
                                  {
                                      "fSymbol": "TNT",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "TRX",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "TOPC",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "THETA",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "UTK",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "VEN",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "WAX",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "WPR",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "WICC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "XRP",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "XEM",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "YEE",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ZEC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.00,
                                      "size_max": 5000.00
                                  },
                                  {
                                      "fSymbol": "ZRX",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ZIL",
                                      "tSymbol": "BTC",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ZLA",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "CTXC",
                                      "tSymbol": "BTC",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ACT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "ADX",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "ABT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "APPC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "AIDOC",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "BAT",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "BTM",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "BLZ",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "CMT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "CVC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 2000000.00
                                  },
                                  {
                                      "fSymbol": "CHAT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "DGD",
                                      "tSymbol": "ETH",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "DBC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "DAT",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "DTA",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 100000000.00
                                  },
                                  {
                                      "fSymbol": "EOS",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ELF",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "EVX",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "EKO",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ELA",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 50000.00
                                  },
                                  {
                                      "fSymbol": "ENG",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 200000.00
                                  },
                                  {
                                      "fSymbol": "EDU",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 100000000.00
                                  },
                                  {
                                      "fSymbol": "GNT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "GAS",
                                      "tSymbol": "ETH",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "GNX",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "HT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "HSR",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 20000.00
                                  },
                                  {
                                      "fSymbol": "ITC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "ICX",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "IOST",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "LET",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "LUN",
                                      "tSymbol": "ETH",
                                      "size_min": 0.00,
                                      "size_max": 20000.00
                                  },
                                  {
                                      "fSymbol": "LSK",
                                      "tSymbol": "ETH",
                                      "size_min": 0.00,
                                      "size_max": 50000.00
                                  },
                                  {
                                      "fSymbol": "LINK",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "MANA",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "MCO",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "MDS",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "MEE",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "MTN",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "MTX",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "NAS",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "OMG",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 200000.00
                                  },
                                  {
                                      "fSymbol": "OST",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "OCN",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ONT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "PAY",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "POWR",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "PROPY",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "QASH",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "QSP",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "QTUM",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "QUN",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "RDN",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "RCN",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "REQ",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "RUFF",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SALT",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "SMT",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SWFTC",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SOC",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "STK",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "SRN",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 300000.00
                                  },
                                  {
                                      "fSymbol": "SNC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "TNT",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "TNB",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 50000000.00
                                  },
                                  {
                                      "fSymbol": "TRX",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "TOPC",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "THETA",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "UTK",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "VEN",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "WICC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "WPR",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "WAX",
                                      "tSymbol": "ETH",
                                      "size_min": 0.01,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "YEE",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ZIL",
                                      "tSymbol": "ETH",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "ZLA",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "CTXC",
                                      "tSymbol": "ETH",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "BTC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 1000.00
                                  },
                                  {
                                      "fSymbol": "BCH",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "CVC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "DTA",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 20000000.00
                                  },
                                  {
                                      "fSymbol": "DASH",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "DBC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ETH",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 1000.00
                                  },
                                  {
                                      "fSymbol": "ETC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 200000.00
                                  },
                                  {
                                      "fSymbol": "EOS",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ELF",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "ELA",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "GNT",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "HT",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "HSR",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 20000.00
                                  },
                                  {
                                      "fSymbol": "ITC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "IOST",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 20000000.00
                                  },
                                  {
                                      "fSymbol": "LET",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "LTC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "MDS",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "NEO",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 10000.00
                                  },
                                  {
                                      "fSymbol": "NAS",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "OMG",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "QTUM",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "RUFF",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "SNT",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "STORJ",
                                      "tSymbol": "USDT",
                                      "size_min": 0.01,
                                      "size_max": 100000.00
                                  },
                                  {
                                      "fSymbol": "SMT",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "TRX",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  },
                                  {
                                      "fSymbol": "THETA",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 3000000.00
                                  },
                                  {
                                      "fSymbol": "VEN",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 500000.00
                                  },
                                  {
                                      "fSymbol": "XRP",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 5000000.00
                                  },
                                  {
                                      "fSymbol": "XEM",
                                      "tSymbol": "USDT",
                                      "size_min": 0.10,
                                      "size_max": 1000000.00
                                  },
                                  {
                                      "fSymbol": "ZEC",
                                      "tSymbol": "USDT",
                                      "size_min": 0.00,
                                      "size_max": 5000.00
                                  },
                                  {
                                      "fSymbol": "ZIL",
                                      "tSymbol": "USDT",
                                      "size_min": 1.00,
                                      "size_max": 10000000.00
                                  }])

        try:
            base = self._huobiAPI.get_symbols()
            if not base['status'] == 'ok':
                raise Exception(base)
            res = []
            for b in base['data']:
                # if not b["symbol-partition"]="main":
                #     continue
                fSymbol = b["base-currency"].upper()
                tSymbol = b["quote-currency"].upper()
                tSymbol_price_precision = math.pow(10,
                                                   -int(b["price-precision"]))
                tSymbol_price_max = ''
                tSymbol_price_min = math.pow(10, -int(b["price-precision"]))
                tSymbol_price_step = math.pow(10, -int(b["price-precision"]))
                fSymbol_size_precision = math.pow(10,
                                                  -int(b["amount-precision"]))
                fSymbol_size_max = ''
                fSymbol_size_min = math.pow(10, -int(b["amount-precision"]))
                fSymbol_size_step = math.pow(10, -int(b["amount-precision"]))
                min_notional = tSymbol_price_min * fSymbol_size_min
                isIn = dataTable[(dataTable['fSymbol']==fSymbol)
                                &(dataTable['tSymbol']==tSymbol)]
                if not isIn.empty:
                    fSymbol_size_min = isIn['size_min'].values[0]
                    fSymbol_size_max = isIn['size_max'].values[0]
                res.append({
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "tSymbol_price": {
                        "precision": tSymbol_price_precision,
                        "max": tSymbol_price_max,
                        "min": tSymbol_price_min,
                        "step": tSymbol_price_step
                    },
                    "fSymbol_size": {
                        "precision": fSymbol_size_precision,
                        "max": fSymbol_size_max,
                        "min": fSymbol_size_min,
                        "step": fSymbol_size_step
                    },
                    "min_notional": min_notional
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getSymbolsLimits: exception err=%s" % err
            raise HuobiException(errStr)

    # a specific symbol's tiker with bid 1 and ask 1 info
    def getMarketOrderbookTicker(self, fSymbol, tSymbol, aggDepth=0):
        try:
            symbol = (fSymbol + tSymbol).lower()
            base = self._huobiAPI.get_depth(symbol, 'step0')
            if not base['status'] == 'ok' or not len(
                    base['tick']["bids"]) > 0 or not len(
                        base['tick']["asks"]) > 0:
                raise Exception(base)
            if aggDepth == 0:
                res = {
                    "timeStamp": base["ts"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": float(base['tick']["bids"][0][0]),
                    "bid_one_size": float(base['tick']["bids"][0][1]),
                    "ask_one_price": float(base['tick']["asks"][0][0]),
                    "ask_one_size": float(base['tick']["asks"][0][1])
                }
            else:
                # calc bids
                aggPrice = num_to_precision(
                    float(base['tick']["bids"][0][0]),
                    float(aggDepth),
                    rounding=ROUND_DOWN)
                bid_one_price = float(aggPrice)
                bid_one_size = 0.0
                for bid in base['tick']["bids"]:
                    if float(bid[0]) < float(aggPrice):
                        break
                    bid_one_size = bid_one_size + float(bid[1])
                # calc asks
                aggPrice = num_to_precision(
                    float(base['tick']["asks"][0][0]),
                    float(aggDepth),
                    rounding=ROUND_UP)
                ask_one_price = float(aggPrice)
                ask_one_size = 0.0
                for ask in base['tick']["asks"]:
                    if float(ask[0]) > float(aggPrice):
                        break
                    ask_one_size = ask_one_size + float(ask[1])
                res = {
                    "timeStamp": base["ts"],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "bid_one_price": bid_one_price,
                    "bid_one_size": bid_one_size,
                    "ask_one_price": ask_one_price,
                    "ask_one_size": ask_one_size
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getMarketOrderbookTicker: {fSymbol=%s, tSymbol=%s, aggDepth=%s}, exception err=%s" % (
                fSymbol, tSymbol, aggDepth, err)
            raise HuobiException(errStr)

    # a specific symbol's orderbook with depth
    def getMarketOrderbookDepth(self, fSymbol, tSymbol, limit=''):
        '''
        "tick": {
            "id": 消息id,
            "ts": 消息生成时间，单位：毫秒,
            "bids": 买盘,[price(成交价), amount(成交量)], 按price降序,
            "asks": 卖盘,[price(成交价), amount(成交量)], 按price升序
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            base = self._huobiAPI.get_depth(symbol, 'step0')
            if not base['status'] == 'ok':
                raise Exception(base)
            if limit != '':
                limit = min((int(limit), len(base['tick']["bids"]),
                             len(base['tick']["asks"])))
            else:
                limit = min((len(base['tick']["bids"]),
                             len(base['tick']["asks"])))
            res = {
                "timeStamp": base["ts"],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "bid_price_size": base['tick']["bids"][0:limit:1],
                "ask_price_size": base['tick']["asks"][0:limit:1]
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getMarketOrderbookDepth: {fSymbol=%s, tSymbol=%s, limit=%s}, exception err=%s" % (
                fSymbol, tSymbol, limit, err)
            raise HuobiException(errStr)

    # a specific symbols kline/candlesticks
    def getMarketKline(self, fSymbol, tSymbol, interval, start, end):
        '''
        "data": [
            {
                "id": K线id（时间戳）,
                "amount": 成交量,
                "count": 成交笔数,
                "open": 开盘价,
                "close": 收盘价,当K线为最晚的一根时，是最新成交价
                "low": 最低价,
                "high": 最高价,
                "vol": 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
            }

        ]
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            period = {
                "1m": "1min",
                "5m": "5min",
                "15m": "15min",
                "30m": "30min",
                "1h": "60min",
                "1d": "1day",
                "1m": "1mon",
                "1w": "1week",
                "1y": "1year"
            }
            granularity = interval_to_milliseconds(interval)
            size = int(
                (date_to_milliseconds(end) - date_to_milliseconds(start)) /
                granularity)
            if size < 1 or size > 2000:
                raise Exception("size must between 1-2000")
            base = self._huobiAPI.get_kline(symbol, period[interval], size)
            if not base['status'] == 'ok' or base['data'] == []:
                err = "{fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s} response base=%s" % (
                    fSymbol, tSymbol, interval, start, end, base)
                raise Exception(err)
            res = []
            timeStamp = date_to_milliseconds(start)
            for b in base['data']:
                timeStamp = timeStamp + granularity
                res.append({
                    "timeStamp": timeStamp,
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "open": b["open"],
                    "high": b["high"],
                    "low": b["low"],
                    "close": b["close"],
                    "volume": b["amount"]
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getMarketKline: {fSymbol=%s, tSymbol=%s, interval=%s, start=%s, end=%s}, exception err=%s" % (
                fSymbol, tSymbol, interval, start, end, err)
            raise HuobiException(errStr)

    # get symbol trade fees
    def getTradeFees(self):
        '''
        币币手续费： 挂单成交0.1%， 吃单成交0.15%
        '''
        res = [{"symbol": "all", "maker": 0.002, "taker": 0.002}]
        return res

    # get current trade
    def getTradeOpen(self, fSymbol, tSymbol, limit='100', ratio=''):
        '''
        /* GET /v1/orders/openOrders */
        {
          "status": "ok",
          "data": [
            {
              "id": 5454937,
              "symbol": "ethusdt",
              "account-id": 30925,
              "amount": "1.000000000000000000",
              "price": "0.453000000000000000",
              "created-at": 1530604762277,
              "type": "sell-limit",
              "filled-amount": "0.0",
              "filled-cash-amount": "0.0",
              "filled-fees": "0.0",
              "source": "web",
              "state": "submitted"
            }
          ]
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            account_id = self._acct_id if self._acct_id else self._huobiAPI.get_accounts(
            )['data'][0]['id']
            side = ''
            size = limit
            base = self._huobiAPI.open_orders(account_id, symbol, side, size)
            if not base['status'] == 'ok':
                raise Exception(base)
            res = []
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            for b in base['data']:
                filled_price = 0.0 if float(
                    b["filled-amount"]) == 0 else float(
                        b["filled-cash-amount"]) / float(b["filled-amount"])
                res.append({
                    "timeStamp": b["created-at"],
                    "order_id": b["id"],
                    "status": CCAT_ORDER_STATUS_OPEN,
                    "type": self.__TYPE[b["type"]],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": self.__SIDE[b["type"]],
                    "ask_bid_price": float(b["price"]),
                    "ask_bid_size": float(b["amount"]),
                    "filled_price": filled_price,
                    "filled_size": float(b["filled-amount"]),
                    "fee": float(b["filled-fees"])
                    # "fee": float(b["filled-cash-amount"]) * ratio
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getTradeOpen: {fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s}, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise HuobiException(errStr)

    # get history trade
    def getTradeHistory(self, fSymbol, tSymbol, limit='100', ratio=''):
        '''
        /* GET /v1/order/orders */
        {
          "status": "ok",
          "data": [
            {
              "id": 59378,
              "symbol": "ethusdt",
              "account-id": 100009,
              "amount": "10.1000000000",
              "price": "100.1000000000",
              "created-at": 1494901162595,
              "type": "buy-limit",
              "field-amount": "10.1000000000",
              "field-cash-amount": "1011.0100000000",
              "field-fees": "0.0202000000",
              "finished-at": 1494901400468,
              "user-id": 1000,
              "source": "api",
              "state": "filled",
              "canceled-at": 0,
              "exchange": "huobi",
              "batch": ""
            }
          ]
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            states = "submitting,submitted,partial-filled,partial-canceled,filled,canceled"
            types = "buy-market,sell-market,buy-limit,sell-limit"
            size = limit
            base = self._huobiAPI.orders_list(symbol, states, types, '', '',
                                              '', '', size)
            if not base['status'] == 'ok':
                raise Exception(base)
            res = []
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            for b in base['data']:
                filled_price = 0.0 if float(b["field-amount"]) == 0 else float(
                    b["field-cash-amount"]) / float(b["field-amount"])
                res.append({
                    "timeStamp": b["created-at"],
                    "order_id": b["id"],
                    "status": self.__STATUS[b["state"]],
                    "type": self.__TYPE[b["type"]],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": self.__SIDE[b["type"]],
                    "ask_bid_price": float(b["price"]),
                    "ask_bid_size": float(b["amount"]),
                    "filled_price": filled_price,
                    "filled_size": float(b["field-amount"]),
                    "fee": float(b["field-fees"])
                    # "fee": float(b["field-cash-amount"]) * ratio
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getTradeHistory: {fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s}, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise HuobiException(errStr)

    # get succeed trade
    def getTradeSucceed(self, fSymbol, tSymbol, limit='100', ratio=''):
        '''
        /* GET /v1/order/orders */
        {
          "status": "ok",
          "data": [
            {
              "id": 59378,
              "symbol": "ethusdt",
              "account-id": 100009,
              "amount": "10.1000000000",
              "price": "100.1000000000",
              "created-at": 1494901162595,
              "type": "buy-limit",
              "field-amount": "10.1000000000",
              "field-cash-amount": "1011.0100000000",
              "field-fees": "0.0202000000",
              "finished-at": 1494901400468,
              "user-id": 1000,
              "source": "api",
              "state": "filled",
              "canceled-at": 0,
              "exchange": "huobi",
              "batch": ""
            }
          ]
        }
        '''
        try:
            symbol = (fSymbol + tSymbol).lower()
            states = "filled"
            types = "buy-market,sell-market,buy-limit,sell-limit"
            size = limit
            base = self._huobiAPI.orders_list(symbol, states, types, '', '',
                                              '', '', size)
            if not base['status'] == 'ok':
                raise Exception(base)
            res = []
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            for b in base['data']:
                filled_price = 0.0 if float(b["field-amount"]) == 0 else float(
                    b["field-cash-amount"]) / float(b["field-amount"])
                res.append({
                    "timeStamp": b["created-at"],
                    "order_id": b["id"],
                    "status": self.__STATUS[b["state"]],
                    "type": self.__TYPE[b["type"]],
                    "fSymbol": fSymbol,
                    "tSymbol": tSymbol,
                    "ask_or_bid": self.__SIDE[b["type"]],
                    "ask_bid_price": float(b["price"]),
                    "ask_bid_size": float(b["amount"]),
                    "filled_price": filled_price,
                    "filled_size": float(b["field-amount"]),
                    "fee": float(b["field-fees"])
                    # "fee": float(b["field-cash-amount"]) * ratio
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getTradeSucceed: {fSymbol=%s, tSymbol=%s, limit=%s, ratio=%s}, exception err=%s" % (
                fSymbol, tSymbol, limit, ratio, err)
            raise HuobiException(errStr)

    # get account all asset balance
    def getAccountBalances(self):
        '''
        /* GET /v1/account/accounts/'account-id'/balance */
        {
          "status": "ok",
          "data": {
            "id": 100009,
            "type": "spot",
            "state": "working",
            "list": [
              {
                "currency": "usdt",
                "type": "trade",
                "balance": "500009195917.4362872650"
              },
              {
                "currency": "usdt",
                "type": "frozen",
                "balance": "328048.1199920000"
              },
             {
                "currency": "etc",
                "type": "trade",
                "balance": "499999894616.1302471000"
              },
              {
                "currency": "etc",
                "type": "frozen",
                "balance": "9786.6783000000"
              }
             {
                "currency": "eth",
                "type": "trade",
                "balance": "499999894616.1302471000"
              },
              {
                "currency": "eth",
                "type": "frozen",
                "balance": "9786.6783000000"
              }
            ],
            "user-id": 1000
          }
        }
        '''
        try:
            base = self._huobiAPI.get_balance()
            if not base['status'] == 'ok':
                raise Exception(base)
            currencies = []
            res = []
            for b in base['data']['list']:
                if b["currency"] not in currencies:
                    currencies.append(b["currency"])
                    res.append({
                        "asset": b["currency"],
                        "balance": 0.0,
                        "free": 0.0,
                        "locked": 0.0
                    })
            for i in range(len(res)):
                for b in base['data']['list']:
                    if res[i]["asset"] == b["currency"] and b[
                            "type"] == "trade":
                        res[i]["free"] = float(b["balance"])
                    if res[i]["asset"] == b["currency"] and b[
                            "type"] == "frozen":
                        res[i]["locked"] = float(b["balance"])
            for i in range(len(res)):
                res[i]["asset"] = res[i]["asset"].upper()
                res[i]["balance"] = res[i]["free"] + res[i]["locked"]
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getAccountBalances: exception err=%s" % err
            raise HuobiException(errStr)

    # get account all asset deposit and withdraw history
    def getAccountDetail(self):
        try:
            res = []
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getAccountDetail: exception err=%s" % (
                asset, err)
            raise HuobiException(errStr)

    # get account asset deposit and withdraw limits
    def getAccountLimits(self):
        '''
        /* GET /v1/common/currencys */
        {
          "status": "ok",
          "data": [
            "usdt",
            "eth",
            "etc"
          ]
        }
        '''
        try:
            base = self._huobiAPI.get_currencies()
            if not base['status'] == 'ok':
                raise Exception(base)
            res = []
            for b in base['data']:
                res.append({
                    "asset": b.upper(),
                    "can_deposit": '',
                    "can_withdraw": '',
                    "min_withdraw": ''
                })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getAccountLimits: exception err=%s" % err
            raise HuobiException(errStr)

    # get account asset balance
    def getAccountAssetBalance(self, asset):
        try:
            base = self._huobiAPI.get_balance()
            if not base['status'] == 'ok':
                raise Exception(base)
            res = {}
            for b in base['data']['list']:
                if b["currency"] == asset.lower():
                    res = {
                        "asset": b["currency"],
                        "balance": 0.0,
                        "free": 0.0,
                        "locked": 0.0
                    }
            if res != {}:
                for b in base['data']['list']:
                    if res["asset"] == b["currency"] and b["type"] == "trade":
                        res["free"] = float(b["balance"])
                    if res["asset"] == b["currency"] and b["type"] == "frozen":
                        res["locked"] = float(b["balance"])
            if res != {}:
                res["asset"] = res["asset"].upper()
                res["balance"] = res["free"] + res["locked"]
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getAccountAssetBalance: {asset=%s}, exception err=%s" % (
                asset, err)
            raise HuobiException(errStr)

    # get account asset deposit and withdraw history detail
    def getAccountAssetDetail(self, asset):
        try:
            deRes = self._huobiAPI.get_deposit_withdraw(
                asset.lower(), type='deposit', froms='0', size='100')
            wiRes = self._huobiAPI.get_deposit_withdraw(
                asset.lower(), type='withdraw', froms='0', size='100')
            if not deRes['status'] == 'ok' or not wiRes['status'] == 'ok':
                err = "deRes=%s, wiRes=%s" % (deRes, wiRes)
                raise Exception(err)
            deposit = []
            for de in deRes['data']:
                deposit.append(de)
            withdraw = []
            for wi in wiRes['data']:
                withdraw.appen(wi)
            res = {}
            if deposit != [] or withdraw != []:
                res = {"deposit": deposit, "withdraw": withdraw}
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.getAccountAssetDetail: {asset=%s}, exception err=%s" % (
                asset, err)
            raise HuobiException(errStr)

    # create orders default limit
    def createOrder(self,
                    fSymbol,
                    tSymbol,
                    ask_or_bid,
                    price,
                    quantity,
                    ratio='',
                    type="limit"):
        #  for speed up, lib not check, check from local db.data
        try:
            symbol = (fSymbol + tSymbol).lower()
            source = 'api'
            if ask_or_bid == CCAT_ORDER_SIDE_BUY and type == CCAT_ORDER_TYPE_LIMIT:
                _type = 'buy-limit'
            if ask_or_bid == CCAT_ORDER_SIDE_BUY and type == CCAT_ORDER_TYPE_MARKET:
                _type = 'buy-market'
            if ask_or_bid == CCAT_ORDER_SIDE_SELL and type == CCAT_ORDER_TYPE_LIMIT:
                _type = 'sell-limit'
            if ask_or_bid == CCAT_ORDER_SIDE_SELL and type == CCAT_ORDER_TYPE_MARKET:
                _type = 'sell-market'
            timeStamp = utcnow_timestamp()
            base = self._huobiAPI.send_order(quantity, source, symbol, _type,
                                             price)
            if not base['status'] == 'ok':
                raise Exception(base)
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            res = {
                "timeStamp": timeStamp,
                "order_id": base["data"],
                "status": CCAT_ORDER_STATUS_ORDERING,
                "type": self.__TYPE[_type],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": ask_or_bid,
                "ask_bid_price": float(price),
                "ask_bid_size": float(quantity),
                "filled_price": 0.0,
                "filled_size": 0.0,
                "fee": 0.0
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.createOrder: {fSymbol=%s, tSymbol=%s, ask_or_bid=%s, price=%s, quantity=%s, ratio=%s, type=%s}, exception err=%s" % (
                fSymbol, tSymbol, ask_or_bid, price, quantity, ratio, type,
                err)
            raise HuobiException(errStr)

    # check orders done or undone
    def checkOrder(self, orderID, fSymbol='', tSymbol='', ratio=''):
        try:
            base = self._huobiAPI.order_info(orderID)
            if not base['status'] == 'ok':
                raise Exception(base)
            # if ratio == '':
            #     ratio = self.getTradeFees()[0]["taker"]
            b = base['data']
            filled_price = 0.0 if float(b["field-amount"]) == 0 else float(
                b["field-cash-amount"]) / float(b["field-amount"])
            res = {
                "timeStamp": b["created-at"],
                "order_id": b["id"],
                "status": self.__STATUS[b["state"]],
                "type": self.__TYPE[b["type"]],
                "fSymbol": fSymbol,
                "tSymbol": tSymbol,
                "ask_or_bid": self.__SIDE[b["type"]],
                "ask_bid_price": float(b["price"]),
                "ask_bid_size": float(b["amount"]),
                "filled_price": filled_price,
                "filled_size": float(b["field-amount"]),
                "fee": float(b["field-fees"])
                # "fee": float(b["field-cash-amount"]) * ratio
            }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.checkOrder: {orderID=%s, fSymbol=%s, tSymbol=%s, ratio=%s}, exception err=%s" % (
                orderID, fSymbol, tSymbol, ratio, err)
            raise HuobiException(errStr)

    # cancel orders done or undone
    def cancelOrder(self, orderID, fSymbol='', tSymbol=''):
        try:
            ba = self._huobiAPI.order_info(orderID)
            if not ba['status'] == 'ok':
                err = "{ ba=%s }" % ba
                raise Exception(err)
            if self.__STATUS[ba['data'][
                    "state"]] == CCAT_ORDER_STATUS_OPEN or self.__STATUS[
                        ba['data']["state"]] == CCAT_ORDER_STATUS_PART_FILLED:
                base = self._huobiAPI.cancel_order(orderID)
                rebase = self._huobiAPI.order_info(orderID)
                if not base['status'] == 'ok' or not rebase['status'] == 'ok':
                    err = "{ ba=%s, base=%s, rebase=%s }" % (ba, base, rebase)
                    raise Exception(err)
                res = {
                    "order_id": orderID,
                    "status": self.__STATUS[rebase['data']["state"]]
                }
            else:
                res = {
                    "order_id": orderID,
                    "status": self.__STATUS[ba['data']["state"]]
                }
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.cancelOrder: {orderID=%s, fSymbol=%s, tSymbol=%s }, exception err=%s" % (
                orderID, fSymbol, tSymbol, err)
            raise HuobiException(errStr)

    # cancel the bathch orders
    def cancelBatchOrder(self, orderIDs, fSymbol='', tSymbol=''):
        try:
            res = []
            for orderID in orderIDs:
                ba = self._huobiAPI.order_info(orderID)
                if not ba['status'] == 'ok':
                    err = "{ ba=%s }" % ba
                    raise Exception(err)
                if self.__STATUS[
                        ba['data']
                    ["state"]] == CCAT_ORDER_STATUS_OPEN or self.__STATUS[
                        ba['data']["state"]] == CCAT_ORDER_STATUS_PART_FILLED:
                    base = self._huobiAPI.cancel_order(orderID)
                    rebase = self._huobiAPI.order_info(orderID)
                    if not base['status'] == 'ok' or not base[
                            'status'] == 'ok' or not rebase['status'] == 'ok':
                        err = "{ ba=%s, base=%s, rebase=%s }" % (ba, base,
                                                                 rebase)
                        raise Exception(err)
                    res.append({
                        "order_id": orderID,
                        "status": self.__STATUS[rebase['data']["state"]]
                    })
                else:
                    res.append({
                        "order_id": orderID,
                        "status": self.__STATUS[ba['data']["state"]]
                    })
            return res
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.cancelBatchOrder: {orderIDs=%s, fSymbol=%s, tSymbol=%s }, exception err=%s" % (
                orderIDs, fSymbol, tSymbol, err)
            raise HuobiException(errStr)

    # one click cancle all orders
    def oneClickCancleOrders(self):
        try:
            res = self._huobiAPI.cancel_open_orders()
            if not res['status'] == 'ok':
                err = "{ res=%s }" % res
                raise Exception(err)
            if res['data']['failed-count'] > 0:
                return False
            return True
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.oneClickCancleOrders: exception err=%s" % err
            raise HuobiException(errStr)

    # one click trans all to baseCoin
    def oneClickTransToBaseCoin(self, baseCoin='USDT'):
        try:
            exceptionStr = []
            balance = self.getAccountBalances()
            symbol = self.getSymbolsLimits()
            deSet = []
            trSet = []
            # trSet -> deSet
            for b in balance:
                isIn = False
                if b['asset'] != baseCoin and b['free'] > 0:
                    for s in symbol:
                        if (baseCoin.upper(), b['asset']) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                        if (b['asset'], baseCoin.upper()) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                    if isIn == False:
                        for s in symbol:
                            if b['asset'] == s['fSymbol'] and isIn == False:
                                for sy in symbol:
                                    if (baseCoin.upper(), s['tSymbol']) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_SELL,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
                                    if (s['tSymbol'], baseCoin.upper()) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_SELL,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
                            if b['asset'] == s['tSymbol'] and isIn == False:
                                for sy in symbol:
                                    if (baseCoin.upper(), s['tSymbol']) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_BUY,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
                                    if (s['tSymbol'], baseCoin.upper()) == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        trSet.append({
                                            'fSymbol':
                                            s['fSymbol'],
                                            'tSymbol':
                                            s['tSymbol'],
                                            'balance':
                                            float(b['free']),
                                            'ask_or_bid':
                                            CCAT_ORDER_SIDE_BUY,
                                            'limit_price_precision':
                                            "NULL"
                                            if s["tSymbol_price"]["precision"]
                                            == '' else float(s["tSymbol_price"]
                                                             ["precision"]),
                                            'limit_size_precision':
                                            "NULL"
                                            if s["fSymbol_size"]["precision"]
                                            == '' else float(s["fSymbol_size"]
                                                             ["precision"]),
                                            'limit_size_min':
                                            "NULL" if
                                            s["fSymbol_size"]["min"] == '' else
                                            float(s["fSymbol_size"]["min"]),
                                            'limit_min_notional':
                                            "NULL" if s["min_notional"] == ''
                                            else float(s["min_notional"])
                                        })
            for tr in trSet:
                res = self.getMarketOrderbookDepth(tr['fSymbol'],
                                                   tr['tSymbol'], 100)
                sum = 0
                trTrade = []
                if tr['ask_or_bid'] == CCAT_ORDER_SIDE_BUY:
                    for r in res['ask_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        trBalanceSize = tr['balance'] / rprice
                        if sum < trBalanceSize:
                            trSize = min(trBalanceSize - sum, rSize)
                            if not trSize > 0:
                                continue
                            if not tr['limit_size_min'] == 'NULL':
                                if trSize < tr['limit_size_min']:
                                    continue
                            if not tr['limit_min_notional'] == 'NULL':
                                if rprice * trSize < tr['limit_min_notional']:
                                    continue
                            sum = sum + trSize
                            trTrade.append({'price': rprice, 'size': trSize})
                if tr['ask_or_bid'] == CCAT_ORDER_SIDE_SELL:
                    for r in res['bid_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        trBalanceSize = tr['balance']
                        if sum < trBalanceSize:
                            trSize = min(trBalanceSize - sum, rSize)
                            if not trSize > 0:
                                continue
                            if not tr['limit_size_min'] == 'NULL':
                                if trSize < tr['limit_size_min']:
                                    continue
                            if not tr['limit_min_notional'] == 'NULL':
                                if rprice * trSize < tr['limit_min_notional']:
                                    continue
                            sum = sum + trSize
                            trTrade.append({'price': rprice, 'size': trSize})
                for trade in trTrade:
                    price = num_to_precision(
                        trade['price'],
                        tr['limit_price_precision'],
                        rounding=ROUND_HALF_UP)
                    size = num_to_precision(
                        trade['size'],
                        tr['limit_size_precision'],
                        rounding=ROUND_DOWN)
                    if not float(size) > 0:
                        continue
                    if not tr['limit_size_min'] == 'NULL':
                        if float(size) < tr['limit_size_min']:
                            continue
                    if not tr['limit_min_notional'] == 'NULL':
                        if float(price) * float(
                                size) < tr['limit_min_notional']:
                            continue
                    try:
                        base = self.createOrder(
                            tr['fSymbol'], tr['tSymbol'], tr['ask_or_bid'],
                            str(price), str(size), 0, CCAT_ORDER_TYPE_LIMIT)
                    except Exception as err:
                        exceptionStr.append(err)
            # deSet -> baseCoin
            balance = self.getAccountBalances()
            for b in balance:
                isIn = False
                if b['asset'] != baseCoin and b['free'] > 0:
                    for s in symbol:
                        if (baseCoin.upper(), b['asset']) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                            deSet.append({
                                'fSymbol':
                                s['fSymbol'],
                                'tSymbol':
                                s['tSymbol'],
                                'balance':
                                float(b['free']),
                                'ask_or_bid':
                                CCAT_ORDER_SIDE_BUY,
                                'limit_price_precision':
                                "NULL" if s["tSymbol_price"]["precision"] == ''
                                else float(s["tSymbol_price"]["precision"]),
                                'limit_size_precision':
                                "NULL" if s["fSymbol_size"]["precision"] == ''
                                else float(s["fSymbol_size"]["precision"]),
                                'limit_size_min':
                                "NULL" if s["fSymbol_size"]["min"] == '' else
                                float(s["fSymbol_size"]["min"]),
                                'limit_min_notional':
                                "NULL" if s["min_notional"] == '' else float(
                                    s["min_notional"])
                            })
                        if (b['asset'], baseCoin.upper()) == (
                                s['fSymbol'], s['tSymbol']) and isIn == False:
                            isIn = True
                            deSet.append({
                                'fSymbol':
                                s['fSymbol'],
                                'tSymbol':
                                s['tSymbol'],
                                'balance':
                                float(b['free']),
                                'ask_or_bid':
                                CCAT_ORDER_SIDE_SELL,
                                'limit_price_precision':
                                "NULL" if s["tSymbol_price"]["precision"] == ''
                                else float(s["tSymbol_price"]["precision"]),
                                'limit_size_precision':
                                "NULL" if s["fSymbol_size"]["precision"] == ''
                                else float(s["fSymbol_size"]["precision"]),
                                'limit_size_min':
                                "NULL" if s["fSymbol_size"]["min"] == '' else
                                float(s["fSymbol_size"]["min"]),
                                'limit_min_notional':
                                "NULL" if s["min_notional"] == '' else float(
                                    s["min_notional"])
                            })
            for de in deSet:
                res = self.getMarketOrderbookDepth(de['fSymbol'],
                                                   de['tSymbol'], 100)
                sum = 0
                deTrade = []
                if de['ask_or_bid'] == CCAT_ORDER_SIDE_BUY:
                    for r in res['ask_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        deBalanceSize = de['balance'] / rprice
                        if sum < deBalanceSize:
                            deSize = min(deBalanceSize - sum, rSize)
                            if not deSize > 0:
                                continue
                            if not de['limit_size_min'] == 'NULL':
                                if deSize < de['limit_size_min']:
                                    continue
                            if not de['limit_min_notional'] == 'NULL':
                                if rprice * deSize < de['limit_min_notional']:
                                    continue
                            sum = sum + deSize
                            deTrade.append({'price': rprice, 'size': deSize})
                if de['ask_or_bid'] == CCAT_ORDER_SIDE_SELL:
                    for r in res['bid_price_size']:
                        rprice = float(r[0])
                        rSize = float(r[1])
                        deBalanceSize = de['balance']
                        if sum < deBalanceSize:
                            deSize = min(deBalanceSize - sum, rSize)
                            if not deSize > 0:
                                continue
                            if not de['limit_size_min'] == 'NULL':
                                if deSize < de['limit_size_min']:
                                    continue
                            if not de['limit_min_notional'] == 'NULL':
                                if rprice * deSize < de['limit_min_notional']:
                                    continue
                            sum = sum + deSize
                            deTrade.append({'price': rprice, 'size': deSize})
                for trade in deTrade:
                    price = num_to_precision(
                        trade['price'],
                        de['limit_price_precision'],
                        rounding=ROUND_HALF_UP)
                    size = num_to_precision(
                        trade['size'],
                        de['limit_size_precision'],
                        rounding=ROUND_DOWN)
                    if not float(size) > 0:
                        continue
                    if not de['limit_size_min'] == 'NULL':
                        if float(size) < de['limit_size_min']:
                            continue
                    if not de['limit_min_notional'] == 'NULL':
                        if float(price) * float(
                                size) < de['limit_min_notional']:
                            continue
                    try:
                        base = self.createOrder(
                            de['fSymbol'], de['tSymbol'], de['ask_or_bid'],
                            str(price), str(size), 0, CCAT_ORDER_TYPE_LIMIT)
                    except Exception as err:
                        exceptionStr.append(err)
            # check trans result
            if not exceptionStr == []:
                raise Exception(exceptionStr)
            balance = self.getAccountBalances()
            for b in balance:
                isIn = False
                if b['asset'] != baseCoin and b['free'] > 0:
                    for s in symbol:
                        if (b['asset'],
                                'USDT') == (s['fSymbol'],
                                            s['tSymbol']) and isIn == False:
                            isIn = True
                            res = self.getMarketOrderbookDepth(
                                s['fSymbol'], s['tSymbol'], 10)
                            if float(b['free']) * float(res['bid_price_size'][
                                    0][0]) > CCAT_BALANCE_SMALL_AMOUNT_USDT:
                                return False
                    if isIn == False:
                        for s in symbol:
                            if b['asset'] == s['fSymbol'] and isIn == False:
                                for sy in symbol:
                                    if (s['tSymbol'], 'USDT') == (
                                            sy['fSymbol'],
                                            sy['tSymbol']) and isIn == False:
                                        isIn = True
                                        res = self.getMarketOrderbookDepth(
                                            s['fSymbol'], s['tSymbol'], 10)
                                        resy = self.getMarketOrderbookDepth(
                                            sy['fSymbol'], sy['tSymbol'], 10)
                                        if float(b['free']) * float(
                                                res['bid_price_size'][0]
                                            [0]) * float(
                                                resy['bid_price_size'][0][0]
                                            ) > CCAT_BALANCE_SMALL_AMOUNT_USDT:
                                            return False
            return True
        except (ReadTimeout, ConnectionError, KeyError, Exception) as err:
            errStr = "src.core.coin.huobi.Huobi.oneClickTransToBaseCoin: exception err=%s" % err
            raise HuobiException(errStr)

    # deposit asset balance
    def depositAsset(self, asset):
        pass

    # withdraw asset balance
    def withdrawAsset(self, asset):
        pass
