#from docutils.parsers import null
#import null

from .models import Course, Employee, Section

def createCourse(title, email):
    if title == "":
        return "Course must have title"
    if len(Course.objects.filter(title=title)):
        return "Course already exists"
    instructor = null
    if email != "":
        entries = list(Employee.objects.filter(EMP_EMAIL=email,EMP_ROLE="Instructor"))

        if len(entries) == 0:
            return "Instructor does not exist, or employee is not an Instructor"
        else:
            instructor = entries[0]
    if instructor==null:
        Course.objects.create(title=title)
    else:
        Course.objects.create(title=title, instructor=instructor)
    return "Course Successfully Created"


def createSection(title, ta, course):
    if title == "":
        return "Section needs to have title"
    taObj =null
    if ta!="":
        taObj = list(Employee.objects.filter(EMP_EMAIL=ta, EMP_ROLE="TA"))
        if len(taObj)<1:
            return "TA does not exist, or employee is not TA"
    if course == "":
        return "Section needs to have a course"
    courseObj = list(Course.objects.filter(title=course))
    if len(courseObj)<1:
        return "Course does not exist"
    if(len(Section.objects.filter(title=title, courseTitle=title)))>0:
        return "Section already exists"
    if(taObj==null):
        Section.objects.create(title=title, course=courseObj[0], courseTitle=title)
    else:
        Section.objects.create(title=title, ta=taObj[0], course=courseObj[0], courseTitle=title)
    return "Section successfully added"

def assignInstructor(instructor, course):
    if instructor=="":
        return "There must be an instructor"
    instructorObj = list(Employee.objects.filter(EMP_EMAIL=instructor, EMP_ROLE="Instructor"))
    if(len(instructorObj)<1):
        return "Instructor does not exist, or employee is not an instructor"
    courseObj = list(Course.objects.filter(title=course))
    if(len(courseObj)<1):
        return "Course does not exist"
    courseObj[0].instructor = instructorObj[0]
    return "Instructor successfully assigned to course"

def assignTA(TA, course, section):
    if TA=="":
        return "There must be a TA"
    taObj = list(Employee.objects.filter(EMP_EMAIL=TA, EMP_ROLE="TA"))
    courseObj = list(Course.objects.filter(title=course))
    if len(taObj)<1:
        return "TA does not exist, or employee is not a TA"
    if len(courseObj)<1:
        return "Course does not exist"
    sectionObj = list(Section.objects.filter(title=section, course=courseObj[0]))
    if len(sectionObj)<1:
        return "Section does not exist"
    sectionObj[0].ta = taObj[0]
    return "TA successfully assigned to section"
