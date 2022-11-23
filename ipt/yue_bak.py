from PyQt5.QtCore import QDateTime,QDate,QTime  ,QThread,pyqtSignal,QFileInfo,Qt
from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QGridLayout,QLabel,QLineEdit
    ,QPushButton,QComboBox,QDateTimeEdit,QProgressBar,QMessageBox,QFileDialog,QMainWindow,  QApplication)
import time
from os import path
from ipt.wt_yue import WorkThread

class yue(QWidget):
    def __init__(self,config, parent=None):
        super(yue, self).__init__(parent)
        layout = QGridLayout()  #创建一个表格排列
        self.fileName1=''
        ###############第一行 文件选择框
        layout.addWidget(QLabel('报表文件',self),0,0 )
        self.qtfile=QLineEdit('',self)
        self.qtfile.insert(config['sheet_day']['filename'] if 'filename' in  config['sheet_day'].keys() else '')
        self.qbfile=QPushButton('选择文件',self)
        self.qbfile.clicked.connect(self.button_click)
        self.qbfile.setEnabled(True)
        layout.addWidget(self.qtfile,0,1,1,6)
        layout.addWidget(self.qbfile,0,7)
        ######################第二行################################################
        layout.addWidget(QLabel('规则行',self) ,1,0)
        self.gzh=QLineEdit('',self)
        self.gzh.insert(config['sheet_day']['gzh'])
        self.gzh.setFixedWidth(40)
        layout.addWidget(QLabel('时间列',self) ,1,2)
        self.sjl=QLineEdit('',self)
        self.sjl.insert(config['sheet_day']['sjl'])
        self.sjl.setFixedWidth(40)
        layout.addWidget(QLabel('BMS厂家',self) ,1,4)
        jslist=['共济','中联','栅格']
        self.jsComboBox=QComboBox(self)   #下拉菜单
        for i in jslist:
            self.jsComboBox.addItem(i)
        self.jsComboBox.setCurrentIndex(int(config['sheet_day']['cj']))
        layout.addWidget(QLabel('模式',self),1,6)
        jslist2=['0--寻找日期','1--最后填充']
        self.js2ComboBox=QComboBox(self)   #下拉菜单
        for i in jslist2:
            self.js2ComboBox.addItem(i)
        self.js2ComboBox.setCurrentIndex(int(config['sheet_day']['mode']))
        layout.addWidget(self.gzh,1,1)
        layout.addWidget(self.sjl,1,3)
        layout.addWidget(self.jsComboBox,1,5)
        layout.addWidget(self.js2ComboBox,1,7)
        ######################第三行时间选择行#############################
        layout.addWidget(QLabel('起始时间',self),2,0) 
        nowyear=time.strftime('%Y',time.localtime(time.time()))
        nowyue=time.strftime('%m',time.localtime(time.time()))
        yearlist=[]
        for i in range(5):
            yearlist.append(str(int(nowyear)-i))
        self.st_nianComboBox=QComboBox(self)   #下拉菜单
        for i in yearlist:
            self.st_nianComboBox.addItem(i+'年')
        yuelist=range(1,13)
        self.st_yueComboBox=QComboBox(self)   #下拉菜单
        for i in yuelist:
            self.st_yueComboBox.addItem(str(i)+'月')
        #self.yueComboBox.setCurrentIndex(int(config['sheet_day']['mode']))
        self.st_nianComboBox.setCurrentIndex(yearlist.index(nowyear))
        self.st_yueComboBox.setCurrentIndex(yuelist.index(int(nowyue)))
        #self.js2ComboBox.setCurrentIndex(int(config['sheet_day']['mode']))
        # #############结束时间选择
        #  
        layout.addWidget(QLabel('结束时间',self),2,4) 
        self.en_nianComboBox=QComboBox(self)   #下拉菜单
        for i in yearlist:
            self.en_nianComboBox.addItem(i+'年')
        self.en_yueComboBox=QComboBox(self)   #下拉菜单
        for i in yuelist:
            self.en_yueComboBox.addItem(str(i)+'月')
        #self.yueComboBox.setCurrentIndex(int(config['sheet_day']['mode']))
        self.en_nianComboBox.setCurrentIndex(yearlist.index(nowyear))
        self.en_yueComboBox.setCurrentIndex(yuelist.index(int(nowyue)))
        ###########查询按钮###########
        self.qtb1=QPushButton('查询',self)
        self.qtb1.clicked.connect(self.work)
        
        layout.addWidget(self.st_nianComboBox,2,1)
        layout.addWidget(self.st_yueComboBox,2,2)
        layout.addWidget(self.en_nianComboBox,2,5)
        layout.addWidget(self.en_yueComboBox,2,6)





        layout.addWidget(self.qtb1,2,7)

        #######第四行进度条
        layout.addWidget(QLabel('进度',self),3,0 )
        self.pbar = QProgressBar(self)
        #self.pbar.setFixedWidth(560)
        layout.addWidget(self.pbar,3,1,1,6 )
        self.setLayout(layout)
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
    def pdsj(self,st_y,st_m,en_y,en_m):
        if st_y>en_y:return False
        else:
            if st_m>en_m:return False
            else:return True
    def work(self):
        stnian=int(self.st_nianComboBox.currentText()[:-1])
        styue=int(self.st_yueComboBox.currentText()[:-1])
        ennian=int(self.en_nianComboBox.currentText()[:-1])
        enyue=int(self.en_yueComboBox.currentText()[:-1])
        if not self.pdsj(stnian,styue,ennian,enyue):
            QMessageBox.information(self, "信息", "起始时间不能大于结束时间",QMessageBox.Yes)
        else:
            if not path.exists(self.fileName1):QMessageBox.information(self, "提示", "检查配置，找不到模板文件",QMessageBox.No)
            else:
                self.t1=time.mktime(time.strptime('{}-{}'.format(stnian,styue),"%Y-%m"))
                self.t2=time.mktime(time.strptime('{}-{}'.format(ennian,enyue),"%Y-%m"))