# -*- coding:utf-8 -*-
import pymysql
import time
class MYSQL:
    def __init__(self,host,port,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port=port
    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8",port=self.port)
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
    ts=MYSQL('172.31.61.61',3307,'gj','xbrother','historyver1')
    sql="SELECT tag_value from data201801 WHERE tag_no like 'S0E100A3' and save_time < '2018-01-03' and save_time >= '2018-01-02 '"
    print(ts.ExecQuery(sql))