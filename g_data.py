
class bl():
    def __init__(self):
        self.vison="1.2.1"
        self.host,self.port,self.usr,self.passwd,self.db='','','','',''
        self.text_help="配置文件帮助:\n\
第一次打开该程序会判断配置文件是否存在,如果不存在则使用初始配置创建该INI配置文件\n\
配置文件包含两部分:\n\
[server]\n\
host = xxx.xxx.xxx.xxx   ;数据库IP\n\
db = MJSQL3.0   ;数据库名中联默认MJSQL3.0   共济默认historyver1\n\
passwd = ABCabc123  ;数据库密码.默认共济的是xbrother中联的需要后台设置\n\
port = 14333  ;数据库端口默认共济的mysql是3307,中联用的sqlserver是1433 \n\
user = sa  ;数据库用户名默认共济的是gj,中联的需要进sqlserver后台设置\n\
\n\
[sheet_day]\n\
sjl = A    ;时间所在列\n\
gzh = 6    ;规则所在行\n\
cj = 1    ;0选择共济  1选择中联\n\
mode =0      ；0选择按时间  1选择最后填充\n\
filename = E:/Seafile/snmp/共济自定义报表程序/ss.xlsx  ;报表文件路径名字\n\
\n\
报表文件格式:\n\
\n\
需要在原来的报表文件里面添加2行,一样命名规则,一行命名测点\n\
\n\
测点行格式:\n\
测点行需要在规则行上一行,测点行格式A=测点ID,多个测点需要换行\n\
中联的测点格式为:A=设备ID|测点索引,比如电表的ID为1234,电量测点在地12个测点,那个格式为:A=1234|12\n\
共济的测点格式为:A=测点ID,测点ID=v6ID+设备ID+测点ID,那个格式为:A=E1S12A23\n\
\n\
规则行格式:\n\
规则行格式需要加上标示符号,目前支持2个标识DATABASE|和TEMPLATE| \n\
DATABASE|标识:\n\
比如:DATABASE|JLJ(A)+JAVG(B)-JSUM(C)  这个代表用测点A的累计值 加上 测点B的平均值,减去测点C的和,A和B的来源于数据库\n\
这里可以使用公式\n\
JLJ这个函数会把数据库里面查询到的数据按照时间排序,然后最后一个值减去第一格式\n\
JMAX这个函数会把数据库里面查询到的数据的最大值返回\n\
JMIN这个函数会把数据库里面查询到的数据的最小值返回\n\
JNEW这个函数会把数据库里面查询到的数据的最新的值返回\n\
JOLD这个函数会把数据库里面查询到的数据的最早的值返回\n\
JAVG这个函数会把数据库里面查询到的数据的平均值返回\n\
JSUM这个函数会把数据库里面查询到的数据的所有数相加返回\n\
TEMPLATE|标识:\n\
TEMPLATE|A{}+B{}   如果是这个格式,会把TEMPLATE|后面的内容直接填入表格{}的值将会被行号替代\n\
\n                  "
        self.text_about='\n\
本版本完成基本日报功能，\n\
业余作品\n\
作者:谭润芝\n\
电话:13267153721\n\
v{}\n\
添加了一个按钮，链接到github主页\n\
v1.2\n\
解决bug:表格中日期处理的错误\n\
新增功能:检查最新版本功能\n\
v1.0\n\
基本报表查询功能'.format(self.vison)
