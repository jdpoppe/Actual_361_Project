import unittest

import os

from docutils.parsers import null

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course
from school_app.Helpers import assignInstructor

class TestAssignInstructor(unittest.TestCase):
    def setUp(self):
        self.instructor1 = Employee.objects.create(EMP_EMAIL="jimgaffigan@uwm.edu", EMP_FNAME="Jim",
                                                  EMP_LNAME="Gaffigan", EMP_ROLE="Instructor", EMP_INITIAL="T",
                                                  EMP_PASSWORD="123")
        self.instructor2 = Employee.objects.create(EMP_EMAIL="billburr@uwm.edu", EMP_FNAME="Bill",
                                                  EMP_LNAME="Burr", EMP_ROLE="Instructor", EMP_INITIAL="B",
                                                  EMP_PASSWORD="789")
        self.fakeinstructor = Employee.objects.create(EMP_EMAIL="", EMP_FNAME="", EMP_LNAME="", EMP_ROLE="Instructor",
                                                      EMP_INITIAL="", EMP_PASSWORD="")
        self.ta = Employee.objects.create(EMP_EMAIL="bertkreischer@uwm.edu", EMP_FNAME="Bert",
                                          EMP_LNAME="Kreischer", EMP_ROLE="TA", EMP_INITIAL="A",
                                          EMP_PASSWORD="456")
        self.course = Course.objects.create(title="Comedy 251", instructor=self.instructor1)
        self.course = Course.objects.create(title="Comedy 351", instructor=self.fakeinstructor)

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
