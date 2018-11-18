# -*- coding: utf-8 -*-

from src.core.engine.engine import Event, EventEngine

class Listen(Engine):

    def __init__(self, engine):
        self.__engine = engine
