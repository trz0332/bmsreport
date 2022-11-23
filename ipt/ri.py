
from PyQt5.QtCore import QDateTime,QDate,QTime  ,QThread,pyqtSignal,QFileInfo,Qt
from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QGridLayout,QGroupBox,QLabel,QLineEdit
    ,QPushButton,QComboBox,QDateTimeEdit,QProgressBar,QMessageBox,QFileDialog,QMainWindow,QCheckBox,  QApplication)
from PyQt5.QtGui import QPixmap,QIcon,QDesktopServices,QPalette,QColor
import time
from .wt_ri import WorkThread
from os import path
from openpyxl import load_workbook
import sip
import gc

lc=locals()
class ri(QWidget):    #日报table框组建
    def __init__(self,config,parent=None):
        super(ri, self).__init__(parent)
        self.color=config['ui']['color']
        if 'sn_check' in config['sheet_day'].keys():
            self.sn_check=config['sheet_day']['sn_check']
        else:self.sn_check={}
        self.workThread=WorkThread()    #多线程
        self.workThread.sinOut.connect(self.setp)  #多线程链接信号输出
        layout = QGridLayout()  #创建一个表格排列
        self.pal1=QPalette()
        #self.pal.setColor(self.backgroundRole(),QColor('red'))
        self.pal1.setColor(self.backgroundRole(),QColor('{}'.format(self.color)))
        #self.bj1=QPixmap('183.png')
        #print(help(self.bj1))
        #self.bj1.scaled(1254,420, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #self.pal.setBrush(self.backgroundRole(),QBrush(self.bj1))
        self.setPalette(self.pal1)
        #self.setWindowFlags(Qt.Widget)  #设置窗口样式
        self.setAutoFillBackground(True)  #

        self.sheetbox = QGroupBox("表名")
        self.sheetbox_lo=QGridLayout()
        self.sheetbox.setLayout(self.sheetbox_lo)
        self.rp_config = QGroupBox("日报配置")
        self.rp_config_lo=QGridLayout()
        self.rp_config.setLayout(self.rp_config_lo)
        layout.addWidget(self.sheetbox,0,0)
        layout.addWidget(self.rp_config,1,0)

        self.fileName1=''
        ###############第一行 文件选择框
        ########
        self.rp_config_lo.addWidget(QLabel('报表文件',self.rp_config),0,0 )
        self.qtfile=QLineEdit('',self.rp_config)
        self.qtfile.insert(config['sheet_day']['filename'] if 'filename' in  config['sheet_day'].keys() else '')
        self.qtfile.editingFinished.connect(self.creatsheetCheckBox)
        self.qbfile=QPushButton('选择文件',self.rp_config)
        self.qbfile.clicked.connect(self.button_click)
        self.qbfile.setEnabled(True)
        self.rp_config_lo.addWidget(self.qtfile,0,1,1,5)
        self.rp_config_lo.addWidget(self.qbfile,0,6)

        self.save_mode=QCheckBox(self.rp_config)
        #self.save_mode.setObjectName()
        self.save_mode.setText('是否另存为')
        self.save_mode.setStatusTip('是否另存为')
        self.save_mode.setChecked(config['sheet_day']['save_mode'] if 'save_mode' in  config['sheet_day'].keys() else False)
        #print(self.save_mode.isChecked())
        self.rp_config_lo.addWidget(self.save_mode,0,7)
        ######################第二行################################################
        self.rp_config_lo.addWidget(QLabel('规则',self.rp_config) ,1,0)
        self.gzh=QLineEdit('',self.rp_config)
        self.gzh.insert(config['sheet_day']['gzh'])
        self.gzh.setFixedWidth(40)
        self.rp_config_lo.addWidget(QLabel('时间',self.rp_config) ,1,2)
        self.sjl=QLineEdit('',self.rp_config)
        self.sjl.insert(config['sheet_day']['sjl'])
        self.sjl.setFixedWidth(40)
        self.rp_config_lo.addWidget(QLabel('BMS厂家',self.rp_config) ,1,4)
        jslist=['共济V7','共济KE','中联S80','中联S90','栅格','栅格clickhouse']
        self.jsComboBox=QComboBox(self.rp_config)   #下拉菜单
        for i in jslist:
            self.jsComboBox.addItem(i)
        self.jsComboBox.setCurrentIndex(int(config['sheet_day']['cj']))
        self.rp_config_lo.addWidget(QLabel('模式',self.rp_config),1,6)
        jslist2=['0--寻找日期','1--最后填充']
        self.js2ComboBox=QComboBox(self.rp_config)   #下拉菜单
        for i in jslist2:
            self.js2ComboBox.addItem(i)
        self.js2ComboBox.setCurrentIndex(int(config['sheet_day']['mode']))
        self.rp_config_lo.addWidget(self.gzh,1,1)
        self.rp_config_lo.addWidget(self.sjl,1,3)
        self.rp_config_lo.addWidget(self.jsComboBox,1,5)
        self.rp_config_lo.addWidget(self.js2ComboBox,1,7)
        ######################第三行时间选择行#############################
        self.rp_config_lo.addWidget(QLabel('起始时间',self.rp_config),2,0)
        self.dt1 = QDateTimeEdit(QDate.currentDate(),self.rp_config) # 创建日期，并初始值  
        self.dt1.setDisplayFormat('yyyy-MM-dd')
        #self.dt1.setMinimumDate(QDate.currentDate().addDays(-90)) # 限定时间最小值，当前时间-365天  
        self.dt1.setMaximumDate(QDate.currentDate().addDays(1)) # 限定时间最大值，当前时间+365天  
        self.dt1.setCalendarPopup(True) # 允许弹出窗口选择日期，setMinimumDate()的限定对这个窗口也有效  
        # #############结束时间选择 
        self.rp_config_lo.addWidget(QLabel('结束时间',self.rp_config),2,4)
        self.dt2 = QDateTimeEdit(QDate.currentDate(),self.rp_config) # 创建日期，并初始值  
        self.dt2.setDate(QDate.currentDate())  
        #self.dt2.setMinimumDate(QDate.currentDate().addDays(-90)) # 限定时间最小值，当前时间-365天  
        self.dt2.setMaximumDate(QDate.currentDate().addDays(1)) # 限定时间最大值，当前时间+365天  
        self.dt2.setCalendarPopup(True) # 允许弹出窗口选择日期，setMinimumDate()的限定对这个窗口也有效  

        ###########查询按钮###########
        self.qtb1=QPushButton('查询',self.rp_config)
        self.qtb1.clicked.connect(self.work)
        
        self.rp_config_lo.addWidget(self.dt1,2,1,1,3)
        self.rp_config_lo.addWidget(self.dt2,2,5,1,2)
        self.rp_config_lo.addWidget(self.qtb1,2,7)

        #######第四行进度条
        self.rp_config_lo.addWidget(QLabel('进度',self.rp_config),3,0 )
        self.pbar = QProgressBar(self.rp_config)
        #self.pbar.setFixedWidth(560)
        self.rp_config_lo.addWidget(self.pbar,3,1,1,6 )
        self.setLayout(layout)
        self.creatsheetCheckBox()
    def creatsheetCheckBox(self):
        self.c_cheetname_ck=[]
        qlist=self.sheetbox.findChildren((QCheckBox,QLabel))
        #print(help(self.sheetbox_lo))
        for i in qlist:
            self.sheetbox_lo.removeWidget(i)
            sip.delete(i)
        filename=str(self.qtfile.text())
        if not path.exists(filename):
            self.sheetbox_lo.addWidget(QLabel('文件不存在',self.sheetbox),0,0)
        else:
            wb=load_workbook(filename)
            self.sheet_name=wb.get_sheet_names()
            for index , i in enumerate(self.sheet_name):
                lc[i]=QCheckBox(self.sheetbox)
                lc[i].setObjectName(i)
                lc[i].setText( i)
                lc[i].setStatusTip(i)
                if i in self.sn_check.keys():
                    if self.sn_check[i]:
                        lc[i].setChecked(True)
                    else:lc[i].setChecked(False)
                else:
                    lc[i].setChecked(True)
                a,b=divmod(index,5)
                self.c_cheetname_ck.append(lc[i])
                self.sheetbox_lo.addWidget(lc[i],a,b)
            wb.close()
        gc.collect()

    def initserverinfo(self,host,port,user,passwd,db):
        self.workThread.init1(host,port,user,passwd,db)

    def setp(self,num):
        print(num)
        if num<100:
            self.pbar.setValue(num)
        elif num==1000:
            self.qtb1.setEnabled(True)
            self.pbar.setValue(0)
            self.workThread.quit()
            QMessageBox.information(self, "错误", "文件保存失败,检查文件是否被打开",QMessageBox.Yes)
        elif num==2000:
            self.qtb1.setEnabled(True)
            self.pbar.setValue(0)
            #self.workThread.quit()
            QMessageBox.information(self, "错误", "链接数据库失败",QMessageBox.Yes)
        elif num==2001:
            self.qtb1.setEnabled(True)
            self.pbar.setValue(0)
            #self.workThread.quit()
            QMessageBox.information(self, "错误", "链接数据库失败",QMessageBox.Yes)

        elif num >=100 and num <101 :
            self.qtb1.setEnabled(True)
            self.pbar.setValue(num)
            QMessageBox.information(self, "提示", "报表导出成功1",QMessageBox.Yes)

    def work(self):
        self.t1=time.mktime(time.strptime(self.dt1.date().toString(Qt.ISODate),"%Y-%m-%d"))
        self.t2=time.mktime(time.strptime(self.dt2.date().toString(Qt.ISODate),"%Y-%m-%d"))+60*60*24
        self.c_cheetname=[]
        for i in self.c_cheetname_ck:
            if i.isChecked():
                self.c_cheetname.append(i.statusTip())

        if time.mktime(time.strptime(self.dt1.date().toString(Qt.ISODate),"%Y-%m-%d"))>time.mktime(time.strptime(self.dt2.date().toString(Qt.ISODate),"%Y-%m-%d")):
            QMessageBox.information(self, "信息", "起始时间不能大于结束时间",QMessageBox.Yes)
        else:
            gzh=self.gzh.text()
            sjl=self.sjl.text()
            cj=self.jsComboBox.currentText()
            self.fileName1=self.qtfile.text()
            mode=int(self.js2ComboBox.currentText().split('--')[0])
            if not path.exists(self.fileName1):
                QMessageBox.information(self, "提示", "检查配置，找不到模板文件",QMessageBox.No)
            elif len(self.c_cheetname)==0:QMessageBox.information(self, "提示", "没有选中任何工作表",QMessageBox.No)
            else:
                self.qtb1.setEnabled(False)
                self.workThread.init2(self.fileName1,self.t1,self.t2,gzh,sjl,cj,mode,self.c_cheetname,self.save_mode.isChecked())
                #print(c_cheetname)
                self.workThread.start()              #计时开始  
                #self.workThread.trigger.connect(over)   #当获得循环完毕的信号时，停止计数 
    
    def button_click(self): 
        # absolute_path is a QString object  
        self.fileName1, self.filetype = QFileDialog.getOpenFileName(self,
                                            "选取文件",  
                                            "",  
                                            "xlsx (*.xlsx)")   #设置文件扩展名过滤,注意用双分号间隔  
        if self.fileName1=='':pass
        else :
            self.qtfile.clear()
            self.qtfile.insert(self.fileName1)
        self.creatsheetCheckBox()