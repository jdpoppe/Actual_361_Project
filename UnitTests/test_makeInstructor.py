from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course
from school_app.Helpers import makeInstructor,createEmp


class TestMakeInstructor(TestCase):
    def setUp(self):
        self.employeeList = {"fleetwood@uwm.edu":["Fleetwood","Mac","Instructor","J","123"],
                             "":["","","Instructor","",""]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.course1 = Course(title="Class 7", instructor=self.empObj[0])
        self.course1.save()
        self.course2 = Course(title="Class 8")
        self.course2.save()
        self.course3 = Course(title="Class 9", instructor=self.empObj[1])
        self.course3.save()


    def test_invalidCourse(self):
        self.assertEqual(makeInstructor("a;slkdfjapsoifjas"), "Course Does not Exist",
                         msg="Entering a course that DNE fails to return proper message")

    def test_validCourseWTeach(self):
        self.assertEqual(makeInstructor("Class 7"), "Fleetwood Mac",
                         msg="Entering a valid course with a valid instructor fails to return proper name")

    def test_validCourseWOTeach(self):
        self.assertEqual(makeInstructor("Class 8"), "Instructor Not Assigned Yet", msg="Entering a course without "
                                                                                       "an instructor fails to "
                                                                                       "return correct message")

    def test_emptyStrings(self):
        self.assertEqual(makeInstructor("Class 9"), " ", msg="Entering a course with an instructor who has no "
                                                            "information fails to return and empty string")
