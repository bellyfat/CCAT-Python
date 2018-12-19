# -*- coding: utf-8 -*-

import logging
import os
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

import colorlog

from src.core.config import Config
from src.core.util.exceptions import LogException


class Logger(object):
    # debug
    __debug = Config()._Debug_debug
    __debug_level = Config()._Debug_level
    # log
    __log_type = Config()._Log_type
    __log_url = Config()._Log_url
    __log_level = Config()._Log_level
    __file_formatter = logging.Formatter(
        '%(asctime)s pid=%(process)d %(levelname)-4s: %(message)s')
    __console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s pid=%(process)d %(levelname)-4s: %(reset)s%(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        },
        secondary_log_colors={},
        style='%')
    # logging
    __level = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self):
        # Config init

        # 设置文件日志的格式
        # 定义日志处理器将INFO或者以上级别的日志发送到 sys.stderr
        # handler = logging.FileHandler(Logger.__log_url, mode="a+")
        handler = logging.handlers.TimedRotatingFileHandler(
            Logger.__log_url, when="d", interval=1, backupCount=7)
        handler.setFormatter(Logger.__file_formatter)
        handler.setLevel(Logger.__level[Logger.__log_level])
        # 设置控制台日志的格式
        # 定义日志处理器将WARNING或者以上级别的日志发送到 console
        console = logging.StreamHandler()
        console.setFormatter(Logger.__console_formatter)
        console.setLevel(Logger.__level[Logger.__debug_level])
        # 设置logger
        self._logger = logging.getLogger(Logger.__log_type)
        # 添加至logger
        self._logger.handlers = []
        self._logger.addHandler(handler)
        if Logger.__debug:
            self._logger.addHandler(console)
        self._logger.setLevel(logging.DEBUG)

    def debug(self, msg):
        try:
            self._logger.debug(msg)
        except Exception as err:
            raise LogException(err)

    def info(self, msg):
        try:
            self._logger.info(msg)
        except Exception as err:
            raise LogException(err)

    def warn(self, msg):
        try:
            self._logger.warn(msg)
        except Exception as err:
            raise LogException(err)

    def error(self, msg):
        try:
            self._logger.error(msg)
        except Exception as err:
            raise LogException(err)

    def critical(self, msg):
        try:
            self._logger.critical(msg)
        except Exception as err:
            raise LogException(err)
