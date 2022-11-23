# -*- coding:utf-8 -*-
import pymssql
import time
class MSSQL:
    def __init__(self,host,user,pwd,db,port=1433):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port= port
    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,port=self.port,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

if __name__=='__main__':
    ts=MSSQL('192.168.1.181','sa','ABCabc123','MJSQL3.0',1433)
    print(ts.ExecQuery('select count(*) form Alarm'))