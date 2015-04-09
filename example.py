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

def populateTableView(model,students):
    """ populateTableView takes in a nested list of students with their info,
    a model (standardItemModel), and adds data to the TableView; it then
    returns the model.
    This method also adds students to the database so it should only be
    called when the database is empty """
    
    row=0;

    # Add students to tableView
    for student in students:
        prename = student[0]+" "+student[1]
        db.addStudent(prename)
        
        name = QStandardItem(prename)
        email = QStandardItem(student[2])
        units = QStandardItem(str(student[3]))
        
        model.setItem(row,0,name)
        model.setItem(row,1,email)
        model.setItem(row,2,units)
        row+=1

    return model

def populateTableWidget(students):
    """ populateTableWidget takes in a nested list of students with their info,
    the table we want to populate, and adds data to the TableWidget """
    
    table = ui.tableWidget
    table.setColumnCount(2)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem("hi"))
    table.setRowCount(len(students))
    row=0;

    # Add students to tableView and tableWidget
    for student in students:
        prename = student[0]+" "+student[1]
        name1 = QTableWidgetItem(prename)
        table.setItem(row,0,name1)
        row+=1

    return table

def pushButton_Clicked(self):
    
    fname = QFileDialog.getOpenFileName()
    filename = (fname[0])
    students = loadworkbook.getStudentsFromWorkbook(filename)

    # Add students to the table Widget
    table = populateTableWidget(students)

    # TableView needs a model
    model = QStandardItemModel(len(students),3)
    model.setHorizontalHeaderItem(0, QStandardItem("Name"))
    model.setHorizontalHeaderItem(1, QStandardItem("Email"))
    model.setHorizontalHeaderItem(2, QStandardItem("Units"))
    
    # Add students to tableView
    model = populateTableView(model,students)
    

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

