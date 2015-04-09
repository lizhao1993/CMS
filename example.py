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


def addColsToGrades():
    table = ui.tableWidget_2
    table.setColumnCount(10)
    table.setRowCount(50)

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
    """ populateTableWidget takes in a nested list of students with their info
    and adds data to the (default) TableWidget """
    
    table = ui.tableWidget
    table.setColumnCount(2)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem("hi"))
    table.setRowCount(len(students))
    row=0;

    # Add students to tableView and tableWidget
    for student in students:
        preset = QTableWidgetItem("Y")
        name1 = QTableWidgetItem(student[0]+" "+student[1])
        table.setItem(row,0,name1)
        table.setItem(row,1,preset)
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
    
def cellChanged(self):
    col = ui.tableWidget.currentColumn()
    row = ui.tableWidget.currentRow()
    
    #get student's name
    
    name = ui.tableWidget.item(row,0)
    if name:
        name = name.text()
        print(name)
        db.stuAbsence(name)
        db.save()

def showDialog(self):

    #self.le = QLineEdit(self)
    text, ok = QInputDialog.getText(self, "Add Assignment","Enter Assignment Name:")

    if ok:
        #self.le.setText(str(text))
        cols = ui.tableWidget_2.columnCount()
        ui.tableWidget_2.insertColumn(cols)        
        table.setHorizontalHeaderItem(cols,QTableWidgetItem(text))
        
        

# Connects the button to the dialog
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    db = DataInterface.DataInterface()

    addColsToGrades()
    ui.pushButton.clicked.connect(pushButton_Clicked)
    ui.add_assignment.clicked.connect(showDialog)
    ui.tableWidget.cellChanged.connect(cellChanged)

    window.show()
    sys.exit(app.exec_())

