import time

def sqldate(ms,log,date_start,date_end,dev_id,formula='lj'):

    stdate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_start))  #处理起始时间
    eddate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_end+1800))  #处理结束时间
    #self.ms=MSSQL(host=self.config['mssql']['host'],user=self.config['mssql']['user'],pwd=self.config['mssql']['password'],db=self.config['mssql']['db'],port=self.config['mssql']['port'])
    sql="SELECT [value],[date] from PointValue WHERE Convert(varchar,[date],120) >= '{}' AND Convert(varchar,[date],120) < '{}' and nDeviceID  = {} and nIndex = {}".format(stdate,eddate,dev_id.split('|')[0],dev_id.split('|')[1])
    log.debug(sql)
    try:
    	reslist=ms.ExecQuery(sql)
    #print(reslist)
    	log.debug(reslist) 
    except:
        log.info('sql运行失败')
        return 'err'
    else:
        if len(reslist) !=0:
            return reslist
        else :

            log.info('sql没有查询到数据')
            return 'err'
   
