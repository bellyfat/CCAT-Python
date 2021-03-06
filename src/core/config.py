# -*- coding: utf-8 -*-

import configparser
import os

from src.core.util.exceptions import ApplicationException, ConfigException


class Config(object):

    __cwd = os.getcwd()
    __confStr = os.path.join(__cwd, "config")

    def __init__(self):
        cf = configparser.ConfigParser()
        try:
            cf.read(Config.__confStr)
            # Config
            # Version info
            Config._Version_version = str(cf["Version"]["version"])
            # Author Info
            Config._Author_author = str(cf['Author']['author'])
            Config._Author_email = str(cf['Author']['email'])
            # Register Settings
            Config._Register_user = str(cf['Register']['user'])
            Config._Register_email = str(cf['Register']['email'])
            Config._Register_phone = str(cf['Register']['phone'])
            Config._Register_pwd = str(cf['Register']['pwd'])
            Config._Register_series = str(cf['Register']['series'])
            Config._Register_regCode = str(cf['Register']['regCode'])
            # Debug Settings
            Config._Debug_debug = cf.getboolean(
                'Debug', 'debug', fallback=False)
            Config._Debug_level = str(cf['Debug']['level'])
            if Config._Debug_level not in [
                    'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
            ]:
                raise Exception(
                    "Config Debug Settings Error, debug level not suport.")
            # Main Settings
            # change re-init needed
            Config._Main_types = str(cf['Main']['types']).replace(
                ' ', '').split(',')
            Config._Main_exchanges = str(cf['Main']['exchanges']).replace(
                ' ', '').split(',')
            Config._Main_excludeCoins = str(
                cf['Main']['excludeCoins']).replace(' ', '').split(',')
            Config._Main_baseCoin = str(cf['Main']['baseCoin'])
            Config._Main_basePriceVolume = cf.getfloat('Main',
                                                       'basePriceVolume')
            Config._Main_basePriceTimeout = cf.getfloat(
                'Main', 'basePriceTimeout')
            Config._Main_baseJudgeTimeout = cf.getfloat(
                'Main', 'baseJudgeTimeout')
            Config._Main_baseStatisticJudgeTimeout = cf.getfloat(
                'Main', 'baseStatisticJudgeTimeout')
            Config._Main_baseStatisticTradeTimeout = cf.getfloat(
                'Main', 'baseStatisticTradeTimeout')
            # plug and play
            Config._Main_apiEpochSaveBound = cf.getfloat(
                'Main', 'apiEpochSaveBound')
            Config._Main_apiResultEpoch = cf.getfloat('Main', 'apiResultEpoch')
            Config._Main_marketKlineInterval = cf.getint(
                'Main', 'marketKlineInterval')
            Config._Main_marketTickerInterval = cf.getint(
                'Main', 'marketTickerInterval')
            Config._Main_statisticJudgeMarketTickerInterval = cf.getint(
                'Main', 'statisticJudgeMarketTickerInterval')
            Config._Main_statisticTradeHistoryInterval = cf.getint(
                'Main', 'statisticTradeHistoryInterval')
            Config._Main_marketDepthLimit = cf.getint('Main',
                                                      'marketDepthLimit')
            Config._Main_marketTickerAggStep = cf.getint(
                'Main', 'marketTickerAggStep')
            Config._Main_judgeMarketTickerCycle = cf.getint(
                'Main', 'judgeMarketTickerCycle')
            Config._Main_statisticJudgeMarketTickerCycle = cf.getint(
                'Main', 'statisticJudgeMarketTickerCycle')
            Config._Main_tradeHistoryCycle = cf.getint('Main',
                                                      'tradeHistoryCycle')
            Config._Main_signalTradeCycle = cf.getint('Main',
                                                      'signalTradeCycle')
            Config._Main_statisticSignalTradeCycle = cf.getint(
                'Main', 'statisticSignalTradeCycle')
            Config._Main_asyncAccount = cf.getboolean(
                'Main', 'asyncAccount', fallback=False)
            Config._Main_syncAccountTimeout = cf.getint(
                'Main', 'syncAccountTimeout')
            Config._Main_asyncMarketKline = cf.getboolean(
                'Main', 'asyncMarketKline', fallback=False)
            Config._Main_syncMarketKlineTimeout = cf.getint(
                'Main', 'syncMarketKlineTimeout')
            Config._Main_asyncMarketDepth = cf.getboolean(
                'Main', 'asyncMarketDepth', fallback=False)
            Config._Main_syncMarketDepthTimeout = cf.getint(
                'Main', 'syncMarketDepthTimeout')
            Config._Main_asyncMarketTicker = cf.getboolean(
                'Main', 'asyncMarketTicker', fallback=False)
            Config._Main_syncMarketTickerTimeout = cf.getint(
                'Main', 'syncMarketTickerTimeout')
            Config._Main_asyncJudge = cf.getboolean(
                'Main', 'asyncJudge', fallback=False)
            Config._Main_syncJudgeTimeout = cf.getint('Main',
                                                      'syncJudgeTimeout')

            Config._Main_asyncBacktest = cf.getboolean(
                'Main', 'asyncBacktest', fallback=False)
            Config._Main_syncBacktestTimeout = cf.getint(
                'Main', 'syncBacktestTimeout')
            Config._Main_asyncOrder = cf.getboolean(
                'Main', 'asyncOrder', fallback=False)
            Config._Main_syncOrderTimeout = cf.getint('Main',
                                                      'syncOrderTimeout')
            Config._Main_asyncStatistic = cf.getboolean(
                'Main', 'asyncStatistic', fallback=False)
            Config._Main_syncStatisticTimeout = cf.getint(
                'Main', 'syncStatisticTimeout')
            Config._Main_typeDisThreshold = cf.getfloat(
                'Main', 'typeDisThreshold')
            Config._Main_typeTraThreshold = cf.getfloat(
                'Main', 'typeTraThreshold')
            Config._Main_typePairThreshold = cf.getfloat(
                'Main', 'typePairThreshold')
            Config._Main_typeDisTimeWindow = cf.getfloat(
                'Main', 'typeDisTimeWindow')
            Config._Main_typeTraTimeWindow = cf.getfloat(
                'Main', 'typeTraTimeWindow')
            Config._Main_typePairTimeWindow = cf.getfloat(
                'Main', 'typePairTimeWindow')
            # Signal Settings
            Config._Signal_auto = cf.getboolean(
                'Signal', 'auto', fallback=False)
            Config._Signal_signals = cf['Signal']['signals']
            # Router Settings
            Config._Router_epoch = cf.getfloat('Router', 'epoch')
            Config._Router_timeout = cf.getfloat('Router', 'timeout')
            # Engine Settings
            Config._Engine_epoch = cf.getfloat('Engine', 'epoch')
            Config._Engine_maxProcess = cf.getint('Engine', 'maxProcess')
            Config._Engine_cacheSize = cf.getint('Engine', 'cacheSize')
            # Event Settings
            Config._Event_lowTimeout = cf.getfloat('Event', 'lowTimeout')
            Config._Event_mediumTimeout = cf.getfloat('Event', 'mediumTimeout')
            Config._Event_highTimeout = cf.getfloat('Event', 'highTimeout')
            # Log Settings
            Config._Log_type = str(cf['Log']['type'])
            if Config._Log_type not in ['default', 'Default', 'DEFAULT']:
                raise Exception(
                    "Config Log Settings Error, log type not suport.")
            Config._Log_url = str(cf['Log']['url']) if str(
                cf['Log']['url'])[0] == '/' else os.path.join(
                    Config.__cwd, str(cf['Log']['url']))
            Config._Log_level = str(cf['Log']['level'])
            if Config._Log_level not in [
                    'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
            ]:
                raise Exception(
                    "Config Log Settings Error, log level not suport.")
            # DB Settings
            Config._DB_type = str(cf['DB']['type'])
            if Config._DB_type not in ['sqlite3', 'Sqlite3', 'SQLITE3']:
                raise Exception(
                    "Config DB Settings Error, db type not suport.")
            Config._DB_url = str(cf['DB']['url']) if str(
                cf['DB']['url'])[0] == '/' else os.path.join(
                    Config.__cwd, str(cf['DB']['url']))
            Config._DB_timeout = cf.getfloat('DB', 'timeout')
            Config._DB_synchronous = cf.getboolean(
                'DB', 'synchronous', fallback=False)
            # Proxies Settings
            Config._Proxies_proxies = cf.getboolean(
                'Proxies', 'proxies', fallback=False)
            Config._Proxies_type = str(cf['Proxies']['type'])
            if Config._Proxies_type not in ['http', 'Http', 'HTTP']:
                raise Exception(
                    "Config Proxies Settings Error, proxies type not suport.")
            Config._Proxies_url = {
                "http": str(cf['Proxies']['http_proxy']),
                "https": str(cf['Proxies']['https_proxy'])
            }
            # Okex Setting
            Config._Okex_exchange = str(cf['Okex']['exchange'])
            Config._Okex_api_key = str(cf['Okex']['api_key'])
            Config._Okex_api_secret = str(cf['Okex']['api_secret'])
            Config._Okex_passphrase = str(cf['Okex']['passphrase'])
            # Binance Setting
            Config._Binance_exchange = str(cf['Binance']['exchange'])
            Config._Binance_api_key = str(cf['Binance']['api_key'])
            Config._Binance_api_secret = str(cf['Binance']['api_secret'])
            # Huobi Setting
            Config._Huobi_exchange = str(cf['Huobi']['exchange'])
            Config._Huobi_api_key = str(cf['Huobi']['api_key'])
            Config._Huobi_api_secret = str(cf['Huobi']['api_secret'])
            Config._Huobi_acct_id = str(cf['Huobi']['acct_id'])
            # Other Setting
            Config._Other_exchange = str(cf['Other']['exchange'])
            Config._Other_api_key = str(cf['Other']['api_key'])
            Config._Other_api_secret = str(cf['Other']['api_secret'])

        except Exception as err:
            errStr = "src.core.config.Config.init: %s" % ConfigException(err)
            raise ApplicationException(errStr)
