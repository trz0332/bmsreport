import time
from .uilog import logger2 as log
from operator import itemgetter
def cl2(reslist):
    resdatelist=[]
    if len(reslist)!=0 and reslist !='err':
        for i in reslist:
            if i[0]:resdatelist.append([time.mktime(time.strptime(str(i[1]),"%Y-%m-%d %H:%M:%S")),float(i[0])])
        resdatelist.sort()
        resdatelist=[i[1] for i in resdatelist]
        return resdatelist
    else: return [0]
def cl(reslist):
    if len(reslist)!=0 and reslist !='err':
        reslist.sort(key=itemgetter(1,0))
        reslist=[i[0] for i in reslist]
        return reslist
    else: return [0]
def JLJ(reslist):
    res=cl(reslist)
    if len(res)==0:data=0
    else:
        data=float((res[-1]))-float(res[0])
    #log.logger2.info(data)
    return round(data,2)
def JAVG(reslist):
    res=cl(reslist)
    data= sum(res)/len(res)
    #log.logger2.info(data)
    return round(data,2)
def JSUM(reslist):
    res=cl(reslist)
    data= sum(res)
    #log.logger2.info(data)
    return round(data,2)
def JMAX(reslist):
    res=cl(reslist)
    data= max(res)
    #log.logger2.info(data)
    return round(data,2)
def JMIN(reslist):
    res=cl(reslist)
    data= min(res)
    #log.logger2.info(data)
    return round(data,2)
def JNEW(reslist):
    res=cl(reslist)
    #log.logger2.info(data)
    data= res[-1]
    return round(data,2)
def JOLD(reslist):
    res=cl(reslist)
    data= res[0]
    #log.logger2.info(data)
    return round(data,2)
def JLAST(reslist):
    res=cl(reslist)
    data= res[-1]
    #log.logger2.info(data)
    return round(data,2)
def JFIRST(reslist):
    res=cl(reslist)
    data= res[0]
    #log.logger2.info(data)
    return round(data,2)

if __name__=='__main__':
    import datetime
    a=[[95.0, datetime.datetime(2021, 6, 7, 16, 1, 41)], [94.0, datetime.datetime(2021, 6, 9, 16, 0, 42)]]
    print(cl2(a))