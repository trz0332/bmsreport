import time
import ui_log as log
def sqldate(ms,date_start,date_end,dev_id):
    stdate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_start))  #处理起始时间
    eddate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_end+1800))  #处理结束时间
    sql="SELECT [value],[date] from PointValue WHERE Convert(varchar,[date],120) >=\
     '{}' AND Convert(varchar,[date],120) < '{}' and nDeviceID  = {} and nIndex =\
      {}".format(stdate,eddate,dev_id.split('|')[0],dev_id.split('|')[1])
    log.logger2.debug(sql)
    try:
        reslist=ms.ExecQuery(sql)
    except Exception as e:
        log.logger2.info(e)
        log.logger2.info('sql运行失败')
        return 'err'
    else:
        log.logger2.debug(reslist) 
        if len(reslist) !=0:
            return reslist
        else :
            log.logger2.info('sql没有查询到数据')
            return 'err'
        
   
