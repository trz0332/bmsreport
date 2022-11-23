
import logging 
import logging.handlers 
import time

########################初始化log日志
LEVELS={'notset':logging.DEBUG,  
        'debug':logging.DEBUG,   
        'info':logging.INFO,   
        'warning':logging.WARNING,  
        'error':logging.ERROR,    
        'critical':logging.CRITICAL} 


LOG_FILENAME = 'test.log'  
LOG_BACKUPCOUNT = 5   
LOG_LEVEL = 'notset'      
def InitLog(file_name,logger):   
    LOG_FILENAME = file_name       
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=10*1024*1024,backupCount=LOG_BACKUPCOUNT)    
    #handler = logging.FileHandler(LOG_FILENAME)  
    formatter = logging.Formatter("[ %(asctime)s ][%(lineno)d][ %(levelname)s ][%(funcName)s] [%(module)s]%(message)s")   
    handler.setFormatter(formatter)       
    #logger = logging.getLogger()   
    logger.addHandler(handler)   
    logger.setLevel(LEVELS.get(LOG_LEVEL.lower()))  
    return logger  

logger2 = logging.getLogger('requestinfo')
logger2=InitLog('报表日志{}.log'.format(time.strftime('%Y%m%d',time.localtime(time.time()))),logger2)
