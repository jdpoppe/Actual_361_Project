from docutils.parsers import null
from .models import Course, Employee, Section

def createCourse(title, email):
    if title == "":
        return "Course has no title"
    if len(Course.objects.filter(title=title)):
        return "Course with same title already exists"
    instructor = null
    if email != "":
        entries = list(Employee.objects.filter(EmailField=email,type=1))

        if len(entries) == 0:
            return "Instructor does not exist or employee is not instructor"
        else:
            instructor = entries[0]

    course = Course.objects.create(title=title, instructor=instructor)
    return "Course Successfully Created"

def createSection(title, ta, course):
    if title == "":
        return "Section needs to have title"
    taObj = null
    if ta!="":
        taObj = list(Employee.objects.filter(EmailField=ta))
        if len(taObj)<1:
            return "TA does not exist"
    if course == "":
        return "Section needs to have a course"
    courseObj = list(Course.objects.filter(title=course))
    if len(courseObj)<1:
        return "Course does not exist"
    if(len(Section.objects.filter(title=title, course=courseObj[0])))>0:
        return "Section already exists"
    Section.objects.create(title=title, ta=taObj[0], course=courseObj[0])
    return "Section successfully added"

def assignInstructor(instructor, course):
    instructorObj = list(Employee.objects.filter(EmailField=instructor, type=1))
    if(len(instructorObj)<1):
        return "Instructor does not exist or employee is not an instructor"
    courseObj = list(Course.objects.filter(title=course))
    if(len(instructorObj<1)):
        return "Course does not exist"
    prev = courseObj[0].instructor
    courseObj[0].instructor = instructorObj[0]
    if prev==null:
        return "Previous Instructor replaced with new Instructor"
    return "Instructor successfully assigned"

def assignTA(TA, course, section):
    taObj = list(Employee.objects.filter(EmailField=TA, type=1))
    courseObj = list(Course.objects.filter(title=course))
    if len(taObj)<1:
        return "TA does not exist, or employee is not a TA"
    if len(courseObj)<1:
        return "Course does not exist"
    sectionObj = list(Section.objects.filter(title=section, course=courseObj[0]))
    if len(sectionObj)<1:
        return "Section does not exist"
    prev = sectionObj[0].ta
    sectionObj[0].ta = taObj
    if prev==null:
        return "Previous TA replaced with new TA"
    return "TA successfully assigned"
