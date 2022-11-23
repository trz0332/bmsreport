#import base64
from PyQt5.QtWidgets import (QTextEdit,QAction, qApp,QApplication,QMainWindow,QMessageBox,QDateTimeEdit,QComboBox
    ,QFileDialog,QPushButton,QProgressBar,QGridLayout,QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,QTreeWidget,QTreeWidgetItem,
        QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtCore import QCoreApplication,Qt ,QThread,pyqtSignal,QFileInfo
from PyQt5.QtGui import QPixmap,QIcon,QDesktopServices,QPalette,QBrush
from PyQt5.QtXml import (QDomDocument, QDomNode, QXmlDefaultHandler,
                         QXmlInputSource, QXmlSimpleReader)
import configparser
import decimal
from encoder import XML2Dict


from os import path
#####################################
from ctypes import windll
windll.shell32.SetCurrentProcessExplicitAppUserModelID("ceshi")
class TabDialog(QDialog):           ##########主界面
    def __init__(self, parent=None):
        super(TabDialog, self).__init__(parent)
        self.lc=local()
        self.xml = XML2Dict()
        self.all_layout = QGridLayout()
        self.Group_div_tree = QGroupBox("设备树")
        self.Group_div_index = QGroupBox("测点")
        self.all_layout.addWidget(self.Group_div_tree,0,0)
        self.all_layout.addWidget(self.Group_div_index,0,1)
        self.setLayout(self.all_layout)
        self.fileName1='StationConfig.xml'
        self.config=self.loadxmlconfig() 
        self.inittree() 
        self.jx()
    def loadxmlconfig(self):
        if not path.exists(self.fileName1):
            return False
        else:
            with open('StationConfig.xml', 'r', encoding='utf-8') as f:
                s = f.read()            # 把文件内容视作string
                the_dict = self.xml.parse(s) # the_dict是dict类型
                #print(the_dict['StationConfig']['CfgStation'])  
            print(list(the_dict['StationConfig'].keys()))
            return the_dict['StationConfig']
    def on_addAction_triggered(self,currNode,addChild1_key):  
        #currNode = self.tree.currentItem()  
        addChild1 =QTreeWidgetItem()  
        addChild1.setText(0,addChild1_key)  
        #addChild1.setText(1, 'addChild1_val')  
        currNode.addChild(addChild1) 
    def inittree(self):
        self.tree = QTreeWidget(self.Group_div_tree ) 
        #self.tree.addTopLevelItem(self.root)
        #self.tree.setColumnCount(1) 
        self.root= QTreeWidgetItem(self.tree)  
        self.root.setText(0,self.config['CfgStation']['Station'][0]['#Station']['StationName']) 

    def jx(self):
        #print(self.config['CfgStation'])


        if self.config: 
            for i in self.config['CfgStation']['Station'][1:]:
                lc[] =QTreeWidgetItem()  
                addChild1.setText(0,addChild1_key)  
                #addChild1.setText(1, 'addChild1_val')  
                currNode.addChild(addChild1) 
            for i in 



    





if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tabdialog = TabDialog()
    tabdialog.show()
    sys.exit(app.exec_())


