import time
import ui_log as log
def cl(reslist):
    resdatelist=[]
    if len(reslist)!=0 and reslist !='err':
        for i in reslist:
            if i[0]:resdatelist.append([time.mktime(time.strptime(str(i[1]),"%Y-%m-%d %H:%M:%S")),float(i[0])])
        resdatelist.sort()
        resdatelist=[i[1] for i in resdatelist]
        return resdatelist
    else: return [0]

def JLJ(reslist):
    res=cl(reslist)
    if len(res)==0:data=0
    else:
        data=float((res[-1]))-float(res[0])
    log.logger2.info(data)
    return(data)
def JAVG(reslist):
    res=cl(reslist)
    data= sum(res)/len(res)
    log.logger2.info(data)
    return(data)
def JSUM(reslist):
    res=cl(reslist)
    data= sum(res)
    log.logger2.info(data)
    return(data)
def JMAX(reslist):
    res=cl(reslist)
    data= max(res)
    log.logger2.info(data)
    return(data)
def JMIN(reslist):
    res=cl(reslist)
    data= min(res)
    log.logger2.info(data)
    return(data)
def JNEW(reslist):
    res=cl(reslist)
    data= res[-1]
    log.logger2.info(data)
    return(data)
def JOLD(reslist):
    res=cl(reslist)
    data= res[0]
    log.logger2.info(data)
    return(data)

if __name__=='__main__':
    a=[[4,'2018-06-05 12:05:00'],[100,'2018-06-05 12:09:00'],[3,'2018-06-05 12:03:00']]
    print(JAVG(a))