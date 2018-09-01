import time
def cl(reslist):
    resdatelist=[]
    if len(reslist)!=0 and reslist !='err':
        for i in reslist:
            #print(i)
            if i[0]:resdatelist.append([time.mktime(time.strptime(str(i[1]),"%Y-%m-%d %H:%M:%S")),float(i[0])])
        resdatelist.sort()
        resdatelist=[i[1] for i in resdatelist]
        return resdatelist
    else: return [0]

def JLJ(reslist):
    res=cl(reslist)
    if len(res)==0:return 0
    else:
        return float((res[-1]))-float(res[0])
def JAVG(reslist):
    res=cl(reslist)
    return sum(res)/len(res)
def JSUM(reslist):
    res=cl(reslist)
    return sum(res)
def JMAX(reslist):
    res=cl(reslist)
    return max(res)
def JMIN(reslist):
    res=cl(reslist)
    return min(res)
def JNEW(reslist):
    res=cl(reslist)
    return res[-1]
def JOLD(reslist):
    res=cl(reslist)
    return res[0]

if __name__=='__main__':
    a=[[4,'2018-06-05 12:05:00'],[100,'2018-06-05 12:09:00'],[3,'2018-06-05 12:03:00']]
    print(avg(a))