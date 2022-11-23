# -*- coding: UTF-8 -*-
from pysnmp.entity.rfc3413.oneliner import cmdgen
import time
class bmsdate():
    def __init__(self,ip,public='public',port=161):
        self._ip=ip
        self._public=public
        self._port=port
    def snmpget(self,oid):
        cg = cmdgen.CommandGenerator() ##获得CommandGenerator对象 
        errorIndication, errorStatus, errorIndex, varBinds = cg.getCmd(
          #0代表v1,1代表v2c  
        cmdgen.CommunityData(self._public),  ##社区信息，my-agent ,public 表示社区名,1表示snmp v2c版本，0为v1版本
        cmdgen.UdpTransportTarget((self._ip, self._port)),##这是传输的通道，传输到IP 192.168.70.237, 端口 161上(snmp标准默认161 UDP端口) 
        *oid
        )
        return  varBinds##varBinds返回是一个stulp，含有MIB值和获得值
    def getmkey(self,oid):
        oidlist=[i.split('|')[0] for i in oid]
        print(oidlist)
        reslist=self.snmpget(oidlist)
        datalist=[]
        for index, i in enumerate(reslist):
            print(i[1])
            if i[1]:
                datalist.append(float(i[1])*float(oid[index].split('|')[1]))
            else :datalist.append(65535)
        return datalist
    def zlsnmp(self,oid):
        olist=['1.3.6.1.4.1.1.{}.{}.0'.format(i.split('|')[0],i.split('|')[1]) for i in oid]
        return self.snmpget(olist)

if __name__ == "__main__":
    idlist=['1.3.6.1.4.1.1.1879057635.57.0|0.1']
    ts=bmsdate('192.168.1.89','public',161)

    for i in ts.getmkey(idlist):
        print(i)
