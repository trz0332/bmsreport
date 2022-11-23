import time
from .uilog import logger2 as log  #historysignal

def sqldate(ms,date_start,date_end,tag_no):
    stdate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_start))  #处理起始时间
    eddate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_end+100))  #处理结束时间
    sql=''
    sql1="SELECT FLOATVALUE ,RECORDTIME from sgdatabase.historysignal where EQUIPMENTID = {} and SIGNALID = {}".format(tag_no.split('|')[0],tag_no.split('|')[1])
    sql2=" and RECORDTIME between  toDateTime('{}') and  toDateTime('{}')".format(stdate,eddate)
    sql=sql1+sql2
    log.debug(sql)
    try:
        res=ms.ExecQuery(sql)
        log.info(res)
    except Exception as e:
        log.info(e)
        log.info('sql运行失败')
        return 'err'
    else:
        if len(res) !=0:
            return res
        else :
            log.info('sql没有查询到数据')
            return 'err'

if __name__=='__main__':
    pass