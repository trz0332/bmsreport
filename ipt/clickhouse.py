# -*- coding:utf-8 -*-
from clickhouse_driver import Client
from .uilog import logger2 as log  #historysignal
import time
class clickhouse:
    def __init__(self,host,port,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port=port
        self.flag=0
        self.__GetConnect()
    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        try:
            self.conn = Client(host=self.host,send_receive_timeout=2,user=self.user,password=self.pwd,database=self.db,port=self.port)
        except Exception as e:
            log.error(e)
            self.flag=0

        else:
            self.flag=1
            return self.conn

    def ExecQuery(self,sql):
        resList=[]
        if self.flag==0:
            self.__GetConnect()
        else:
            resList=self.conn.execute(sql)
        #resList = cur.fetchall()

        #查询完毕后必须关闭连接

        return resList

    def ExecNonQuery(self,sql):
        pass
        if self.flag==0:
            self.__GetConnect()
        else:

            self.conn.execute(sql)


if __name__=='__main__':
    ts=MYSQL('172.31.61.61',3307,'gj','xbrother','historyver1')
    sql="SELECT tag_value from data201801 WHERE tag_no like 'S0E100A3' and save_time < '2018-01-03' and save_time >= '2018-01-02 '"
    print(ts.ExecQuery(sql))