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
import datetime
from datetime import date

def populateTableView(model,students):
    """ populateTableView takes in a nested list of students with their info,
    a model (standardItemModel), and adds data to the TableView; it then
    returns the model.
    This method also adds students to the database so it should only be
    called when the database is empty """
    
    row=0;

    # Add students to tableView
    for student in students:
        name = student[0]+" "+student[1]
        email = student[2]
        units = str(student[3])
        db.addStudent(name)
        db.stuMod(name,"Email",email)
        db.stuMod(name,"Units",units)
        model.setItem(row,0,QStandardItem(name))
        model.setItem(row,1,QStandardItem(email))
        model.setItem(row,2,QStandardItem(units))
        row+=1
        
    db.save()
    return model

def populateAttendance(students):
    """ populateattendanceTable takes in a nested list of students with their info
    and adds data to the (default) attendanceTable; it is called when a new
    roster is uploaded """
    
    table = ui.attendanceTable
    table.setColumnCount(2)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    today = date.today()
    todaysDate = today.strftime("%m/%d/%y")
    db.addDate(todaysDate) 
    table.setHorizontalHeaderItem(1,QTableWidgetItem(todaysDate))
    table.setRowCount(len(students))
    row=0;

    # Add students to attendanceTable
    for student in students:
        preset = QTableWidgetItem("Y")
        name1 = QTableWidgetItem(student[0]+" "+student[1])
        table.setItem(row,0,name1)
        table.setItem(row,1,preset)
        row+=1
        
    db.save()
    return table

def populateGrades(students):
    """ populateGrades takes in a nested list of students and adds their names
    to the first column in the grades table; it is called when a new roster
    is uploaded """
    
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
    """ getRoster is called when the button to import a roster is clicked; it
    reads the imported excel file into a nested list of students and then
    populates the roster, attendanceTable, and the gradesTable """
    
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
        db.addAssignment(text)
        db.save()
        
def populateRosterFromDB(model,names):
    emails = db.stuMassCall("Email")
    units = db.stuMassCall("Units")

    for row in range(0,len(names)):
        model.setItem(row,0,QStandardItem(names[row]))
        model.setItem(row,1,QStandardItem(emails[row]))
        model.setItem(row,2,QStandardItem(units[row]))
    

def populateAttendanceFromDB(names):
    table = ui.attendanceTable
    today = datetime.date.today()
    todaysDate = today.strftime("%m/%d/%y")
    print(todaysDate)
    db.addDate(todaysDate)
    dates = db.data.findall("Date")
    
    table.setColumnCount(len(dates)+1)
    table.setRowCount(len(names))
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem(todaysDate))
    preset = QTableWidgetItem("Y")
    row=0
    cols = table.columnCount()-1

    # Add students to attendanceTable
    for student in names:
        name = names[row]
        col=cols
        table.setItem(row,0,QTableWidgetItem(name))
        for date in dates:
            date = date.attrib["info"]
            table.setHorizontalHeaderItem(col,QTableWidgetItem(date))
            table.setItem(row,col,preset)
            col-=1
        row+=1
    db.save()
    return table


def populateGradesFromDB(names):
    """ populateGrades takes in a nested list of students and adds their names
    to the first column in the grades table """
    
    table = ui.gradesTable
    assignments = db.data.findall("Homework")
    table.setColumnCount(len(assignments)+1)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setRowCount(len(names))
    row=0

    for student in names:
        name = names[row] #there are row students/names
        table.setItem(row,0,QTableWidgetItem(name))
        col=1
        for hw in assignments:
            hwName = hw.attrib["info"]
            table.setHorizontalHeaderItem(col,QTableWidgetItem(hwName))
            grade = db.stuCall(name,hwName)
            table.setItem(row,col,QTableWidgetItem(grade))
            col+=1
        row+=1
    return table
            
            
        
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    filename = "database.xml"

    if filename:
        db = DataInterface.DataInterface(filename)
        names = db.stuMassCall("Name")
        model = QStandardItemModel(len(names),3)
        model.setHorizontalHeaderItem(0, QStandardItem("Name"))
        model.setHorizontalHeaderItem(1, QStandardItem("Email"))
        model.setHorizontalHeaderItem(2, QStandardItem("Units"))
        
        populateRosterFromDB(model,names)
        ui.rosterView.setModel(model)
        
        attendanceTable = populateAttendanceFromDB(names)
        gradesTable = populateGradesFromDB(names)
    else:
        db = DataInterface.DataInterface()

    ui.pushButton.clicked.connect(getRoster)
    ui.add_assignment.clicked.connect(showDialog)
    ui.attendanceTable.cellChanged.connect(cellChangedAttendance)
    ui.gradesTable.cellChanged.connect(cellChangedGrades)

    window.show()
    sys.exit(app.exec_())

