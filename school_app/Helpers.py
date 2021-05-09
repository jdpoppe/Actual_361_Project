# from docutils.parsers import null
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


def createSection(title, ta, course):
    if title == "":
        return "Section needs to have title"
    taObj = ""
    if ta != "":
        taObj = list(Employee.objects.filter(EMP_EMAIL=ta, EMP_ROLE="TA"))
        if len(taObj) < 1:
            return "TA does not exist, or employee is not TA"
    if course == "":
        return "Section needs to have a course"
    courseObj = list(Course.objects.filter(title=course))
    if len(courseObj) < 1:
        return "Course does not exist"
    if (len(Section.objects.filter(title=title))) > 0:
        return "Section already exists"
    Section.objects.create(title=title, ta=taObj[0], course=courseObj[0])
    return "Section successfully added"


def assignInstructor(instructor, course):
    if instructor == "":
        return "There must be an instructor"
    instructorObj = list(Employee.objects.filter(EMP_EMAIL=instructor, EMP_ROLE="Instructor"))
    if (len(instructorObj) < 1):
        return "Instructor does not exist, or employee is not an instructor"
    courseObj = list(Course.objects.filter(title=course))
    if (len(courseObj) < 1):
        return "Course does not exist"
    courseObj[0].instructor = instructorObj[0]
    return "Instructor successfully assigned to course"


returnMessageAssignTA = {0:"TA does not exist, or employee is not a TA",
                         1:"Course does not exist, or Instructor does not teach course",
                         2:"Section does not exist"}

def assignTA(TA, course, section, instructor):
    if TA == "":
        return "There must be a TA"
    x = 0
    try:
        taObj = Employee.objects.get(EMP_EMAIL=TA, EMP_ROLE="TA")
        x = x+1
        instructorObj = Employee.objects.get(EMP_EMAIL=instructor, EMP_ROLE="Instructor")
        courseObj = Course.objects.get(title=course, instructor=instructorObj)
        x = x+1
        sectionObj = Section.objects.get(title=section, course=courseObj)
    except:
        return returnMessageAssignTA[x]

    sectionObj.emp = taObj
    sectionObj.save()
    return "TA successfully assigned to section"

def assignTAToSection(user, instructor, title, courser):
    pass

