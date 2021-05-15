
from .models import Course, Employee, Section


def createCourse(title, email):
    if title == "":
        return "Course must have title"
    if len(Course.objects.filter(title=title)) > 0:
        return "Course already exists"
    instructor = ""
    if email != "":
        entries = list(Employee.objects.filter(EMP_EMAIL=email, EMP_ROLE="Instructor"))

        if len(entries) == 0:
            return "Instructor does not exist, or employee is not an Instructor"
        else:
            instructor = entries[0]
    Course.objects.create(title=title, instructor=instructor)
    return "Course Successfully Created"

createSectionMessage = {0:"Section needs to have title",
                        1:"Section needs to have a course",
                        2:"Course does not exist",
                        3:"TA does not exist, or employee is not TA",
                        4:"Section already exists",
                        5:"Section successfully added"}
def createSection(title, ta, course):
    x = 0
    checkEmpty = [title,course]
    for i in checkEmpty:
        if i == "":
            return createSectionMessage[x]
        x = x+1
    try:
        courseObj = Course.objects.get(title=course)
        x = x+1
        taObj = Employee.objects.get(EMP_EMAIL=ta, EMP_ROLE="TA")
    except:
        if (x == 3 and ta != "")|(x == 2):
            return createSectionMessage[x]
        else:
            taObj = ""
    x = x+1
    if (len(Section.objects.filter(title=title, course=courseObj))) > 0:
        return createSectionMessage[x]
    x = x+1
    if taObj == "":
        Section.objects.create(title=title, course=courseObj)
    else:
        Section.objects.create(title=title, emp=taObj, course=courseObj)
    return createSectionMessage[x]

assignInstructorMessage = {0:"There must be an instructor",
                           1:"Instructor does not exist, or employee is not an instructor",
                           2:"Course does not exist",
                           3:"Instructor successfully assigned to course"}

def assignInstructor(instructor, course):
    x = 0
    if instructor == "":
        return assignInstructorMessage[x]
    x = x+1
    try:
        instructorObj = Employee.objects.get(EMP_EMAIL=instructor, EMP_ROLE="Instructor")
        x = x+1
        courseObj = Course.objects.get(title=course)
        x=x+1
    except:
        return assignInstructorMessage[x]
    courseObj.instructor = instructorObj
    courseObj.save()
    return assignInstructorMessage[x]


returnMessageAssignTA = {0: "TA does not exist, or employee is not a TA",
                         1: "Course does not exist, or Instructor does not teach course",
                         2: "Section does not exist"}


def assignTA(TA, course, section, instructor):
    if TA == "":
        return "There must be a TA"
    x = 0
    try:
        taObj = Employee.objects.get(EMP_EMAIL=TA, EMP_ROLE="TA")
        x = x + 1
        instructorObj = Employee.objects.get(EMP_EMAIL=instructor, EMP_ROLE="Instructor")
        courseObj = Course.objects.get(title=course, instructor=instructorObj)
        x = x + 1
        sectionObj = Section.objects.get(title=section, course=courseObj)
    except:
        return returnMessageAssignTA[x]

    sectionObj.emp = taObj
    sectionObj.save()
    return "TA successfully assigned to section"


returnMessageAssignEmployee = {0: "Course does not exist",
                               1: "Section does not exist",
                               2: "Employee does not exist",
                               3: "You cannot assign a supervisor to a section",
                               4: "Employee successfully assigned to section",
                               5: "Course has different Instructor assigned to it, "
                                  "cannot assign new instructor to section"}


def assignEmployeeToSection(employee, section, course):
    x = 0
    try:
        courseObj = Course.objects.get(title=course)
        x = x + 1
        sectionObj = Section.objects.get(title=section, course=courseObj)
        x = x + 1
        employeeObj = Employee.objects.get(EMP_EMAIL=employee)
        x = x + 1
    except:
        return returnMessageAssignEmployee[x]
    if employeeObj.EMP_ROLE == "Supervisor":
        return returnMessageAssignEmployee[x]
    if (employeeObj.EMP_ROLE == "Instructor") & (courseObj.instructor == None):
        courseObj.instructor = employeeObj
        courseObj.save()
    elif (courseObj.instructor != employeeObj) & (employeeObj.EMP_ROLE == "Instructor"):
        return returnMessageAssignEmployee[x + 2]
    sectionObj.emp = employeeObj
    sectionObj.save()
    return returnMessageAssignEmployee[x + 1]

def makeInstructor(title):
    try:
        currentCourse = Course.objects.get(title=title)
        instructor = currentCourse.instructor
        if currentCourse.instructor == None:
            return "Instructor Not Assigned Yet"
        return instructor.EMP_FNAME + " " + instructor.EMP_LNAME
    except:
        return "Course Does not Exist"


def courseList():
    c = Course.objects.all()
    courses = list()
    for i in c:
        courses.append(i.title)
    return courses





def sectionsForCourse(course):
    try:
        currentCourse = Course.objects.get(title=course)
    except:
        raise TypeError
    allSections = Section.objects.filter(course=currentCourse)
    sectionNames = list()
    for i in allSections:
        if i.emp == None:
            sectionNames.append((i.title, "No one", "assigned"))
        else:
            sectionNames.append((i.title, i.emp.EMP_FNAME, i.emp.EMP_LNAME))
    return sectionNames

def taForCourse(course):
    try:
        currentCourse = Course.objects.get(title=course)
    except:
        raise TypeError
    allSections = Section.objects.filter(course=currentCourse)
    sectionNames = list()
    for i in allSections:
        if i.emp != None:
            toAdd = (i.emp.EMP_FNAME, i.emp.EMP_LNAME)
            doesNotContain = True
            isNotTA = True
            if i.emp.EMP_ROLE != "TA":
                isNotTA = False
            for j in sectionNames:
                if j == toAdd:
                    doesNotContain=False
                    break
            if doesNotContain & isNotTA:
                sectionNames.append(toAdd)
    return sectionNames

def courseAndSection(courses):
    courseAndSection = []
    for i in courses:
        sections = sectionsForCourse(i)
        courseAndSection.append((i, sections))
    return courseAndSection

def createEmp(employeeList, empObj):
    for i in employeeList.keys():
        temp = Employee(EMP_EMAIL=i, EMP_FNAME=employeeList[i][0], EMP_LNAME=employeeList[i][1],
                        EMP_ROLE=employeeList[i][2], EMP_INITIAL=employeeList[i][3],
                        EMP_PASSWORD=employeeList[i][4])
        temp.save()
        empObj.append(temp)
    return empObj

def displayEmp():
    allEmployee = list(Employee.objects.all())
    formattedEntries = []
    for i in allEmployee:
        formattedEntries.append(
            (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))  # i.0, i.1, i.2, i.3, i.4
    return formattedEntries







