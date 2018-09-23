from PyQt5.QtWidgets import (QTextEdit,QAction, qApp,QApplication,QMainWindow,QMessageBox,QDateTimeEdit,QComboBox,QFileDialog,QPushButton,QProgressBar,QGridLayout,QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,
        QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtCore import QCoreApplication,Qt,QDateTime,QDate,QTime  ,QThread,pyqtSignal,QFileInfo
from PyQt5.QtGui import QPixmap,QIcon,QDesktopServices
import configparser
from os import path
import sys
import img
from mssql import MSSQL
import decimal




###############C初始化config.ini这个配置文件#########################################
config = configparser.ConfigParser()
configdict={'server':{'host':'192.168.1.91','port':'1433','user':'sa','passwd':'ABCabc123','db':'MJSQL3.0'},

        }

if path.exists("config1.ini"):  #如果配置文件存在,导入配置文件
    config.read("config1.ini")
else:

    print('初始化配置文件')   #如果配置文件不存在,从初始字典里面导入配置文件
    config.read_dict(configdict)
    config.write(open("config1.ini","w"))
##########################################################
class TabDialog(QDialog):           ##########主界面
    def __init__(self, parent=None):
        super(TabDialog, self).__init__(parent)
        self.creatui()
    def creatui(self):
        self.icon_title = QIcon()
        self.icon_title.addPixmap(QPixmap(":/img/title.ico"), QIcon.Normal, QIcon.Off)   #标题图表
        self.icon_save = QIcon()
        self.icon_save.addPixmap(QPixmap(":/img/save.ico"), QIcon.Normal, QIcon.Off)  #保存图表
        self.icon_help=QIcon()
        self.icon_help.addPixmap(QPixmap(":/img/help.ico"), QIcon.Normal, QIcon.Off)  # 帮助图表
        self.icon_aboat = QIcon()
        self.icon_aboat.addPixmap(QPixmap(":/img/about.ico"), QIcon.Normal, QIcon.Off)  #关于图表
        self.icon_github = QIcon()
        self.icon_github.addPixmap(QPixmap(":/img/github.ico"), QIcon.Normal, QIcon.Off)  #关于图表
        self.setWindowTitle('自定义报表程序')
        self.setGeometry(300,300,650,270) 
        #self.setFixedSize(self.width(), self.height())
        self.permissionsGroup = QGroupBox("服务器信息")
        self.permissionsLayout = QGridLayout()
        self.setWindowIcon(self.icon_title)
        #########################################
        self.qm=QMainWindow()
        exitAct = QAction(self.icon_save,"保存配置",self.qm)
        exitAct.setShortcut("Ctrl+S")
        exitAct.triggered.connect(self.saveconfig)
        self.toolbar = self.qm.addToolBar("save")
        exitAct1 = QAction(self.icon_help,"帮助",self.qm)
        exitAct1.setShortcut("Ctrl+H")
        exitAct1.triggered.connect(self.openhelp)
        exitAct2 = QAction(self.icon_aboat,"关于",self.qm)
        exitAct2.setShortcut("Ctrl+I")
        exitAct2.triggered.connect(self.openaboat)
        exitAct3 = QAction(self.icon_github,"查看源码",self.qm)
        exitAct3.setShortcut("Ctrl+M")
        exitAct3.triggered.connect(self.openaurl)
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(exitAct1)
        self.toolbar.addAction(exitAct2)
        self.toolbar.addAction(exitAct3)
        self.updatlabel=QLabel('',self.toolbar)
        self.updatlabel.setOpenExternalLinks(True)
        self.updatlabel.setFixedWidth(150)
        self.updatlabel.move(500,0)
        ###############第一行###############
        self.permissionsLayout.addWidget(QLabel('数据库',self.permissionsGroup),1,0 )
        self.le_host=QLineEdit('',self.permissionsGroup)
        #self.le_host.editingFinished.connect(self.initserver)
        self.le_host.setInputMask('000.000.000.000')
        self.le_host.insert(config['server']['host'])
        self.le_host.setFixedWidth(100)
        #print((self.le_host.height(),self.le_host.width()))
        self.permissionsLayout.addWidget(QLabel('端口',self.permissionsGroup),1,2 )
        self.le_port=QLineEdit('',self.permissionsGroup)
        self.le_port.setInputMask('99999')
        self.le_port.insert(config['server']['port'])
        #self.le_port.editingFinished.connect(self.initserver)
        self.le_port.setFixedWidth(40)
        self.permissionsLayout.addWidget(QLabel('用户名',self.permissionsGroup),1,4)
        self.le_usr=QLineEdit('',self.permissionsGroup)
        self.le_usr.insert(config['server']['user'])
        #self.le_usr.editingFinished.connect(self.initserver)
        self.le_usr.setFixedWidth(40)
        self.permissionsLayout.addWidget(QLabel('密码',self.permissionsGroup),1,6 )
        self.le_passwd=QLineEdit('',self.permissionsGroup)
        self.le_passwd.insert(config['server']['passwd'])
        #self.le_passwd.editingFinished.connect(self.initserver)
        self.le_passwd.setFixedWidth(100)
        self.le_passwd.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.permissionsLayout.addWidget(QLabel('数据库名',self.permissionsGroup),1,8 )
        self.le_db=QLineEdit('',self.permissionsGroup)
        self.le_db.insert(config['server']['db'])
        self.le_db.setFixedWidth(80)
        #self.le_db.editingFinished.connect(self.initserver)
        ##################################
        self.permissionsLayout.addWidget(QLabel('设备名',self.permissionsGroup),2,0 )
        self.le_devname=QLineEdit('',self.permissionsGroup)
        self.permissionsLayout.addWidget(self.le_devname,2,1,1,8)
        self.le_devname.setFixedWidth(600)
        self.qtb1=QPushButton('查询',self)
        self.permissionsLayout.addWidget(self.qtb1,2,9)
        self.qtb1.clicked.connect(self.work)
        ##############################
        self.permissionsLayout.addWidget(self.le_host,1,1)
        self.permissionsLayout.addWidget(self.le_port,1,3)
        self.permissionsLayout.addWidget(self.le_usr,1,5)
        self.permissionsLayout.addWidget(self.le_passwd,1,7)
        self.permissionsLayout.addWidget(self.le_db,1,9)
        self.permissionsGroup.setLayout(self.permissionsLayout)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.qm)
        self.mainLayout.addWidget(self.permissionsGroup)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)


        self.reviewEdit = QTextEdit(self )   #定义一个文本编辑控件
        self.mainLayout.addWidget(self.reviewEdit)
        self.reviewEdit.setPlainText('')   #帮助文本的内容填入到文本编辑框
        self.ts=zldatbase()
    def initserver(self):
        pass
    def openaurl(self):
        pass
    def openaboat(self):
        pass
    def openhelp(self):
        pass
    def work(self):
        self.qtb1.setEnabled(False)
        self.ts.init(self.le_host.text(),int(self.le_port.text()),self.le_usr.text(),self.le_passwd.text(),self.le_db.text())
        tx=self.ts.main(self.le_devname.text())
        self.reviewEdit.setPlainText(tx)
        self.qtb1.setEnabled(True)
        QMessageBox.information(self, "信息", "查询成功",QMessageBox.Yes)
    def saveconfig(self):
        config.set('server','host',self.le_host.text())
        config.set('server','port',self.le_port.text())
        config.set('server','user',self.le_usr.text())
        config.set('server','passwd',self.le_passwd.text())
        config.set('server','db',self.le_db.text())
        with open("config.ini","w") as fh:
            config.write(fh)

        QMessageBox.information(self, "信息", "配置文件保存成功",QMessageBox.Yes)
