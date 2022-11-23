import time
from .uilog import logger2 as log
def range_date(date_start,date_end):          #2020061100:35_0_41_1_4_0:0000
    tlist=[]
    while date_start<date_end+86400:
        stdate=time.strftime("%Y%m%d", time.localtime(date_start))  #处理起始时间
        tlist.append('new_hisdp_{}'.format(stdate))
        date_start+=86400
    #print(tlist)
    return tlist

def sqldate(db,date_start,date_end,dev_id):
    tlist=range_date(date_start,date_end)
    res_all=[]
    devid=int(dev_id.split('|')[0])
    point_index=int(dev_id.split('|')[1])
    try:
        for sheet in tlist[:-1]:
            res=db[sheet].find({'id':devid,'s':1,'i':point_index})
            for i in res:
                x=i['l']
                for z in x:
                    res_all.append([z['v'],z['t'].replace(microsecond=0)])
    
        if tlist[-1] in db.list_collection_names():
            res=db[tlist[-1]].find({'id':devid,'s':1,'i':point_index,'_id':'{}/{}/00'.format(devid,point_index)})
            res_all.append([res[0]['l'][0]['v'],res[0]['l'][0]['t'].replace(microsecond=0)])
    except Exception as e:
        #print(e)
        log.debug(e)
        log.debug('查询失败运行失败')
        return 'err'
    else:
        #print(res_all)
        log.debug(res_all)
        return res_all


if __name__=='__main__':
    import pymongo
    import js2
    myclient = pymongo.MongoClient("mongodb://10.2.201.15:27017/")
    mydb = myclient["mon_data"]
    x=sqldate(mydb,time.time()-86400*2,time.time()-86400,'596|12')
    f=js2.cl2(x)
    print(f)
