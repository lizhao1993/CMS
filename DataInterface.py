__author__ = 'Jake'

# Imports functions to parse and modify XML database.

import xml.etree.ElementTree as ET
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import SubElement, ElementTree


class DataInterface:
    """ This class contains all basic database management functions
    for Student CMS. When working with this class, it is
    important to maintain the integrity of the student data
    categories and the headerList instance variable to prevent
    errors in which one attempts to modify the attributes of a
    category which does not exist. """

    # the static list of all default headers for students and groups
    deflist = ["Name", "Email", "Units", "Number_of_Absences",
               "Number_of_Excused", "In_Class", "Flag", "Students", "Grade", "Students", "Units"]

#############################################################################
#          Database Initialization, Creation, Saving and Upkeep             #
#############################################################################
    def __init__(self, fileloc="", year="", semester=""):
        """ Creates the database. If a file location (fileloc), the
        function open up a previously saved database.
        If no file location is passed, the function will use newDB to
        create a new database. """

        # stores list of non-default fields for students and groups respectively
        self.headerList = []
        self.groHeaderList = []
        # creates the list of non-default data categories.
        if fileloc:
            tree = ET.parse(fileloc)
            # reads from the database file into an ElementTree object
            self.data = tree.getroot()
            # sets the root of this object to the global variable data.
            self.findHeaders()  # loads all non-default data categories.
        else:
            self.data = self.newDB(year, semester)
            # sets the global variable data to the root returned by
            # newDB.


    def save(self, filename="database.xml"):
        """ Writes the database to the current folder. If a file name is
        passed, it will be saved under that name.
        If no name is passed, it will be saved under the default name
        "database.xml". """

        # wraps the global variable data (an Element) in an ElementTree
        # instance.
        file = ElementTree(self.data)
        file.write(filename)


    def newDB(self, year="", semester=""):
        """ Returns the root of a new ElementTree named "Gradebook" with
        the four subelements "Students", "Assignments", "Groups",
        and "Dates" for the four categories of data that could be
        stored in the database. Also stores the year
        and semester attributes for the Gradebook if those are passed.
        """

        root = ET.Element("Gradebook")
        # creates the Gradebook element and adds its attributes.
        root.attrib["year"] = year
        root.attrib["semester"] = semester

        # adds the four SubElements of the Gradebook.
        SubElement(root, "Students")
        SubElement(root, "Assignments")
        SubElement(root, "Groups")
        SubElement(root, "Dates")

        return root  # returns the root to be saved as self.data.


    def findHeaders(self):
        """ findHeaders:  Deduces the list of non-default category
        headers by finding a non-flagged, non-dropped student
        and adding all of their non-default categories to the header
        list. NOT FOR EXTERNAL USE. """

        # creates the list of default student categories and the empty header
        # lists.
        headerlist = []
        headerlistgro = []

        # finds the first non-flagged, non-dropped student and sets
        # the list of their children to catlist.
        stulist = self.data.find("Students").getchildren()
        x = 0
        while (stulist[x].find("Flag").attrib["info"] == "Yes"
               or stulist[x].find("In_Class").attrib["info"] == "No"):
            x += 1
        catlist = stulist[x].getchildren()

        # adds all categories whose tags are not a member of stdlist
        # to headerlist.
        for x in range(0, len(headerlist)):
            if (catlist[x].tag not in self.deflist):
                headerlist.append(catlist[x].tag)

        # sets local headerlist equal to the instanced headerList.
        self.headerList = headerlist

#############################################################################
#                           Finding Functions                               #
#############################################################################

    def findStudent(self, name):
        """ Returns the student Element with the attribute of the given
        name. NOT FOR EXTERNAL USE. """

        path = ".//Name[@info='" + name + "']"
        return self.data.find(path)

    def findAssignDate(self, sname, adname):
        """ Returns the Assignment or Date Element with the attribute of the given
        name. NOT FOR EXTERNAL USE. """

        student = self.findStudent(sname)
        path = ".//AssignDate[@name='" + adname + "']"
        return student.find(path)

    def findGroup(self, name):
        """ Returns the Group Element with the attribute of the given
        name. NOT FOR EXTERNAL USE. """
        path = ".//Group[@info='" + name + "']"
        return self.data.find(path)

    def findGroupStu(self, sname):
        """ Returns the Group Element with the given student as a member.
        NOT FOR EXTERNAL USE. """
        groups = self.data.find("Groups").getchildren()

        for x in range(0, len(groups)):
            if (sname in groups[x].find("Students").attrib["info"]):
                return groups[x]

        return ET.Element("None")

    def findDates(self):
        """ Returns the list of Date names. NOT FOR EXTERNAL USE. """

        dates = self.data.findall(".//Date")
        dateNames = []

        for x in range(0, len(dates)):
            dateNames.append(dates[x].attrib["info"])
        return dateNames

    def findHW(self):
        """ Returns the list of Assignment names. NOT FOR EXTERNAL USE. """

        assignments = self.data.findall(".//Homework")
        hwNames = []

        for x in range(0, len(assignments)):
            hwNames.append(assignments[x].attrib["info"])
        return hwNames

    def findAllGroups(self):
        """ Returns the list of Group names. NOT FOR EXTERNAL USE. """

        groups = self.data.findall(".//Group")
        groupNames=[]

        for i in range(0,len(groups)):
            groupNames.append(groups[i].attrib["info"])
        return groupNames


