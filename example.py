# last edited 4/2/2015
# authors: Student CMS team - Neftali Dominguez, Li Zhao, Nicole Chang, Jacob Patton


import sys
import loadworkbook
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAction,
                             QTextEdit)
from CMS1 import Ui_MainWindow
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)


app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

def pushButton_Clicked(self):
    
    fname = QFileDialog.getOpenFileName()
    filename = (fname[0])
    students = loadworkbook.getStudentsFromWorkbook(filename)

    model = QStandardItemModel(len(students),3)
    model.setHorizontalHeaderItem(0, QStandardItem("Name"))
    model.setHorizontalHeaderItem(1, QStandardItem("Email"))
    model.setHorizontalHeaderItem(2, QStandardItem("Units"))
    row=0;
    for student in students:
        name = QStandardItem(student[0]+" "+student[1])
        email = QStandardItem(student[2])
        units = QStandardItem(str(student[3]))
        model.setItem(row,0,name)
        model.setItem(row,1,email)
        model.setItem(row,2,units)
        row+=1
    ui.tableView.setModel(model)
    ui.tableView.resizeColumnToContents(0)
    ui.tableView.resizeColumnToContents(1)
    ui.tableView.resizeColumnToContents(2)



ui.pushButton.clicked.connect(pushButton_Clicked)

window.show()
sys.exit(app.exec_())

