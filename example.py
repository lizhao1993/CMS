# last edited 4/2/2015
# authors: Student CMS team - Neftali Dominguez, Li Zhao, Nicole Chang, Jacob Patton


import sys
import loadworkbook
import DataInterface
import xml.etree.ElementTree as ET
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CMS1 import Ui_MainWindow


app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

db = DataInterface.DataInterface()

def pushButton_Clicked(self):
    
    fname = QFileDialog.getOpenFileName()
    filename = (fname[0])
    students = loadworkbook.getStudentsFromWorkbook(filename)

    # Set up the table
    table = ui.tableWidget
    table.setColumnCount(2)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem("hi"))
    table.setRowCount(len(students))

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
        
        name1 = QTableWidgetItem(prename)
        
        name = QStandardItem(prename)
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
    
    db.save()

def saveAttendanceChanges(self):
    table = ui.tableWidget
    rows = table.rowCount()
    cols = table.columnCount()

    for row in range(0,rows):
        for col in range(0,cols):
            if table.cellChanged(row,col):
                #get value with currentItem
                #use currentRow to get student's name
                #find student in DB
                #if absent, add absence to count in DB
                print("hi")
                pass
                
                
    

# Connects the button to the dialog
ui.pushButton.clicked.connect(pushButton_Clicked)
ui.pushButton_3.clicked.connect(saveAttendanceChanges)

window.show()
sys.exit(app.exec_())