#############################################################################
#                        Student Roster Functions                           #
#############################################################################

    def addStudent(self, name):
        """ Creates a new student, with defaults of enrolled and
        unflagged. Student has all current column categories but without any
        values. If the student was already in the database returns an integer
        error message. """
        # checks that the student was not dropped
        if(self.findStudent(name)):
            students = self.data.find("Students")
            # finds the Students data category.
            student = SubElement(students, "Name")
            # adds a new subelement with the student's name as a tag.
            student.attrib["info"] = name
            # adds all default student data categories.
            SubElement(student, "Email").attrib["info"] = ""
            SubElement(student, "Units").attrib["info"] = ""
            SubElement(student, "Number_of_Absences").attrib["info"] = "0"
            SubElement(student, "Number_of_Excused").attrib["info"] = "0"
            SubElement(student, "In_Class").attrib["info"] = "Yes"
            SubElement(student, "Flag").attrib["info"] = "No"
            SubElement(student, "Grade").attrib["info"] = "Pass"

            # adds all additional data categories.
            for x in range(0, len(self.headerList)):
                cat = SubElement(student, "AssignDate").attrib["info"] = ""
                cat.attrib["name"] = self.headerList[x]

            return 1; # added a new student
        else:
            # if the student was previously dropped, they are un-dropped
            student = self.findStudent(name)
            if(student.find("In_Class") == "Yes"): return 2 # attempted to re-add a currently enrolled student
            else: return 3 # attempted to re-add a currently dropped student

    def dropStudent(self, name):
        """ Sets the InClass attribute to indicate that the student
        has dropped. """

        student = self.findStudent(name)
        student.find("In_Class").attrib["info"] = "No"

    def stuAbsence(self, name):
        """ Tallies the number of absences and excused absences the student has
        by iterating through all of their categories which are a part of the date list
        and adding an absence if the stored string is not 'Y' """

        # retrieves all of the given student's AssignDate categories and a list of date names
        student = self.findStudent(name)
        dateList = self.findDates()
        slist = student.findall("AssignDate")

        # initializes the absence and excused tallies
        absence = 0
        excused = 0

        # iterates through the AssignDate list and checks categories whose name is in the date List
        for x in range(0, len(slist)):
            if(slist[x].attrib["name"] in dateList):
                # increases excused if 'E' is found
                if(slist[x].attrib["info"] == "E"):
                    excused += 1
                # increases absence if 'Y' is not found
                else:
                    if(slist[x].attrib["info"] != "Y"):
                        absence += 1

        #sets the number of excused and absences categories
        student.find("Number_of_Excused").attrib["info"] = str(excused)
        student.find("Number_of_Absences").attrib["info"] = str(absence)

    def stuGrade(self, name):
        """ Determines whether the student has passed or failed by checking their
        number of absences and the total of their group and individual grades. At
        this time, the minimum necessary values are hard-coded. """

        grade = "Pass"
        student = self.findStudent(name)
        print (int(student.find("Number_of_Absences").attrib["info"]))

        #if(int(student.find("Number_of_Absences").attrib["info"]) >= 3):
        #    grade = "Fail"

        #assignlist = student.findall("AssignDate")
        #assigns = self.findHW()
        #totalpoints = 0
        #for x in range(0, len(assignlist)):
        #    if (assignlist[x].attrib["name"] in assigns):
        #        totalpoints += int(assignlist[x].attrib["info"])
        #if (totalpoints < 150): grade = "Fail"


        weeklylist = self.findGroupStu(name).findall("WeekGrade")
        weekpoints = 0
        dlist = ["Students", "Units"]
        for x in range(0, len(weeklylist)):
            if (weeklylist[x].attrib["name"] not in dlist):
                weekpoints += int(weeklylist[x].attrib["info"])
        if (weekpoints < 15): grade = "Fail"

        student.find("Grade").attrib["info"] = grade

    def stuSort(self, vlist):
        """ Takes a list of student elements, removes all dropped or
        flagged students and sorts alphabetically.
        NOT FOR EXTERNAL USE. """

        # initializes the sorting helper lists, name list and the returned list
        nlist = []
        v2list = []

        # iterates through the student element list, removing flagged or dropped student
        for x in range(0, len(vlist)):
            if (vlist[x].find("Flag").attrib["info"] == "No"
                or vlist[x].find("In_Class").attrib["info"] == "Yes"):
                # if a student is not flagged or dropped, their name is added to the name list
                nlist.append(vlist[x].attrib["name"])
        # alphabetically sorts the name list
        nlist.sort()

        # creates a list of student elements in the order of the sorted name list
        for x in range(0, len(nlist)):
            v2list.append(self.findStudent(nlist[x]))

        # returns the sorted element list
        return v2list

    def stuRec(self, name):
        """ Reconciles a student's categories with the database
        headerList. Only for use in edge cases. """

        # gets a list of the student's subelements
        student = self.findStudent(name)
        catlist = student.getchildren()

        # if the resulting list is the appropriate size, quit the function
        if (len(catlist) == (len(self.headerList) + 9)): return True

        # gets a list of unique AssignDates the student has
        localheaders = []
        for x in range(0, len(catlist)):
            if (catlist[x].attrib["name"]):
                localheaders.append(catlist[x].attrib["name"])

        # adds sub elements from the header list the student does not have
        for x in range(0, len(self.headerList)):
            if (self.headerList[x] not in localheaders):
                cat = SubElement(student, "AssignDate")
                cat.attrib["name"] =  self.headerList[x]
                cat.attrib["info"] = ""

        return True


