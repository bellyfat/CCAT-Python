# -*- coding: utf-8 -*-

# engine class
# super class of all engines

from multiprocessing import Pool
from multiprocessing import Process
from abc import ABCMeta, abstractmethod

class Engine(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass
