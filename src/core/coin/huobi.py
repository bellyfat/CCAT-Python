# -*- coding: utf-8 -*-

# Huobi Class

from src.core.coin.lib.huobipro_api.Utils import ACCESS_KEY
from src.core.coin.coin import Coin
from src.core.util.exceptions import HuobiException
from src.core.util.helper import date_to_milliseconds, interval_to_milliseconds

class Huobi(Coin):

    def __init__(self, exchange, api_key, api_secret, passphrase,
                 proxies=None):
        super(Huobi, self).__init__(exchange, api_key, api_secret, proxies)
