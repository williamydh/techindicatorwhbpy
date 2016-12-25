#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年12月3日

@author: william
'''

import talib

from utils.logUtils import Logger

logger = Logger("OverlapStudies")
def BBANDS(close, timeperiod, returnList):
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod, nbdevup=2, nbdevdn=2, matype=0)
    i=0
    while i < len(returnList):
        returnList[i].append(round(upperband[i],4))
        returnList[i].append(round(middleband[i],4))
        returnList[i].append(round(lowerband[i],4))
        i=i+1    