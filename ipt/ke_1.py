import time,sys
sys.path.append("../")
from .uilog import logger2 as log
housrs=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
minutes=['0000', '0300', '0600', '0900', '1200', '1500', '1800', '2100', '2400', '2700', '3000', '3300']
def t2s(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{}:{}".format(m, s)
def time2date(x):  #用于把ssdb里面的时间转换程ISO时间
    if not isinstance(x, str):
        gg=str(x, encoding = "utf-8") .split(':')
    else:gg=x.split(':')
    data='{}-{}-{}'.format(gg[0][:4],gg[0][4:6],gg[0][6:8])
    return '{} {}:{}'.format(data,gg[0][8:10],t2s(int(gg[2])))
def range_date(date_start,date_end,devid):          #2020061100:35_0_41_1_4_0:0000
    tlist=[]
    while date_start<date_end:
        stdate=time.strftime("%Y%m%d", time.localtime(date_start))  #处理起始时间
        for housr in housrs:
            for minute in minutes:
                tlist.append('{}{}:{}:{}'.format(stdate,housr,devid,minute))
        date_start+=86400
    return tlist
        
def sqldate(ssdb,date_start,date_end,dev_id):
    tlist=range_date(date_start,date_end,dev_id)
    res_all=[]
    try:
        tlist.append(('{}00:{}:0000').format(time.strftime("%Y%m%d", time.localtime(date_end)),dev_id))
        res=ssdb.multi_get(*tlist)
        """
        for i in tlist:
            a=time.time()
            resx=ssdb.scan('{}000'.format(i),'{}3700'.format(i),10000)
            res_all+=resx
            print(resx)
            #print(time.time()-a)
        end_key=('{}00:{}:0000').format(time.strftime("%Y%m%d", time.localtime(date_end)),dev_id)
        res_all+=[end_key,ssdb.get(end_key)]
        res=[]
        """
        for i in range(len(res)//2):
            res_all.append((float(res[2*i+1]),time2date(res[2*i])))
    except Exception as e:
        #print(e)
        log.info(e)
        log.info('查询失败运行失败')
        return 'err'
    else:
        log.debug(res_all)
        return res_all

if __name__=='__main__':
    import pyssdb
    import js2
    host='172.31.169.81'
    #host='172.31.61.130'
    ssdb = pyssdb.Client(host=host, port=31002)
    x=sqldate(ssdb,time.time()-86400*2,time.time()-86400,'44_0_149_1_640_0')
    f=js2.cl(x)
    print(x)
    #print(time.time())
