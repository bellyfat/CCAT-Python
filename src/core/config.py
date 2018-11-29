# -*- coding: utf-8 -*-

import configparser
import os

from src.core.util.exceptions import ConfigException


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
                'Debug', 'debug', fallback=True)
            Config._Debug_level = str(cf['Debug']['level'])
            # Main Settings
            Config._Main_exchanges = cf['Main']['exchanges'].split(',')
            Config._Main_excludeCoins = cf['Main']['excludeCoins'].split(',')
            Config._Main_baseCoin = str(cf['Main']['baseCoin'])
            Config._Main_basePriceVolume = cf.getfloat('Main',
                                                       'basePriceVolume')
            Config._Main_basePriceTimeout = cf.getfloat('Main',
                                                       'basePriceTimeout')

            Config._Main_symbolStartBaseCoin = cf.getfloat(
                'Main', 'symbolStartBaseCoin')
            Config._Main_symbolEndBaseCoin = cf.getfloat(
                'Main', 'symbolEndBaseCoin')
            Config._Main_symbolEndTimeout = cf.getfloat(
                'Main', 'symbolEndTimeout')
            Config._Main_apiEpochSaveBound = cf.getfloat(
                'Main', 'apiEpochSaveBound')
            # Engine Settings
            Config._Engine_epoch = cf.getfloat('Engine', 'epoch')
            Config._Engine_maxProcess = cf.getfloat('Engine', 'maxProcess')
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
            # DB Settings
            Config._DB_type = str(cf['DB']['type'])
            if Config._DB_type not in ['sqlite3', 'Sqlite3', 'SQLITE3']:
                raise Exception(
                    "Config DB Settings Error, db type not suport.")
            Config._DB_url = str(cf['DB']['url']) if str(
                cf['DB']['url'])[0] == '/' else os.path.join(
                    Config.__cwd, str(cf['DB']['url']))
            Config._DB_timeout = cf.getfloat('DB', 'timeout')
            Config._DB_synchronous = cf.getboolean('DB', 'synchronous', fallback=False)
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
            # Gate Setting
            Config._Gate_exchange = str(cf['Gate']['exchange'])
            Config._Gate_api_key = str(cf['Gate']['api_key'])
            Config._Gate_api_secret = str(cf['Gate']['api_secret'])

        except Exception as err:
            errStr = "src.core.config.Config.init: %s" % ConfigException(err)
            raise ConfigException(err)
