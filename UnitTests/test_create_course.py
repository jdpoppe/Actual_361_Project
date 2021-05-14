from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course
from school_app.Helpers import createCourse, createEmp


# Create your tests here.

class TestCreateCourse(TestCase):
    def setUp(self):
        self.employeeList = {"jimgaffigan@uwm.edu":["Jim","Gaffigan","Instructor","T","123"],
                             "bertkreischer@uwm.edu":["Bert","Kreischer","Supervisor","A","456"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.course = Course(title="Comedy 251", instructor=self.empObj[0])
        self.course.save()
    def test_noTitle(self):
        self.assertEqual("Course must have title", createCourse("", "jimgaffigan@uwm.edu"),
                         msg="Entering a course without a title fails to return message \"Course must have title\"")

    def test_courseExists(self):
        self.assertEqual("Course already exists", createCourse("Comedy 251", "jimgaffigan@uwm.edu"),
                         msg="Entering a course that already exists fails to return message "
                             "\"Course already exists\"")

    def test_instructorDNE(self):
        self.assertEqual("Instructor does not exist, or employee is not an Instructor",
                         createCourse("Comedy 361", "tomsegurra@uwm.edu"),
                         msg="Entering an instructor that does not exist fails to return message"
                             "\"Instructor does not exist, or employee is not an Instructor\"")

    def test_employeeNotInstructor(self):
        self.assertEqual("Instructor does not exist, or employee is not an Instructor",
                         createCourse("Comedy 361", "bertkreischer@uwm.edu"),
                         msg = "Entering an employee who is not an instructor does not return message, "
                               "\"Instructor does not exist, or employee is not an Instructor\"")

    def test_validInput(self):
        self.assertEqual("Course Successfully Created", createCourse("Comedy 680","jimgaffigan@uwm.edu"),
                         msg="Entering an untaken course title and instructor fails to return message "
                             "\"Course successfully created\"")