#############################################################################
#                       Student Data Management                             #
#############################################################################


    def stuMod(self, name, header, value="", assign = False):
        """ Changes the attribute of the given header category within
        the given student element. Set assign to true if modifying a
        non-default category. """

        if(assign): self.findAssignDate(name,header).attrib["info"] = value
        else: self.findStudent(name).find(header).attrib["info"] = value

    def stuCall(self, name, header, assign = False):
        """ Gets the attribute of the given header category within
        the given student element. Set assign to true if calling a
        non-default category. """

        if(assign): return self.findAssignDate(name,header).attrib["info"]
        student = self.findStudent(name)
        path = ".//" + header
        return student.find(path).attrib["info"]



    def stuAdd(self, header, value=""):
        """ Adds a category with the tag given by the header to all
        students and adds this category to the list of
        categories which will be given to students added in the future.
        If a default is given in the value input
        this will be given to all students. This function will add
        duplicate categories, which will cause errors.
        Thus, this function should be used in conjunction with stuQuery
        which checks for duplicates. """

        self.headerList.append(header)
        students = self.data.find("Students")
        clist = students.getchildren()

        for x in range(0, len(clist)):
            student = SubElement(clist[x], "AssignDate")
            student.attrib["info"] = value
            student.attrib["name"] = header


    def stuQuery(self, header):
        """ Returns true if the students have a category with the given
        header as a tag and false if they do not. Use
        this to avoid adding duplicate categories. """

        return header in self.headerList

    def addAssignment(self, hwName):
        """ Adds an assignment to the list of already added assignments. Use
         with stuAdd when adding an assignment. """

        assignments = self.data.find("Assignments")
        assignment = SubElement(assignments, "Homework")
        assignment.attrib["info"] = hwName

    def addDate(self, today):
        """ Adds an date to the list of already added date. Use
         with stuAdd when adding an date. """

        dates = self.data.find("Dates")
        ddate = SubElement(dates, "Date")
        ddate.attrib["info"] = today


    def stuMassMod(self, header, vlist):
        """ Changes all values of the given DEFAULT header to the corresponding
        values of a list of values. This list must
        include all non-flagged, non-dropped students and must be
        arranged in alphabetical order by student
        name. If the list given is the wrong size or the header is not
        a category, the function will return
        false. Otherwise, true will be returned. """

        slist = self.data.find("Students").getchildren()
        slist = self.stuSort(slist)

        # checks to make sure that given modify list has the same length as the
        # sorted student list.
        if ((len(slist) != len(vlist)) or (header in self.headerList)):
            return False

        for x in range(0, len(slist)):
            slist[x].find(header).attrib["info"] = vlist[x]

        return True

    def stuMassAssignDateMod(self, header, vlist):
        """ Has the same function as stuMassMod except it is specifically
        for modifying AssignDate subElements. Failing to use this function when
        modifying subElements of this type will result in crashes. """

        slist = self.data.find("Students").getchildren()
        slist = self.stuSort(slist)

        if ((len(slist) != len(vlist)) or (header in self.headerList)):
            return False

        for x in range(0, len(slist)):
            path = ".//AssignDate[@name ='" + header + "']"
            slist[x].find(path).attrib["info"] = vlist[x]

        return True

    def stuMassCall(self, header):
        """ Returns a list of the values each student has of a given
        category with the DEFAULT header as a tag. This
        list is in alphabetical order and only includes non-dropped,
        non-flagged students. If the given
        header is not the tag of a category, then the function will
        return an empty string. """

        if(header == "Name"): path = ".//Name"
        else: path = ".//Name/" + header
        students = self.data.findall(path)

        vlist = []
        headers = self.deflist

        # checks to make sure the header is default
        if (header not in headers):
            return vlist

        # gets each non-dropped student's value at the desired element
        for x in range(0, len(students)):
            if(students[x].find("In_Class").attrib["info"] == "Yes"): vlist.append(students[x].attrib["info"])

        return vlist

    def stuMassAssignDateCall(self, header):
        """ Has the same function as stuMassCall except it is specifically
        for calling AssignDate subElements. Failing to use this function when
        calling subElements of this type will result in crashes. """

        path = ".//AssignDate[@name='" + header + "']"
        students = self.data.findall(path)

        vlist = []
        headers = self.deflist + self.headerList

        if (header not in headers):
            return vlist

        for x in range(0, len(students)):
            if(students[x].find("In_Class").attrib["info"] == "Yes"): vlist.append(students[x].attrib["info"])

        return vlist

    def stuCatMod(self, target, name):
        """ Allows the tag of a preexisting student category to be
        changed without effecting the category's
        stored data. """

        # if the header does not exist, returns false
        if (target not in self.headerList): return False

        self.headerList.remove(target)
        stulist = self.data.find("Students").getchildren()

        # iterates through the list of students, changing the target element's
        # name if it is found and adding it if it is not
        for x in range(0, len(stulist)):
            path = ".//AssignDate[@name='" + target + "']"
            if (stulist[x].find(path)):
                stulist[x].find(path).attrib["name"] = name
            else:
                cat = SubElement(stulist[x], "AssignDate")
                cat.attrib["name"] = name
                cat.attrib["info"] = ""

        return True

