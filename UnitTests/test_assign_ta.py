import unittest

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import assignTA

class TestAssignTA(unittest.TestCase):
    def setUp(self):
        if len(list(Employee.objects.filter(EMP_EMAIL="jgaffigan@uwm.edu"))) < 1:
            self.instructor = Employee.objects.create(EMP_EMAIL="jgaffigan@uwm.edu", EMP_FNAME="Jim",
                                                      EMP_LNAME="Gaffigan", EMP_ROLE="Instructor", EMP_INITIAL="T",
                                                      EMP_PASSWORD="123")
            self.ta = Employee.objects.create(EMP_EMAIL="bkreischer@uwm.edu", EMP_FNAME="Bert",
                                              EMP_LNAME="Kreischer", EMP_ROLE="TA", EMP_INITIAL="A",
                                              EMP_PASSWORD="456")
            self.fakeTA = Employee.objects.create(EMP_EMAIL="", EMP_FNAME="",
                                                  EMP_LNAME="", EMP_ROLE="TA", EMP_INITIAL="",
                                                  EMP_PASSWORD="")
            self.course = Course.objects.create(title="Comedy 252", instructor=self.instructor)
            self.course2 = Course.objects.create(title="Comedy 351")
            self.section = Section.objects.create(title="Lab 101", course=self.course, emp=self.ta)
            self.section2 = Section.objects.create(title="Lab 102", course=self.course, emp=self.fakeTA)


    def test_courseDNE(self):
        self.assertEqual("Course does not exist, or Instructor does not teach course",
                         assignTA("bkreischer@uwm.edu","Comedy 458","Lab 101","jgaffigan@uwm.edu"),
                         msg="Entering a course that does not exist fails to return message, "
                             "\"Course does not exist\"")


    def test_sectionDNE(self):
        self.assertEqual("Section does not exist",
                         assignTA("bkreischer@uwm.edu","Comedy 252","Lab 103","jgaffigan@uwm.edu"),
                         msg="Entering a section that DNE fails to return message \"Section does not exist\"")


    def test_taDNE(self):
        self.assertEqual("TA does not exist, or employee is not a TA",
                         assignTA("tomsegurra@uwm.edu", "Comedy 252", "Lab 101", "jgaffigan@uwm.edu"),
                         msg="Entering a ta that DNE fails to return message "
                             "\"TA does not exist, or employee is not TA\"")

    def test_courseIsNotTaughtByInstructor(self):
        self.assertEqual("Course does not exist, or Instructor does not teach course",
                         assignTA("bkreischer@uwm.edu", "Comedy 351", "Lab 101", "jgaffigan@uwm.edu"),
                         msg = "Entering a course that the instructor does not teach fails to return message, "
                               "\"Course does not exist, or Instructor does not teach course\"")

    def test_allExistEmpNotTA(self):
        self.assertEqual("TA does not exist, or employee is not a TA",
                         assignTA("jgaffigan@uwm.edu", "Comedy 252", "Lab 801", "jgaffigan@uwm.edu"),
                         msg="Entering an employee that is not ta fails to return message"
                             "\"TA does not exist, or employee is not TA\"")


    def test_allExistNoPrev(self):
        self.assertEqual("TA successfully assigned to section",
                         assignTA("bkreischer@uwm.edu", "Comedy 252", "Lab 102", "jgaffigan@uwm.edu"),
                         msg="Entering valid inputs with no previous ta assigned to the section fails to return "
                             "\"TA successfully assigned to section\"")

    # If this test, or any other test in test_assign_ta, doesn't work, clear out the data base by going to admin page
    # and clearing out all previous entries. It will not run correctly if there are duplicate entries in the database
    def test_allExistPrev(self):
        self.assertEqual("TA successfully assigned to section",
                         assignTA("bkreischer@uwm.edu", "Comedy 252", "Lab 101", "jgaffigan@uwm.edu"),
                         msg="Entering valid inputs with a previous ta assigned to the section returns message "
                             "\"TA successfully assigned to section\"")
