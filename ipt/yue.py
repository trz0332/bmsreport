from PyQt5.QtCore import QDateTime,QDate,QTime  ,QThread,pyqtSignal,QFileInfo,Qt
from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QGridLayout,QGroupBox,QLabel,QLineEdit
    ,QPushButton,QComboBox,QDateTimeEdit,QProgressBar,QMessageBox,QFileDialog,QMainWindow,QCheckBox,  QApplication)



class yue(QWidget):
    def __init__(self,config,parent=None):
        super(yue, self).__init__(parent)
        layout = QVBoxLayout()
        topLabel = QLabel("还没做这个功能")
        layout.addWidget(topLabel)
        self.setLayout(layout)
