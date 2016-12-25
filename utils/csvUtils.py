#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Created on 2016年11月30日

@author: william
'''
import pandas as pd
import numpy as np
import datetime, time 
import math
from func import OverlapStudies as ovst
from utils.logUtils import Logger

logger = Logger("csvUtils")
originalCsvFile = "/Users/william/Downloads/data-compx/300001.SZ.csv"
processCsvFile = "D:/talibdata/5/300001.SZ.csv"
indexCsvFile = "/Users/william/Downloads/data-compx/399006.csv"
encoding = "GBK"

removeStopDayList = []
stopDayList = []

df = pd.read_csv(originalCsvFile, encoding=encoding)
rowValues = df.values


dfIndexValue = pd.read_csv(indexCsvFile, encoding=encoding).values
indexList = []
for indexValue in dfIndexValue:
    tmp = time.strptime(indexValue[0], "%Y-%m-%d")
    y, m, d = tmp[0:3]
    indexValue[0] = datetime.date(y, m, d)
    indexList.append(indexValue.tolist())


for rowValue in rowValues:
    t = time.strptime(rowValue[0][0:10], "%Y-%m-%d")
    y, m, d = t[0:3]
    rowValue[0] = datetime.date(y, m, d)
    if rowValue[8] == u"停牌一天":        
        stopDayList.append(rowValue.tolist())
    else:
        removeStopDayList.append(rowValue.tolist())
        
removeStopDayListLen = len(removeStopDayList)        
del removeStopDayList[removeStopDayListLen - 1]
removeStopDayListLen = len(removeStopDayList)

rowValueN = removeStopDayList[removeStopDayListLen - 1]

def getAdjfactorData(rowValuei, rowValueN):
    tmpAdj = rowValuei[7] / rowValueN[7]
    rowValuei[1] = round(rowValuei[1] * tmpAdj, 4)
    rowValuei[2] = round(rowValuei[2] * tmpAdj, 4)
    rowValuei[3] = round(rowValuei[3] * tmpAdj, 4)
    rowValuei[4] = round(rowValuei[4] * tmpAdj, 4)
    rowValuei[6] = round(rowValuei[6] / tmpAdj)
 
    return

def getIndexAndFuncParams(firstIndexDate):
    if removeStopDayList[0][0] > firstIndexDate:
        firstIndexDate = removeStopDayList[0][0]
    retequity = 0.0
    retindex = 0.0
    ret = 0.0
    close = 0.0
    closeIndex = 0.0
    closePre = 0.0
    closeIndexPre = 0.0
    i = 0
    
    openList = []
    highList = []
    lowList = []
    closeList=[]
    volumeList = []
        
    while i < removeStopDayListLen :
        getAdjfactorData(removeStopDayList[i], rowValueN)
        
        openList.append(removeStopDayList[i][1])   
        highList.append(removeStopDayList[i][2])   
        lowList.append(removeStopDayList[i][3])   
        closeList.append(removeStopDayList[i][4])   
        volumeList.append(removeStopDayList[i][6])  
    
        dateI = removeStopDayList[i][0]
        close = removeStopDayList[i][4]
        for indexItem in indexList:
                if indexItem[0] == dateI:
                    closeIndex = indexItem[4]
        if dateI > firstIndexDate:
            retequity = round(math.log(close) - math.log(closePre), 4)
            retindex = round(math.log(closeIndex) - math.log(closeIndexPre), 4)
            ret = round(retequity - retindex, 4)
                    
        removeStopDayList[i].append(retequity)
        removeStopDayList[i].append(retindex)
        removeStopDayList[i].append(ret)
    
        closeIndexPre = closeIndex
        closePre = close
        i = i + 1    
    openNdarry = np.array(openList)
    highNdarry = np.array(highList)
    lowNdarry = np.array(lowList)
    closeNdarry = np.array(closeList)
    volumeNdarry = np.array(volumeList)
    return openNdarry, highNdarry, lowNdarry, closeNdarry, volumeNdarry, removeStopDayList

firstIndexDate = indexList[0][0]
preCloseIndex = indexList[0][4]

timeperiod=5
openNdarry, highNdarry, lowNdarry, closeNdarry, volumeNdarry, returnList = getIndexAndFuncParams(firstIndexDate)


#Overlap Studies
ovst.BBANDS(closeNdarry, timeperiod, returnList)
rowLen = len(returnList[0])
for rowItem in returnList:
    logger.debug(str(rowItem[0]) + " || " + str(rowItem[rowLen-3]) + " || " + str(rowItem[rowLen-2]) + " || " + str(rowItem[rowLen-1]))


'''
for rowItem in removeStopDayList:
    logger.debug(str(rowItem[0]) + " || " + str(rowItem[61]) + " || " + str(rowItem[62]) + " || " + str(rowItem[63]))   
'''
