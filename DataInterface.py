__author__ = 'Jake'

#Imports functions to parse and modify XML database.

import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import SubElement, ElementTree

# This class contains all basic database management functions for Student CMS. When working with this class, it is
#   important to maintain the integrity of the student data categories and the headerList instance variable to prevent
#   errors in which one attempts to modify the attributes of a category which does not exist.
class DataInterface:
    # __init__: Creates the database. If a file location (fileloc), the function open up a previously saved database.
    #          If no file location is passed, the function will use newDB to create a new database.
    def __init__(self, fileloc=None, year=None, semester=None):
        self.headerList = []        # creates the list of non-default data categories.
        if fileloc:
            tree = ET.parse(fileloc)  # reads from the database file into an ElementTree object
            self.data = tree.getroot()  # sets the root of this object to the global variable data.
            self.findHeaders() # loads all non-default data categories.
        else:
            self.data = self.newDB(year, semester)  # sets the global variable data to the root returned by newDB.

    # save:  Writes the database to the current folder. If a file name is passed, it will be saved under that name.
    #       If no name is passed, it will be saved under the default name "database.xml".
    def save(self, filename="database.xml"):
        file = ElementTree(self.data)  # wraps the global varable data (an Element) in an ElementTree instance.
        file.write(filename)

    # newDB: Returns the root of a new ElementTree named "Gradebook" with the three subelements "Students", "Groups",
    #        and "Dates" for the three categories of data that could be stored in the database. Also stores the year
    #        and semester attributes for the Gradebook if those are passed.
    def newDB(self, year=None, semester=None):
        root = ET.Element("Gradebook")  # creates the Gradebook element and adds its attributes.
        root.attrib["year"] = year
        root.attrib["semester"] = semester

        SubElement(root, "Students")  # adds the three SubElements of the Gradebook.
        SubElement(root, "Groups")
        SubElement(root, "Dates")

        return root  # returns the root to be saved as self.data.

    # findHeaders:  Deduces the list of non-default category headers by finding a non-flagged, non-dropped student
    #               and adding all of their non-default categories to the header list. NOT FOR EXTERNAL USE.
    def findHeaders(self):
        # creates the list of default categories and the empty header list.
        deflist = ["ID", "Units", "Number of Absences", "Number of Excused", "In Class", "Flag"]
        headerlist = []

        # finds the first non-flagged, non-dropped student and sets the list of their children to catlist.
        stulist = self.data.find("Students").getchildren()
        x = 0
        while(stulist[x].find("Flag").attrib["info"] == True or stulist[x].find("In Class").attrib["info"] == False):
            x += 1
        catlist = stulist[x].getchildren()

        # adds all categories whose tags are not a member of stdlist to headerlist.
        for x in range(0, len(headerlist)):
            if(catlist[x].tag not in deflist): headerlist.append(catlist[x].tag)

        # sets local headerlist equal to the instanced headerList.
        self.headerList = headerlist

    # addStudent:   Creates a new student and notes that this student has not dropped the class and isn't flagged.
    #               Student has all current column categories but without any values.
    def addStudent(self, name):
        students = self.data.find("Students")  # finds the Students data category.
        student = SubElement(students, name)  # adds a new subelement with the student's name as a tag.

        # adds all default student data categories.
        SubElement(student, "ID")
        SubElement(student, "Units")
        SubElement(student, "Number of Absences")
        SubElement(student, "Number of Excused")
        SubElement(student, "In Class").attrib["info"] = True
        SubElement(student, "Flag").attrib["info"] = False

        # adds all additional data categories.
        for x in range(0, len(self.headerList)):
            SubElement(student, self.headerList[x])

    # findStudent:  Finds the student Element with the tag of the given name. NOT FOR EXTERNAL USE.
    def findStudent(self, name):
        students = self.data.find("Students")
        return students.find(name)

    # stuSort:  Takes a list of student elements, removes all dropped or flagged students and sorts alphabetically.
    #           NOT FOR EXTERNAL USE.
    def stuSort(self, vlist):
        nlist = []
        v2list = []

        for x in range(0, len(vlist)):
            if(vlist[x].find("Flag").attrib["info"] == False or vlist[x].find("In Class").attrib["info"] == True):
                   nlist.append(vlist[x].tag)
        nlist.sort()

        for x in range(0, len(nlist)):
            v2list.append(self.findStudent(nlist))

        return v2list

    # dropStudent:   Sets the InClass attribute to indicate that the student has dropped.
    def dropStudent(self, name):
        student = self.findStudent(name)
        student.find("In Class").attrib["info"] = 0

    # stuMod, stuCall: Change or modify respectively the attribute of the given header category within the given
    #                  student element.
    def stuMod(self, name, header, value):
        student = self.findStudent(name)
        student.find(header).attrib["info"] = value

    def stuCall(self, name, header):
        student = self.findStudent(name)
        return student.find(header).attrib["info"]

    # stuAdd:   Adds a category with the tag given by the header to all students and adds this category to the list of
    #           categories which will be given to students added in the future. If a default is given in the value input
    #           this will be given to all students. This function will add duplicate categories, which will cause errors.
    #           Thus, this function should be used in conjunction with stuQuery which checks for duplicates.
    def stuAdd(self, header, value=None):
        self.headerList.append(header)
        students = self.data.find("Students")
        clist = students.getchildren()

        for x in range(0, len(clist)):
            if (value != None):
                SubElement(clist[x], header).attrib["info"] = value
            else:
                SubElement(clist[x], header)

    # stuQuery: Returns true if the students have a category with the given header as a tag and false if they do not. Use
    #           this to avoid adding duplicate categories.
    def stuQuery(self, header):
        return header in self.headerList

    # stuMassMod:  Changes all values of the given header to the corresponding values of a list of values. This list must
    #              include all non-flagged, non-dropped students and must be arranged in alphabetical order by student
    #              name. If the list given is the wrong size or the header is not a category, the function will return
    #              false. Otherwise, true will be returned.
    def stuMassMod(self, header, vlist):
        slist = self.data.find("Students").getchildren()
        slist = self.stuSort(slist)

        if((len(slist) != len(vlist)) or (header in self.headerList)): return False

        for x in range(0, len(slist)):
            slist[x].find(header).attrib["info"] = vlist[x]

        return True

    # stuMassCall:  Returns a list of the values each student has of a given category with the header as a tag. This
    #               list is in alphabetical order and only includes non-dropped, non-flagged students. If the given
    #               header is not the tag of a category, then the function will return None.
    def stuMassCall(self, header):
        slist = self.data.find("Students").getchildren()
        slist = self.stuSort(slist)
        vlist = []

        if(header not in self.headerList): return None

        for x in range(0, len(slist)):
            vlist.append(slist[x].find(header).attrib["info"])

        return vlist

    # stuRec:   Reconciles a student's categories with the database headerList. Should be used whenever a student
    #           is un-flagged or un-dropped.
    def stuRec(self, name):
        student = self.findStudent(name)
        catlist = student.getchildren()
        stdlist = ["ID", "Units", "Number of Absences", "Number of Excused", "In Class", "Flag"]

        if(len(catlist) == (len(self.headerList)+6)): return True

        localheaders = []
        for x in range(0, len(catlist)):
            if(catlist[x].tag not in stdlist): localheaders.append(catlist[x].tag)

        for x in range(0, len(self.headerList)):
            if(self.headerList[x] not in localheaders): SubElement(student, self.headerList[x])

    # stuCatMod:    Allows the tag of a preexisting student category to be changed without effecting the category's
    #               stored data.
    def stuCatMod(self, target, name):
        if(target not in self.headerList): return False
        self.headerList.remove(target)

        stulist = self.data.find("Students").getchildren()
        for x in range(0, len(stulist)):
            if(stulist[x].find(target)): stulist[x].find(target).tag = name
            else: SubElement(stulist[x], name)

        return True

















