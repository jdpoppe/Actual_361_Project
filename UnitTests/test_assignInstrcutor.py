from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course
from school_app.Helpers import assignInstructor, createEmp

class TestAssignInstructor(TestCase):
    def setUp(self):
        self.employeeList = {"jimgaffigan@uwm.edu":["Jim","Gaffigan","Instructor","T","123"],
                             "billburr@uwm.edu":["Bill","Burr","Instructor","B","789"],
                             "bertkreischer@uwm.edu":["Bert","Kreischer","TA","A","456"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.course1 = Course(title="Comedy 251", instructor=self.empObj[0])
        self.course1.save()
        self.course2 = Course(title="Comedy 351")
        self.course2.save()

    def test_courseDNE(self):
        self.assertEqual("Course does not exist", assignInstructor("jimgaffigan@uwm.edu","Comedy 457"))

    def test_instructorDNE(self):
        self.assertEqual("Instructor does not exist, or employee is not an instructor",
                         assignInstructor("tomsegurra@uwm.edu", "Comedy 251"))

    def test_empNotInstructor(self):
        self.assertEqual("Instructor does not exist, or employee is not an instructor",
                         assignInstructor("bertkreischer@uwm.edu", "Comedy 251"))

    def test_allExistNoPrev(self):
        self.assertEqual("Instructor successfully assigned to course",
                         assignInstructor("jimgaffigan@uwm.edu", "Comedy 351"))

    def test_allExistPrev(self):
        self.assertEqual("Instructor successfully assigned to course",
                         assignInstructor("billburr@uwm.edu", "Comedy 251"),
                         msg="Entering valid inputs for a course that already had an instructor fails to return "
                             "message \"Instructor successfully assigned to course\"")
