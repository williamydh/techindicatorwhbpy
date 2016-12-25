#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 2016年12月1日

@author: william
'''

import logging
 
class Logger:
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        #fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # 设置Console日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler("techindicatorwhbpy.log")
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
        
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
        
    def error(self, message):
        self.logger.error(message)
    
    def warn(self, message):
        self.logger.warn(message)
        
    def critical(self, message):
        self.logger.critical(message)