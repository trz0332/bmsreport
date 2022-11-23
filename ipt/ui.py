# -*- coding: utf_8 -*-

import requests
#import datetime 
import time
import os
from os import path
import sys
from . import img 
#import base64
from PyQt5.QtWidgets import (QTextEdit,QAction, qApp,QApplication,QMainWindow,QMessageBox,QDateTimeEdit,QComboBox
    ,QFileDialog,QPushButton,QProgressBar,QGridLayout,QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,
        QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtCore import QCoreApplication,Qt ,QThread,pyqtSignal,QFileInfo,qRegisterResourceData,QUrl
from PyQt5.QtGui import QPixmap,QIcon,QDesktopServices,QPalette,QColor
#import configparser
from .g_data  import bl
#import decimal
from .ri import ri
from .zjyaml import *
from . import update
#from zhou import zhou
#from yue import yue 
#from ctypes import windll
#windll.shell32.SetCurrentProcessExplicitAppUserModelID("报表程序")
###########################
blc=bl()   ##放了一些变量,用来作于全局变量导入
blc.conf_fn='config.yaml'
###############C初始化config.ini这个配置文件#########################################
config={'server':{'host':'172.31.169.81','port':'31002','user':'mysql','passwd':'xbrother','db':'sgdatabase'},
        'sheet_day':{'sjl':'A',"gzh":'3',"cj":'1',"mode":'1',"filename":'C:/Users/MOGU/Desktop/写的小工具/byq.xlsx'},
        'ui':{'color':'#FFFFE2'}}

if path.exists(".\config.yaml"):  #如果配置文件存在,导入配置文件
    config=loadyaml(blc.conf_fn)
else:
    print('初始化配置文件')   #如果配置文件不存在,从初始字典里面导入配置文件
    saveyaml(config,blc.conf_fn)
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
        self.config=config
        self.setWindowOpacity(0.9)  #设置透明
        self.creatico()  #创建图标
        self.creatui()
        self.creattab()   #运行检查升级函数QMainWindow
    def creatico(self):
        self.icon_title = QIcon()
        self.icon_title.addPixmap(QPixmap(":/img/icon_mogu.png"), QIcon.Normal, QIcon.Off)   #标题图表
        self.icon_save = QIcon()
        self.icon_save.addPixmap(QPixmap(":/img/icon_save.png"), QIcon.Normal, QIcon.Off)  #保存图表
        self.icon_help=QIcon()
        self.icon_help.addPixmap(QPixmap(":/img/icon_help.png"), QIcon.Normal, QIcon.Off)  # 帮助图表
        self.icon_aboat = QIcon()
        self.icon_aboat.addPixmap(QPixmap(":/img/icon_aboat.png"), QIcon.Normal, QIcon.Off)  #关于图表
        self.icon_github = QIcon()
        self.icon_github.addPixmap(QPixmap(":/img/icon_github.png"), QIcon.Normal, QIcon.Off)  #github图表
        self.icon_open = QIcon()
        self.icon_open.addPixmap(QPixmap(":/img/icon_open.png"), QIcon.Normal, QIcon.Off)  #github图表
    def creatui(self):

        self.setWindowTitle('自定义报表程序    name:{}|mail:{}|ver:{}'.format(blc.name,blc.mail,blc.vison))
        self.setGeometry(300,300,650,270) 
        ######################################
        self.pal=QPalette()
        #self.pal.setColor(self.backgroundRole(),QColor('red'))
        self.pal.setColor(self.backgroundRole(),QColor('{}'.format(self.config['ui']['color'])))
        #self.bj1=QPixmap('183.png')
        #print(help(self.bj1))
        #self.bj1.scaled(1254,420, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #self.pal.setBrush(self.backgroundRole(),QBrush(self.bj1))
        self.setPalette(self.pal)
        self.setWindowFlags(Qt.Widget)  #设置窗口样式
        self.setAutoFillBackground(True)  #
        ##########################################

        #self.setFixedSize(self.width(), self.height())
        self.permissionsGroup = QGroupBox("服务器信息")
        self.permissionsLayout = QGridLayout()
        self.setWindowIcon(self.icon_title)
        #palette1.setBrush(w.backgroundRole(), QtGui.QBrush(image)) #背景图片
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
        exitAct4 = QAction(self.icon_open,"加载配置文件\nCtrl+O",self.qm)
        exitAct4.setShortcut("Ctrl+O")
        exitAct4.triggered.connect(self.openconfig)
        self.toolbar.addAction(exitAct4)
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
        self.le_host.insert(self.config['server']['host'])
        self.le_host.setFixedWidth(100)
        self.le_host.setToolTip('这里要填数据库的IP')
        #print((self.le_host.height(),self.le_host.width()))
        self.permissionsLayout.addWidget(QLabel('端口',self.permissionsGroup),1,2 )
        self.le_port=QLineEdit('',self.permissionsGroup)
        self.le_port.setInputMask('99999')
        self.le_port.insert(self.config['server']['port'])
        self.le_port.editingFinished.connect(self.initserver)
        self.le_port.setFixedWidth(40)
        self.le_port.setToolTip('这里要填数据库的端口\n中联S80默认1443\n中联S90默认27017\n共济V7默认3307\n共济KE默认8888\n栅格默认3306\n中联S90和攻击KE默认不允许其他IP连接数据库需要修改数据库配置文件bind: 127.0.0.1改为 bind: 0.0.0.0')
        self.permissionsLayout.addWidget(QLabel('用户名',self.permissionsGroup),1,4)
        self.le_usr=QLineEdit('',self.permissionsGroup)
        self.le_usr.insert(self.config['server']['user'])
        self.le_usr.editingFinished.connect(self.initserver)
        self.le_usr.setFixedWidth(40)
        self.le_usr.setToolTip('这里要填数据库的用户名\n中联默认sa\n共济默认gj\n栅格默认mysql\n中联S90默认无用户名\n共济KE默认无用户名')
        self.permissionsLayout.addWidget(QLabel('密码',self.permissionsGroup),1,6 )
        self.le_passwd=QLineEdit('',self.permissionsGroup)
        self.le_passwd.insert(self.config['server']['passwd'])
        self.le_passwd.editingFinished.connect(self.initserver)
        self.le_passwd.setFixedWidth(100)
        self.le_passwd.setToolTip('这里要填数据库的密码\n中联无默认值\n共济默认xbrother\n栅格默认mysql\n中联S90默认无密码\n共济KE默认无密码')
        self.le_passwd.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.permissionsLayout.addWidget(QLabel('数据库名',self.permissionsGroup),1,8 )
        self.le_db=QLineEdit('',self.permissionsGroup)
        self.le_db.insert(self.config['server']['db'])
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
        self.config['color']=blc.color
        self.ts1=ri(self.config)
        #self.ts2=zhou()
        #self.ts3=yue(config)
        self.tabWidget.addTab(self.ts1, "日报")
        self.mainLayout.addWidget(self.tabWidget)
        #self.tabWidget.addTab(self.ts2, "周报")
        #self.mainLayout.addWidget(self.tabWidget)
        #self.tabWidget.addTab(self.ts3, "月报")
        #self.mainLayout.addWidget(self.tabWidget)
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
            s=update.get_version()
            blc_vi=self.compare(blc.vison,s['ver'])
            if blc_vi == '=':
                self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#000000;\">已经是最新版本</span></a></p></body></html>")
            elif blc_vi == '>' and not self.mustupdate:
                self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#0000ff;\">你这个是内部版本吧<br>居然比发布版本要高</span></a></p></body></html>")
            elif blc_vi == '<' and not self.mustupdate:
                #QMessageBox.information(self, "信息", "有最新版本{}\n{}".format(s['ver'],s['info']),QMessageBox.Yes)
                button=QMessageBox.question(self,"Question","检查新版本{},是否升级\n本次更新{}".format(s['ver'],s['info']),
                                          QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
                if button == QMessageBox.Ok:
                    filelist,ver=update._update(s)
                    if filelist:
                        update.upgru(filelist,ver)
                        QMessageBox.about(self, '提示', '更新完成，请重新启动程序')
                        python = sys.executable
                        #self.setWindowTitle("腾讯TBlock监控-厂验辅助工具V{}(最新版本)".format(ver_info['ver']))
                        os.execl(python, python, * sys.argv)
                    else:
                        QMessageBox.about(self, '提示', '下载失败，请手动更新2')
                elif button == QMessageBox.Cancel:
                    #self.setWindowTitle("腾讯TBlock监控-厂验辅助工具V{}(有最新版本{})".format(local_info['ver'],ver_info['ver']))
                #QMessageBox.information(self, "信息", "有最新版本{}\n{}".format(s['vison'],s['info']),QMessageBox.Yes)
                    self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#ff0000;\">有最新版本{}</span></a></p></body></html>".format(s['ver']))
            #url='http://wechat.52hengshan.com:6000/weixin/api/v1.0/appvison'
            #s=requests.get(url=url,timeout=1).json()
        except Exception as e:
            print(e)
            self.updatlabel.setText("<html><head/><body><p><span style=\" text-decoration: underline; color:#00ff00;\">无法联网查找最新版本</span></a></p></body></html>")


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
        QDesktopServices.openUrl(QUrl('https://github.com/trz0332/bmsreport'))
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
        #config.set('server','host',self.le_host.text())
        config['server']['host']=self.le_host.text()
        #config.set('server','port',self.le_port.text())
        config['server']['port']=self.le_port.text()
        #config.set('server','user',self.le_usr.text())
        config['server']['user']=self.le_usr.text()
        #config.set('server','passwd',self.le_passwd.text())
        config['server']['passwd']=self.le_passwd.text()
        #config.set('server','db',self.le_db.text())
        config['server']['db']=self.le_db.text()
        #config.set('sheet_day','sjl',self.ts1.sjl.text())
        config['sheet_day']['sjl']=self.ts1.sjl.text()
        #config.set('sheet_day','gzh',self.ts1.gzh.text())
        config['sheet_day']['gzh']=self.ts1.gzh.text()
        #config.set('sheet_day','cj',str(self.ts1.jsComboBox.currentIndex()))
        config['sheet_day']['cj']=self.ts1.jsComboBox.currentIndex()
        #config.set('sheet_day','mode',str(self.ts1.js2ComboBox.currentIndex()))
        config['sheet_day']['mode']=self.ts1.js2ComboBox.currentIndex()
        config['sheet_day']['save_mode']=self.ts1.save_mode.isChecked()
        config['sheet_day']['sn_check']={}
        #print(len(self.ts1.sheet_name))
        #print(path.exists(self.config['sheet_day']['filename']))
        if not path.exists(self.config['sheet_day']['filename']):
            config['sheet_day']['sn_check']={}
        else:
            for index,i in enumerate(self.ts1.sheet_name):
                config['sheet_day']['sn_check'][i]=[x.isChecked() for x in self.ts1.c_cheetname_ck][index]


        #config.set('sheet_day','filename',str(self.ts1.qtfile.text()))
        config['sheet_day']['filename']=str(self.ts1.qtfile.text())
        saveyaml(config,blc.conf_fn)
        QMessageBox.information(self, "信息", "配置文件保存成功",QMessageBox.Yes)
    def openconfig(self):  #保存配置到config.ini
        # absolute_path is a QString object  
        blc.conf_fn, self.filetype = QFileDialog.getOpenFileName(self,
                                            "选取文件",  
                                            "",  
                                            "yaml (*.yaml)")   #设置文件扩展名过滤,注意用双分号间隔  
        if blc.conf_fn=='':pass
        else :
            self.config=loadyaml(blc.conf_fn)
            self.le_host.setText(self.config['server']['host'])
            #self.le_host.insert(self.config['server']['host'])
            #config['server']['port']=self.le_port.text()
            self.le_port.setText(self.config['server']['port'])
            #config['server']['user']=self.le_usr.text()
            self.le_usr.setText(self.config['server']['user'])
            #config['server']['passwd']=self.le_passwd.text()
            self.le_passwd.setText(self.config['server']['passwd'])
            #config['server']['db']=self.le_db.text()
            self.le_db.setText(self.config['server']['db'])
            #config['sheet_day']['sjl']=self.ts1.sjl.text()
            self.ts1.sjl.setText(self.config['sheet_day']['sjl'])
            #config['sheet_day']['gzh']=self.ts1.gzh.text()
            self.ts1.gzh.setText(self.config['sheet_day']['gzh'])
            #config['sheet_day']['cj']=self.ts1.jsComboBox.currentIndex()
            self.ts1.jsComboBox.setCurrentIndex(int(config['sheet_day']['cj']))
            #config['sheet_day']['mode']=self.ts1.js2ComboBox.currentIndex()
            self.ts1.js2ComboBox.setCurrentIndex(int(config['sheet_day']['mode']))
            self.ts1.save_mode.setChecked(config['sheet_day']['save_mode'] if 'save_mode' in  config['sheet_day'].keys() else False)
            #config['sheet_day']['filename']=str(self.ts1.qtfile.text())
            self.ts1.qtfile.setText(self.config['sheet_day']['filename'])
            self.ts1.creatsheetCheckBox()

def run():
    
    app = QApplication(sys.argv)
    tabdialog = TabDialog()
    tabdialog.show()
    tabdialog.checkvision()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tabdialog = TabDialog()
    tabdialog.show()
    tabdialog.checkvision()
    sys.exit(app.exec_())