class zldatbase():
    def init(self,server,port,user,passwd,db):
        self.count=1
        self.ms=MSSQL(host=server,port=port,user=user,pwd=passwd,db=db)
        #print(server,port,user,passwd,db)
    def name_get_id(self,name):
        sql="SELECT nID,strFullName  from NameObject WHERE strFullName like '%{}%'".format(name)
        try:
            reslist = self.ms.ExecQuery(sql) 
        except:
            return False
        else:return reslist
    def id_get_name(self,devid):  #根据ID查找名
        sql= "SELECT strfullname  FROM nameobject where nid like '{}'".format(devid)
        #print(sql)
        res=self.ms.ExecQuery(sql)
        #print(res,789)
        self.count+=1
        if res :
            if res[0][0]:
                return res[0][0]
            else:'未知设备'
        else:return '未知设备'
    def main(self,name):
        res=self.name_get_id(name)
        #print(res)
        text=''
        if res:
            for i in res:
                #print(i)
                text1=''
                text1+='|||本级设备名: '+i[1]+' '+'本级设备ID: '+'    '+str(i[0])
                upid=self.checkcont(i[0])
                #print(upid,123)
                upname=self.id_get_name(upid)
                #print(upname,234)
                text1='上级设备名: '+upname+' 上级设备ID: '+str(upid)+'    '+text1 +'\n'
                #print(text1)
                text+=text1
            return text
        else: return '没有查询到任何设备'
    def checkcont(self,devid):  #查询设备关系表

        sql="SELECT * from Container where nSubObjectID = {}".format(devid)
        try:
            res=self.ms.ExecQuery(sql)
            #print(res)
            self.count+=1
        except:return '未知设备'
        else:
            for i in res:
                if i[1]==62:return i[0]
                else :pass
    




    
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)


    tabdialog = TabDialog()
    tabdialog.show()
    sys.exit(app.exec_())

