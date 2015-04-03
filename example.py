#this is the current version 03/31/15
import sys
import loadworkbook
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QAction,
                             QTextEdit)
from CMS1 import Ui_MainWindow


app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

def pushButton_Clicked(self):
    print("hello")
    fname = QFileDialog.getOpenFileName()
    filename = (fname[0])
    students = loadworkbook.getStudentsFromWorkbook(filename)
    print(students)

model = QStandardItemModel(2,3)
model.setHorizontalHeaderItem(0, QStandardItem("Name"))
model.setHorizontalHeaderItem(1, QStandardItem("Email"))
model.setHorizontalHeaderItem(2, QStandardItem("Units"))

firstRow = QStandardItem("ColumnValue")
model.setItem(0,0,firstRow)

ui.tableView.setModel(model)
ui.pushButton.clicked.connect(pushButton_Clicked)

window.show()
sys.exit(app.exec_())


