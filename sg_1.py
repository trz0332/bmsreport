import time
import ui_log as log
def int2str(s,y):
    if len(str(s))<y:
        return('0'*(y-len(str(s)))+str(s))
    else :return str(s)

def sqldate(ms,date_start,date_end,tag_no):
    stdate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_start))  #处理起始时间
    eddate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_end))  #处理结束时间
    sql=''
    sql1="SELECT FLOATVALUE ,RECORDTIME from historysignal_{} where EQUIPMENTID = \'{}\' and SIGNALID = \'{}\'"

    sql2= " and RECORDTIME >= ( SELECT RECORDTIME FROM historysignal_{} WHERE \
     EQUIPMENTID = '{}' and SIGNALID = '{}' and RECORDTIME < '{} ' \
     ORDER BY RECORDTIME DESC LIMIT 1) and RECORDTIME < \
      (SELECT RECORDTIME FROM historysignal_{} WHERE EQUIPMENTID = '{}' and SIGNALID = '{}' \
      and RECORDTIME > '{} ' LIMIT 1 )"
    sy=int(stdate.split(' ')[0].split('-')[0])
    sm=int(stdate.split(' ')[0].split('-')[1])
    ey=int(eddate.split(' ')[0].split('-')[0])
    em=int(eddate.split(' ')[0].split('-')[1])
    tablesheet=[]
    while sy<=ey:
        if sy == ey:
            while sm<=em:
                tablesheet.append(str(sy)+int2str(sm,2))
                sm+=1
        else :
            while sm <=12:    
                tablesheet.append(str(sy)+int2str(sm,2))
                sm+=1
        sm=1
        sy+=1
    for index,i in enumerate(tablesheet):
        if index==len(tablesheet)-1:
            sql=sql+sql1.format(i,tag_no.split('|')[0],tag_no.split('|')[1])+\
            sql2.format(i,tag_no.split('|')[0],tag_no.split('|')[1],stdate,i,tag_no.split('|')[0],tag_no.split('|')[1],eddate)
        else:
            sql+=sql1.format(i,tag_no.split('|')[0],tag_no.split('|')[1])+\
            sql2.format(i,tag_no.split('|')[0],tag_no.split('|')[1],stdate,i,tag_no.split('|')[0],tag_no.split('|')[1],eddate)+' union '
    log.logger2.debug(sql)
    try:
        res=ms.ExecQuery(sql)
        log.logger2.info(res)
    except:
        log.logger2.info('sql运行失败')
        return 'err'
    else:
        if len(res) !=0:
            return res
        else :
            log.logger2.info('sql没有查询到数据')
            return 'err'


    #return js.js(reslist,formula)
