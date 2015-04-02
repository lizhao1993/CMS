#this is the current version 03/31/15


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from CMS1 import Ui_MainWindow
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
#from pyexcel as pe import json

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
#need to load old table

    
def pushButton_Clicked(self):
    print ("hello")
    fname = QFileDialog.getOpenFileName()
    #with xlrd.open_workbook(fname) as f: # import as excel
    sheet= pe.load(fname)
    #print json.dumps(sheet.to_array())
    ui.tableView.setText(data) 
    
        
ui.pushButton.clicked.connect(pushButton_Clicked)


window.show()
sys.exit(app.exec_())

