# -*- coding: utf_8 -*-
import requests
from datetime import date
import time
from os import path
from img import *
#import base64
from PyQt5.QtWidgets import (QTextEdit,QAction, qApp,QApplication,QMainWindow,QMessageBox,QDateTimeEdit,QComboBox,QFileDialog,QPushButton,QProgressBar,QGridLayout,QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,
        QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtCore import QCoreApplication,Qt ,QThread,pyqtSignal,QFileInfo
from PyQt5.QtGui import QPixmap,QIcon,QDesktopServices
import configparser
from g_data import bl
import decimal
from ri import ri
from zhou import zhou
from yue import yue
#####################################
from ctypes import windll
windll.shell32.SetCurrentProcessExplicitAppUserModelID("报表程序")
###########################
blc=bl()   ##放了一些变量,用来作于全局变量导入
###############C初始化config.ini这个配置文件#########################################
config = configparser.ConfigParser()
configdict={'server':{'host':'192.168.1.93','port':'3307','user':'gj','passwd':'xbrother','db':'historyver1'},
        'sheet_day':{'sjl':'A',"gzh":'3',"cj":'1',"mode":'0',"filename":''}
        }

if path.exists("config.ini"):  #如果配置文件存在,导入配置文件
    config.read("config.ini")
else:

    print('初始化配置文件')   #如果配置文件不存在,从初始字典里面导入配置文件
    config.read_dict(configdict)
    config.write(open("config.ini","w"))
##########################################################
#################初始化图标文件，如果图标文件不纯在，从base64编码里面释放该图标文件##################
#import ico
#def  sfico(iconame):
#    if not os.path.exists(iconame):
#        with open(iconame, 'wb+') as tmp:   #临时文件用来保存jpg文件  
#            tmp.write(base64.b64decode(ico.img[iconame.split('.')[0]]))
#            tmp.close()
#icolist=  ['save1.ico','title.jpg']    
#for i in icolist:
#    sfico(i)
##################################################
class TabDialog(QDialog):           ##########主界面
    def __init__(self, parent=None):
        super(TabDialog, self).__init__(parent)
        self.mustupdate=False
        self.creatico()
        self.creatui()
        self.creattab()
        self.checkvision()   #运行检查升级函数
    def creatico(self):
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
    def creatui(self):
        self.setWindowTitle('自定义报表程序')
        self.setGeometry(300,300,650,270) 
        #self.setFixedSize(self.width(), self.height())
        self.permissionsGroup = QGroupBox("服务器信息")
        self.permissionsLayout = QGridLayout()
        self.setWindowIcon(self.icon_title)
        ###############工具栏##########################
        self.qm=QMainWindow()
        exitAct = QAction(self.icon_save,"保存配置\nCtrl+S",self.qm)
        exitAct.setShortcut("Ctrl+S")
        exitAct.triggered.connect(self.saveconfig)
        self.toolbar = self.qm.addToolBar("save")
        exitAct1 = QAction(self.icon_help,"帮助\nCtrl+H",self.qm)
        exitAct1.setShortcut("Ctrl+H")
        exitAct1.triggered.connect(self.openhelp)
        exitAct2 = QAction(self.icon_aboat,"关于\nCtrl+I",self.qm)
        exitAct2.setShortcut("Ctrl+I")
        exitAct2.triggered.connect(self.openaboat)
        exitAct3 = QAction(self.icon_github,"查看源码\nCtrl+M",self.qm)
        exitAct3.setShortcut("Ctrl+M")
        exitAct3.triggered.connect(self.openaurl)
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(exitAct1)
        self.toolbar.addAction(exitAct2)
        self.toolbar.addAction(exitAct3)
        self.updatlabel=QLabel('',self.toolbar)
        self.updatlabel.setOpenExternalLinks(True)
        self.updatlabel.setFixedWidth(150)
        self.toolbar.addWidget(self.updatlabel)
        self.toolbar.setMovable(False)
        #self.toolbar.setFloatable(False)
        ###############服务器信息###############
        self.permissionsLayout.addWidget(QLabel('数据库',self.permissionsGroup),1,0 )
        self.le_host=QLineEdit('',self.permissionsGroup)
        self.le_host.editingFinished.connect(self.initserver)
        self.le_host.setInputMask('000.000.000.000')
        self.le_host.insert(config['server']['host'])
        self.le_host.setFixedWidth(100)
        self.le_host.setToolTip('这里要填数据库的IP')
        #print((self.le_host.height(),self.le_host.width()))
        self.permissionsLayout.addWidget(QLabel('端口',self.permissionsGroup),1,2 )
        self.le_port=QLineEdit('',self.permissionsGroup)
        self.le_port.setInputMask('99999')
        self.le_port.insert(config['server']['port'])
        self.le_port.editingFinished.connect(self.initserver)
        self.le_port.setFixedWidth(40)
        self.le_port.setToolTip('这里要填数据库的端口\n中联默认1443\n共济默认3307\n栅格默认3306')
        self.permissionsLayout.addWidget(QLabel('用户名',self.permissionsGroup),1,4)
        self.le_usr=QLineEdit('',self.permissionsGroup)
        self.le_usr.insert(config['server']['user'])
        self.le_usr.editingFinished.connect(self.initserver)
        self.le_usr.setFixedWidth(40)
        self.le_usr.setToolTip('这里要填数据库的用户名\n中联默认sa\n共济默认gj\n栅格默认mysql')
        self.permissionsLayout.addWidget(QLabel('密码',self.permissionsGroup),1,6 )
        self.le_passwd=QLineEdit('',self.permissionsGroup)
        self.le_passwd.insert(config['server']['passwd'])
        self.le_passwd.editingFinished.connect(self.initserver)
        self.le_passwd.setFixedWidth(100)
        self.le_passwd.setToolTip('这里要填数据库的密码\n中联无默认值\n共济默认xbrother\n栅格默认mysql')
        self.le_passwd.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.permissionsLayout.addWidget(QLabel('数据库名',self.permissionsGroup),1,8 )
        self.le_db=QLineEdit('',self.permissionsGroup)
        self.le_db.insert(config['server']['db'])
        self.le_db.setFixedWidth(80)
        self.le_db.setToolTip('这里要填数据库名\n中联无默认值\n共济默认historyver1\n栅格默认sgdatabase') 
        self.le_db.editingFinished.connect(self.initserver)
        ##################################
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
    def creattab(self):
        self.tabWidget = QTabWidget()
        self.ts1=ri(config)
        self.ts2=zhou()
        self.ts3=yue()
        self.tabWidget.addTab(self.ts1, "日报")
        self.mainLayout.addWidget(self.tabWidget)
        self.tabWidget.addTab(self.ts2, "周报")
        self.mainLayout.addWidget(self.tabWidget)
        self.tabWidget.addTab(self.ts3, "月报")
        self.mainLayout.addWidget(self.tabWidget)
    ###################检测版本########################################
    def compare(self,a, b):  #比较版本号函数
        la = a.split('.')
        lb = b.split('.')
        f = 0
        if len(la) > len(lb):
            f = len(la)
        else:
            f = len(lb)
        for i in range(f):
            try:
                if  int(la[i]) > int(lb[i]):
                    return '>'
                elif int(la[i]) == int(lb[i]):
                    continue
                else:
                    if i==0:
                        self.mustupdate=True
                    else:
                        return '<'
            except IndexError as e:
                if len(la) > len(lb):
                    return '>'
                else:
                    return '<'
        return '='
    def  checkvision(self):  # 在线获取版本号
        try:
            url='http://wechat.52hengshan.com/weixin/api/v1.0/appvison'
            s=requests.get(url=url,timeout=2).json()
        except:
            self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#00ff00;\">无法联网查找最新版本</span></a></p></body></html>")
        else:
            blc_vi=self.compare(blc.vison,s['vison'])
            if blc_vi == '=':
                self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#0000ff;\">已经是最新版本</span></a></p></body></html>")
            elif blc_vi == '>' and not self.mustupdate:self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#0000ff;\">你这个是内部版本吧<br>居然比发布版本要高</span></a></p></body></html>")
            elif blc_vi == '<' and not self.mustupdate:self.updatlabel.setText("<html><head/><body><p><a href=\"{}\"><span style=\" text-decoration: underline; color:#ff0000;\">有最新版本,点此升级</span></a></p></body></html>".format(s['url']))
            elif blc_vi == '<' and  self.mustupdate:
                self.tabWidget.setEnabled(False)
                self.updatlabel.setText("<html><head/><body><p><a href=\"{}\"><span style=\" text-decoration: underline; color:#ff0000;\">此版本有重大风险<br>不建议使用，必须升级</span></a></p></body></html>".format(s['url']))
    def initserver(self):   ##########从主界面获取的数据存入全局变量
        blc.host=self.le_host.text()
        blc.port=int(self.le_port.text())
        blc.usr=self.le_usr.text()
        blc.passwd=self.le_passwd.text()
        blc.db=self.le_db.text()
        self.ts1.initserverinfo(blc.host,blc.port,blc.usr,blc.passwd,blc.db)

    def openaboat(self):   #######关于菜单的弹窗内容
        self.wid1 = QMainWindow() 
        self.wid1.setWindowTitle('关于')  
        self.wid1.setGeometry(300,300,300,300)
        self.wid1.setWindowIcon(self.icon_aboat)    
        reviewEdit = QTextEdit(self.wid1 )
        reviewEdit.setGeometry(0,0,300,300) 
        self.wid1.setFixedSize(self.wid1.width(), self.wid1.height())
        reviewEdit.setPlainText(blc.text_about)
        reviewEdit.setReadOnly(True)
        self.wid1.show()
    def openaurl(self):
        QDesktopServices.openUrl(QtCore.QUrl('https://github.com/trz0332/bmsreport'))
    def openhelp(self):          ##帮助菜单的弹窗内容
        if path.exists("help.txt"):    #判断help.txt是否存在，如果存在获取帮助文本里面的内容，填充到文本编辑控件显示
            with open('help.txt','r') as fb:
                blc.text_help=fb.read()
        else:
            with open('help.txt','a') as fb:   #如果帮助文本不存下，从默认的帮助变量获取文本，保存到help.txt
                fb.write(blc.text_help)
        self.wid = QMainWindow() 
        self.wid.setWindowTitle('帮助')  #帮助窗口标题
        self.wid.setGeometry(300,300,600,400)   #帮助窗口大小
        self.wid.setWindowIcon(self.icon_help)    #帮助窗口图标
        self.reviewEdit = QTextEdit(self.wid )   #定义一个文本编辑控件
        self.reviewEdit.setGeometry(0,0,600,400)   #设置文本编辑控件大小
        self.wid.setFixedSize(self.wid.width(), self.wid.height())  #设置固定大小不允许改变
        self.reviewEdit.setPlainText(blc.text_help)   #帮助文本的内容填入到文本编辑框
        self.reviewEdit.setReadOnly(True)   #制度模式
        self.wid.show()   #展示窗口
    def saveconfig(self):  #保存配置到config.ini
        config.set('server','host',self.le_host.text())
        config.set('server','port',self.le_port.text())
        config.set('server','user',self.le_usr.text())
        config.set('server','passwd',self.le_passwd.text())
        config.set('server','db',self.le_db.text())
        config.set('sheet_day','sjl',self.ts1.sjl.text())
        config.set('sheet_day','gzh',self.ts1.gzh.text())
        config.set('sheet_day','cj',str(self.ts1.jsComboBox.currentIndex()))
        config.set('sheet_day','mode',str(self.ts1.js2ComboBox.currentIndex()))
        config.set('sheet_day','mode',str(self.ts1.js2ComboBox.currentIndex()))
        config.set('sheet_day','filename',str(self.ts1.qtfile.text()))
        with open("config.ini","w") as fh:
            config.write(fh)
        QMessageBox.information(self, "信息", "配置文件保存成功",QMessageBox.Yes)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tabdialog = TabDialog()
    tabdialog.show()
    sys.exit(app.exec_())



