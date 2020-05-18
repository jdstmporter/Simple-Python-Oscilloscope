'''
Created on 18 May 2020

@author: julianporter
'''
import logging
from logging.handlers import SysLogHandler

class Log(object):
    def __init__(self,name,level = logging.INFO):
        self.level=level
        self.log=logging.getLogger(name)
        self.log.setLevel(self.level)
        
        handler=SysLogHandler(facility=SysLogHandler.LOG_SYSLOG)
        handler.setLevel(self.level)
        formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
    
    def setConsole(self):
        handler=logging.StreamHandler()
        handler.setLevel(self.level)
        formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        
    
    def debug(self,message):
        self.log.debug(message)
    
    def info(self,message):
        self.log.info(message)
        
    def warning(self,message):
        self.log.warning(message)
        
    def error(self,message):
        self.log.error(message)
        
    def critical(self,message):
        self.log.critical(message)
    
SYSLOG = Log('spectrum')
SYSLOG.setConsole()
    
    
        
