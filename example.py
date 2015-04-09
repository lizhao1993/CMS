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

def populateAttendance(students):
    """ populateattendanceTable takes in a nested list of students with their info
    and adds data to the (default) attendanceTable """
    
    table = ui.attendanceTable
    table.setColumnCount(2)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem("hi"))
    table.setRowCount(len(students))
    row=0;

    # Add students to attendanceTable
    for student in students:
        preset = QTableWidgetItem("Y")
        name1 = QTableWidgetItem(student[0]+" "+student[1])
        table.setItem(row,0,name1)
        table.setItem(row,1,preset)
        row+=1
    return table

def populateGrades(students):
    table = ui.gradesTable
    table.setColumnCount(1)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setRowCount(len(students))
    row=0;

    for student in students:
        name1 = QTableWidgetItem(student[0]+" "+student[1])
        table.setItem(row,0,name1)
        row+=1
    return table

def getRoster(self):
    
    fname = QFileDialog.getOpenFileName()
    filename = (fname[0])
    students = loadworkbook.getStudentsFromWorkbook(filename)

    # Add students to the table Widget
    table = populateAttendance(students)
    gradesTable = populateGrades(students)

    # TableView needs a model
    model = QStandardItemModel(len(students),3)
    model.setHorizontalHeaderItem(0, QStandardItem("Name"))
    model.setHorizontalHeaderItem(1, QStandardItem("Email"))
    model.setHorizontalHeaderItem(2, QStandardItem("Units"))
    
    # Add students to tableView
    model = populateTableView(model,students)
    

    # Display the attendanceTable and the tableView
    table.show()
    gradesTable.show()
    ui.rosterView.setModel(model)
    
    db.save()
    
def cellChangedAttendance(self):
    col = ui.attendanceTable.currentColumn()
    row = ui.attendanceTable.currentRow()
    
    #get student's name
    if col!=0:
        name = ui.attendanceTable.item(row,0)
        if name:
            name = name.text()
            db.stuAbsence(name)
            db.save()

def cellChangedGrades(self):
    col = ui.gradesTable.currentColumn()
    row = ui.gradesTable.currentRow()
    
    #get student's name
    if col!=0:
        name = ui.gradesTable.item(row,0)
        if name:
            name = name.text()
            header = ui.gradesTable.horizontalHeaderItem(col)
            if header:
                header = header.text()
                item = ui.gradesTable.currentItem()
                if item:
                    item = item.text()
                    db.stuMod(name,header,item)
                    db.save()

def showDialog(self):
    inputDialog = QInputDialog()
    text, ok = inputDialog.getText(ui.add_assignment,"Add Assignment",
                                   "Enter Assignment Name:")
    if ok:
        cols = ui.gradesTable.columnCount()
        ui.gradesTable.insertColumn(cols)        
        ui.gradesTable.setHorizontalHeaderItem(cols,QTableWidgetItem(text))

        # gets number of students if it's known
        if ui.attendanceTable.columnCount()>0:
            rows = ui.attendanceTable.rowCount()
            ui.gradesTable.setRowCount(rows)
            
        #add the homework name to the database for all students
        db.stuAdd(text)
        db.save()
            
            
        
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    db = DataInterface.DataInterface()

    ui.pushButton.clicked.connect(getRoster)
    ui.add_assignment.clicked.connect(showDialog)
    ui.attendanceTable.cellChanged.connect(cellChangedAttendance)
    ui.gradesTable.cellChanged.connect(cellChangedGrades)

    window.show()
    sys.exit(app.exec_())

