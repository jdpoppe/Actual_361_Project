import unittest

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import makeInstructor


class TestMakeInstructor(unittest.TestCase):
    def setUp(self):
        if len(Employee.objects.filter(EMP_EMAIL="fleetwood@uwm.edu"))<1:
            self.instructor = Employee.objects.create(EMP_EMAIL="fleetwood@uwm.edu", EMP_FNAME="Fleetwood",
                                                      EMP_LNAME="Mac", EMP_ROLE="Instructor", EMP_INITIAL="J",
                                                      EMP_PASSWORD="123")
            self.ghost = Employee.objects.create(EMP_EMAIL="", EMP_FNAME="",
                                                      EMP_LNAME="", EMP_ROLE="Instructor", EMP_INITIAL="",
                                                      EMP_PASSWORD="")
            self.course1 = Course.objects.create(title="Class 7", instructor=self.instructor)
            self.course2 = Course.objects.create(title="Class 8")
            self.course3 = Course.objects.create(title="Class 9", instructor=self.ghost)

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
