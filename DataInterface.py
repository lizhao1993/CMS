__author__ = 'Jake'

#Imports functions to parse and modify XML database.

import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import SubElement, ElementTree

#This class contains all basic database management functions for Student CMS
class DataInterface:

    #__init__: Creates the database. If a file location (fileloc), the function open up a previously saved database.
    #          If no file location is passed, the function will use newDB to create a new database.
    def __init__(self, fileloc = None, year = None, semester = None):
        if fileloc:
            tree = ET.parse(fileloc)            #reads from the database file into an ElementTree object
            self.data = tree.getroot()          #sets the root of this object to the global variable data.
        else:
            self.data = self.newDB(year, semester)   #sets the global variable data to the root returned by newDB.

    #save:  Writes the database to the current folder. If a file name is passed, it will be saved under that name.
    #       If no name is passed, it will be saved under the default name "database.xml".
    def save(self, filename = "database.xml"):
        file = ElementTree(self.data)   #wraps the global varable data (an Element) in an ElementTree instance.
        file.write(filename)

    #newDB: Returns the root of a new ElementTree named "Gradebook" with the three subelements "Students", "Groups",
    #       and "Dates" for the three categories of data that could be stored in the database. Also stores the year
    #       and semester attributes for the Gradebook if those are passed.
    def newDB(self, year = None, semester = None):
        root = ET.Element("Gradebook")          #creates the Gradebook element and adds its attributes.
        root.attrib["year"] = year
        root.attrib["semester"] = semester

        SubElement(root, "Students")            #adds the three SubElements of the Gradebook.
        SubElement(root, "Groups")
        SubElement(root, "Dates")

        return root                             #returns the root to be saved as self.data.

    #addStudent:    Creates a new student and notes that this student has not dropped the class
    def addStudent(self, name):
        students = self.data.find("Students")   #finds the Students data category.

        student = SubElement(students, name)    #adds a new subelement with the student's name as a tag.
        student.attrib["InClass"] = 1           #sets the student to have not dropped.

    #dropStudent:   Sets the InClass attribute to indicate that the student has dropped.
    def dropStudent(self, name):
        students = self.data.find("Students")   #finds the dropping student.
        student = students.find(name)

        student.set("InClass", 0)               #sets them InClass to show they have dropped.




