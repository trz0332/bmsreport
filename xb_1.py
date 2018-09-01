import time
def int2str(s,y):
    if len(str(s))<y:
        return('0'*(y-len(str(s)))+str(s))
    else :return str(s)

def sqldate(ms,log,date_start,date_end,tag_no,formula='lj'):

    stdate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_start))  #处理起始时间
    eddate=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(date_end))  #处理结束时间
    sql=''
    sql1="SELECT tag_value ,save_time from data{} where tag_no like \'{}\'"
    sql2=" and save_time >= '{}' and save_time < '{}'".format(stdate,eddate)
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
        if index==len(tablesheet)-1:sql+=sql1.format(i,tag_no)+sql2
        else:sql+=sql1.format(i,tag_no)+sql2+' union '
    log.debug(sql)
    
    try:
        res=ms.ExecQuery(sql)
        log.info(res)
    except:
        log.info('sql运行失败')
        return 'err'
    else:
        if len(res) !=0:
            return res
        else :

            log.info('sql没有查询到数据')
            return 'err'
    log.debug(reslist)

    #return js.js(reslist,formula)
