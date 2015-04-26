#TODOs: getRoster(), addNewProject()
#TODO: Get feedback working
#TODO: Export functionality
#TODO: New semester/year functionality




import sys
import os.path
import loadworkbook
import DataInterface
import xml.etree.ElementTree as ET
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from CMS1 import Ui_MainWindow
import datetime
from datetime import date

from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter


def populateTableView(model,students):
    """ This is a function for populating the roster;
    populateTableView takes in a nested list of students with their info,
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
    table.setHorizontalHeaderItem(1,QTableWidgetItem("Total Unexcused"))
    table.setRowCount(len(students))
    row=0;
    for student in students:
        name = student[0]+" "+student[1]
        db.addStudent(name)
        absences = db.stuCall(name,"Number_of_Absences")
        table.setItem(row,0,QTableWidgetItem(name))
        table.setItem(row,1,QTableWidgetItem(absences))
        row+=1        
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
    #TODO: Check if the db already has stuff in it and if so, do a
    #      comparison
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
            date = ui.attendanceTable.horizontalHeaderItem(col)
            print(name)
            if date:
                date = date.text()
                item = ui.attendanceTable.currentItem()
                #item = ui.attendanceTable.item(row,col)
                print(date)
               
                if item:
                    item = item.text()
                    print(item)
                    db.stuAbsence(name)
                    db.stuMod(name,date,item)
                    
                    
                    db.save()
            #print (date)
            
            #inp = ui.attendanceTable.item(row,col)
            #inptext= inp.text()
            
            
            #db.stuMod(name,date,inptext)
            
            #db.save()

def cellChangedGrades(self):
    col = ui.gradesTable.currentColumn()
    row = ui.gradesTable.currentRow()    
    #get student's name
    if col!=0:
        name = ui.gradesTable.item(row,0)
        if name:
            name = name.text()
            print(name)
            header = ui.gradesTable.horizontalHeaderItem(col)
            if header:
                header = header.text()
                print(header)
                item = ui.gradesTable.currentItem()
                if item:
                    item = item.text()
                    print(item)
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
        #add the homework name to the database for all students
        db.stuAdd(text)
        db.addAssignment(text)
        db.save()

def populateProjTable(model,names):
    model.setHorizontalHeaderItem(0,QStandardItem("Name"))
    model.setHorizontalHeaderItem(1,QStandardItem("Units"))
    row=0
    for name in names:
        units=db.stuCall(name, "Units")
        model.setItem(row,0,QStandardItem(name))
        model.setItem(row,1,QStandardItem(units))
        row+=1
    return model

def projComboBoxFill(dialog):
    combo = QComboBox(dialog)
    names=db.stuMassCall("Name")
    for name in names:
        combo.addItem(name)
    return combo
        
def onChanged(self):
    value = ui.numStudents.value() 
    form=ui.form 
    numAlready=form.rowCount()
    total=value+4
    print(total-numAlready)
    if total>numAlready: #we need boxes
        for i in range(0,total-numAlready):
            combo=projComboBoxFill(ui.dialog)
            form.addRow(combo)
    if total<numAlready:
        for i in range(0,abs(total-numAlready)):
            form.takeAt(6)
    if total==numAlready:
        combo=projComboBoxFill(ui.dialog)
        form.addRow(combo)
    

def addNewProject(self):
    #TODO: Create model for the student info: name & number of units
    #TODO: Create model for the feedback: date & comment
    #TODO: Add project to the database
    #TODO: Add students to project group
    ui.dialog = QDialog()
    ui.form = QFormLayout(ui.dialog)
    form = ui.form
    #Get the info from the dialog window
    form.addRow(QLabel("Enter project name and students."))
    fields = []
    le = QLineEdit(ui.dialog) #will contain the user input for project names
    form.addRow("Project Name",le)
    fields.append(le)
    #user inputs for the students
    ui.numStudents = QSpinBox(ui.dialog)
    ui.numStudents.setRange(1,10)
    form.addRow("Number of Students",ui.numStudents)
    ui.numStudents.valueChanged.connect(onChanged)
    #Add the OK and Cancel buttons
    buttonBox = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
        Qt.Horizontal, ui.dialog)
    form.addRow(buttonBox)
    buttonBox.accepted.connect(ui.dialog.accept)
    buttonBox.rejected.connect(ui.dialog.reject)

    # Li Zhao 04/23
    
    #groAdd(le, value=le)
    #groStuAdd(le, name1)
    #groStuAdd(le, name1)
    #groStuAdd(le, name1)
    
    result = ui.dialog.exec_()
    
    # Li Zhao 04/23
    #feedback = projectFeedback.getText()
    #groCommentMod(projName, projName, feedback)
        
def accepted(self):        
    projName = fields[0].text()
    numPages = ui.toolBox.count()
    combo = ui.chooseProject
    #set up the page to display project data
    page = QWidget()
    page.setGeometry(QRect(0,0,100,30))
    page.setObjectName(projName)
    students = QTableView(page)
    students.setGeometry(QRect(0, 0, 260, 140))
    students.setObjectName("stuInProject_"+str(numPages))
    projectFeedback = QTableView(page)
    projectFeedback.setGeometry(QRect(0, 150, 260, 150))
    projectFeedback.setObjectName("projFeedback_"+str(numPages))
    #add page to UI & to comboBox
    ui.toolBox.addItem(page,projName)
    combo.addItem(projName)
##    #create model for student & units:
##    model=QStandardItemModel(len(stuNames),2)
##    model=populateProjTable(model,stuNames)
##    students.show()
##    students.setModel(model)
##    #create model for project feedback & dates
##    feedmodel=QStandardItemModel(len(stuNames),2)
##    feedmodel.setHorizontalHeaderItem(0,QStandardItem("Date"))
##    feedmodel.setHorizontalHeaderItem(1,QStandardItem("Feedback"))
##    projectFeedback.show()
##    projectFeedback.setModel(feedmodel)
        
def addTodaysDate(self):
    #TODO: check if today's date is already in DB!
    inputDialog = QInputDialog()
    today, ok = inputDialog.getText(ui.add_assignment,"Add Date",
                                   "Enter Date:")
    if ok:
        colnum = ui.attendanceTable.columnCount()
        ui.attendanceTable.insertColumn(colnum)
        ui.attendanceTable.setHorizontalHeaderItem(colnum,QTableWidgetItem(today))
        db.stuAdd(today,"Y")
        db.addDate(today)
        #print(today)
        
        db.save()


        
        rows = ui.attendanceTable.rowCount()
        for i in range(0,rows):
            ui.attendanceTable.setItem(i,colnum,QTableWidgetItem("Y"))

        
        
def populateRosterFromDB(model,names):
    emails = db.stuMassCall("Email")
    units = db.stuMassCall("Units")
    for row in range(0,len(names)):
        model.setItem(row,0,QStandardItem(names[row]))
        model.setItem(row,1,QStandardItem(emails[row]))
        model.setItem(row,2,QStandardItem(units[row]))
    

def populateAttendanceFromDB(names):
    dates = db.findDates()    
    table = ui.attendanceTable
    table.setColumnCount(len(dates)+2)
    table.setRowCount(len(names))
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setHorizontalHeaderItem(1,QTableWidgetItem("Total Unexcused"))
    col = table.columnCount()-1
    rows=len(names)
    
    for date in dates:
        table.setHorizontalHeaderItem(col,QTableWidgetItem(date))
        for i in range(0,rows):
            table.setItem(i,0,QTableWidgetItem(names[i]))
            absences = db.stuCall(names[i],"Number_of_Absences")
            table.setItem(i,1,QTableWidgetItem(absences))
            table.setItem(i,col,QTableWidgetItem("Y"))
        col=col-1
                
    return table


def populateGradesFromDB(names):
    """ populateGrades takes in a nested list of students and adds their names
    to the first column in the grades table """    
    table = ui.gradesTable
    assignments = db.findHW()
    table.setColumnCount(len(assignments)+1)
    table.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
    table.setRowCount(len(names))
    row=0
    for student in names:
        name = names[row]
        table.setItem(row,0,QTableWidgetItem(name))
        col=1
        for hw in assignments:
            table.setHorizontalHeaderItem(col,QTableWidgetItem(hw))
            grade = db.stuCall(name,hw)
            table.setItem(row,col,QTableWidgetItem(grade))
            col+=1
        row+=1
    return table

def export():
    """ export saves the student name and final grades into a excel file"""
    names = db.stuMassCall("Name")
    #call the grade function for each student 
    for name in names:
        db.stuGrade(name)
    #get the list of grade from database
    finalgrades = db.stuMassCall("Grade")
     
    #make an excel workbook

    wb = Workbook()
    dest_filename = 'Export.xlsx'

    #make a worksheet
    ws1 = wb.active
    ws1.title = "Grade"

    #put in the names and grades
    #First value is header
    ws1.cell(row=1, column=1).value = "Name"
    r = 2
    for name in names:
        ws1.cell(row=r, column=1).value = name
        r += 1

    ws1.cell(row=1, column=2).value = "Grade"
    j = 2
    for grade in finalgrades:
        ws1.cell(row=j, column=2).value = grade
        j += 1

    #save the file
    wb.save(filename = dest_filename)
    
            
            
        
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    filename = "database.xml"
    
    if os.path.isfile(filename):
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
    ui.addProjectBttn.clicked.connect(addNewProject)
    ui.addDateButton.clicked.connect(addTodaysDate)
    ui.attendanceTable.cellChanged.connect(cellChangedAttendance)
    ui.gradesTable.cellChanged.connect(cellChangedGrades)    
    ui.export_2.clicked.connect(export)

    ui


    window.show()
    sys.exit(app.exec_())

