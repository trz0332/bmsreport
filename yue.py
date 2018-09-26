from PyQt5.QtCore import QDateTime,QDate,QTime  ,QThread,pyqtSignal,QFileInfo,Qt
from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QGridLayout,QLabel,QLineEdit
    ,QPushButton,QComboBox,QDateTimeEdit,QDateEdit,QProgressBar,QMessageBox)

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
        #self.qbfile.clicked.connect(self.button_click)
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
        self.dt1 = QDateEdit(QDate.currentDate(),self) # 创建日期，并初始值  
        self.dt1.setDisplayFormat('yyyy-MM-dd')
        #self.dt1.setMinimumDate(QDate.currentDate().addDays(-90)) # 限定时间最小值，当前时间-365天  
        self.dt1.setMaximumDate(QDate.currentDate().addDays(1)) # 限定时间最大值，当前时间+365天  
        self.dt1.setCalendarPopup(True) # 允许弹出窗口选择日期，setMinimumDate()的限定对这个窗口也有效  
        # #############结束时间选择 
        layout.addWidget(QLabel('结束时间',self),2,4)
        self.dt2 = QDateEdit(QDate.currentDate(),self) # 创建日期，并初始值  
        self.dt2.setDate(QDate.currentDate())  
        #self.dt2.setMinimumDate(QDate.currentDate().addDays(-90)) # 限定时间最小值，当前时间-365天  
        self.dt2.setMaximumDate(QDate.currentDate().addDays(1)) # 限定时间最大值，当前时间+365天  
        self.dt2.setCalendarPopup(True) # 允许弹出窗口选择日期，setMinimumDate()的限定对这个窗口也有效  

        ###########查询按钮###########
        self.qtb1=QPushButton('查询',self)
        #self.qtb1.clicked.connect(self.work)
        
        layout.addWidget(self.dt1,2,1,1,3)
        layout.addWidget(self.dt2,2,5,1,2)
        layout.addWidget(self.qtb1,2,7)

        #######第四行进度条
        layout.addWidget(QLabel('进度',self),3,0 )
        self.pbar = QProgressBar(self)
        #self.pbar.setFixedWidth(560)
        layout.addWidget(self.pbar,3,1,1,6 )
        self.setLayout(layout)