# last edited 4/2/2015
# authors: Student CMS team - Neftali Dominguez, Li Zhao, Nicole Chang, Jacob Patton


import sys
import loadworkbook
import DataInterface
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CMS1 import Ui_MainWindow


app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

def pushButton_Clicked(self):
    
    fname = QFileDialog.getOpenFileName()
    filename = (fname[0])
    students = loadworkbook.getStudentsFromWorkbook(filename)
    db = DataInterface.DataInterface()

    # Set up the table
    table = ui.tableWidget
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem("hi"))
    table.setRowCount(len(students))
    table.setColumnCount(2)

    # TableView needs a model
    model = QStandardItemModel(len(students),3)
    model.setHorizontalHeaderItem(0, QStandardItem("Name"))
    model.setHorizontalHeaderItem(1, QStandardItem("Email"))
    model.setHorizontalHeaderItem(2, QStandardItem("Units"))
    row=0;

    # Add students to tableView and tableWidget
    for student in students:
        prename = student[0]+" "+student[1]
        db.addStudent(prename)
        name = QStandardItem(prename)
        name1 = QTableWidgetItem(prename)
        email = QStandardItem(student[2])
        units = QStandardItem(str(student[3]))
        
        table.setItem(row,0,name1)
        model.setItem(row,0,name)
        model.setItem(row,1,email)
        model.setItem(row,2,units)
        row+=1

    # Display the tableWidget and the tableView
    table.show()
    ui.tableView.setModel(model)
    #db.save()

# Connects the button to the dialog
ui.pushButton.clicked.connect(pushButton_Clicked)

window.show()
sys.exit(app.exec_())

