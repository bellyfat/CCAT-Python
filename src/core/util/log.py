# -*- coding: utf-8 -*-

import os
import time
import logging
import colorlog
from src.core.config import Config

class Logger(object):

    _type = Config()._log["type"]
    _fileStr = Config()._log["url"]
    # _fileStr = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + "_CCAT_Python_Spam.log"
    _logfile = os.path.join(os.getcwd(),"log", _fileStr)
    _file_formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    _console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)-8s: %(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )


    def __init__(self):
        # 设置文件日志的格式
        # 定义日志处理器将INFO或者以上级别的日志发送到 sys.stderr
        handler = logging.FileHandler(Logger._logfile, mode="a+")
        handler.setFormatter(Logger._file_formatter)
        handler.setLevel(logging.INFO)
        # 设置控制台日志的格式
        # 定义日志处理器将WARNING或者以上级别的日志发送到 console
        console = logging.StreamHandler()
        console.setFormatter(Logger._console_formatter)
        console.setLevel(logging.DEBUG)
        # 设置logger
        self._logger = logging.getLogger(Logger._type)
        # 添加至logger
        self._logger.handlers = []
        self._logger.addHandler(handler)
        self._logger.addHandler(console)
        self._logger.setLevel(logging.DEBUG)

    def debug(self, msg):
        self._logger.debug(msg)

    def info(self, msg):
        self._logger.info(msg)

    def warn(self, msg):
        self._logger.warn(msg)

    def error(self, msg):
        self._logger.error(msg)

    def critical(self, msg):
        self._logger.critical(msg)