#############################################################################
#                       Group Roster Functions                              #
#############################################################################

    def addGroup(self, name):
        """ Adds a group with the give name and initializes default categories. """

        groups = self.data.find("Groups")

        # adds the group element with the given name as its 'info' attribute
        group = SubElement(groups, "Group")
        group.attrib["info"] = name

        # sets default categories
        SubElement(group, "Units").attrib["info"] = "0"
        SubElement(group, "Students").attrib["info"] = []

    def groStuAdd(self, gname, sname):
        """ Adds a student with the name sname to the group with gname.
        will fail if a group with the given name does not exist or if
        a student with the given name does not exist. Also adds the
        given student's units to the group's unit total. """

        # finds the group and adds the sname to the group's student list
        group = self.findGroup(gname)
        group.find("Students").attrib["info"].append(sname)

        # find's the group and the student's current units, adds them,
        # and sets the group's units to this number
        groupUnits=int(group.find("Units").attrib["info"])
        studentUnits=int(self.findStudent(sname).find("Units").attrib["info"])
        groupUnits+=studentUnits
        group.find("Units").attrib["info"]=str(groupUnits)

    def groStudRemove(self, gname, sname):
        """ Remove's the given student and their units from the group's
        student list and unit count respectively. If the student is not
        in the group, this function will improperly remove units from the
        group. Once again, if the group or student does not exist, this
        function will fail. """

        # finds group and student list
        group = self.findGroup(gname)
        slist = group.find("Students").attrib["info"]
        newlist = []

        # iterates through the student list, adding students which do not
        # have name sname to the new list
        for x in range(0, len(slist)):
            if sname != slist[x]: newlist.append(slist[x])

        # sets the group's student list equal to the new list
        group.find("Students").attrib["info"] = newlist

        # modifies the group's unit count as above except uses subtraction.
        groupUnits=int(group.find("Units").attrib["info"])
        studentUnits=int(self.findStudent(sname).find("Units").attrib["info"])
        groupUnits-=studentUnits
        group.find("Units").attrib["info"]=str(groupUnits)



#############################################################################
#                        Group Data Management                              #
#############################################################################

    def groMod(self, name, header, value):
        """ Changes the attribute of the given header category within
        the given group element. Cannot modify Units or Students as
        those categories are handled in groStuAdd and groStuRemove."""

        group = self.findGroup(name)
        path = ".//WeekGrade[@name='" + header + "']"
        group.find(path).attrib["info"] = value

    def groCall(self, name, header):
        """ Retrieves the attribute of the given header category within
        the given group element. Cannot modify Units or Students as
        those categories are handled in groStuAdd and groStuRemove."""

        group = self.findGroup(name)
        path = ".//WeekGrade[@name='" + header + "']"
        return group.find(path).attrib["info"]

    def groAdd(self, group, header, value=""):
        """ Adds a WeekGrade subElement with the name given by header and with the
        info attribute set to value. This subelement currently cannot be removed
        or modified. """

        group = self.findGroup(group)
        cat = SubElement(group, "WeekGrade")
        cat.attrib["info"] = value
        cat.attrib["name"] = header

    def groCommentMod(self, name, header, comment):
        """ Modifies the comment stored in the WeekGrade subelement with the name
        attribute given by header. The comment must be a string. """
        group = self.findGroup(name)
        path = ".//WeekGrade[@name='" + header + "']"
        group.find(path).text = comment

    def groCommentCall(self, name, header):
        """ Retrieves the comment stored in the WeekGrade subelement with the name
        attribute given by header. The comment returned will be a string. """

        group = self.findGroup(name)
        path = ".//WeekGrade[@name='" + header + "']"
        return group.find(path).text

    def groMassDateCall(self, gname):
        """ Retrieves the names of all stored WeekGrade subelements and returns them as an
        unsorted list of strings. """

        group = self.findGroup(gname)
        datesElements = group.findall(".//WeekGrade")
        
        dates=[]
        for date in datesElements:
            dates.append(date.attrib["name"])
        return dates

        





















