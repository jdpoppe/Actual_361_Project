from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import assignTA, createEmp

class TestAssignTA(TestCase):
    def setUp(self):
        self.employeeList = {"jimgaffigan@uwm.edu":["Jim", "Gaffigan", "Instructor","T", "123"],
                             "bertkreischer@uwm.edu":["Bert", "Kreischer", "TA", "A", "456"]}
        self.empObjects = list()
        self.empObjects = createEmp(self.employeeList,self.empObjects)
        self.course = Course(title="Comedy 252", instructor=self.empObjects[0])
        self.course.save()
        self.course2 = Course(title="Comedy 351")
        self.course.save()
        self.section = Section(title="Lab 101", course=self.course, emp=self.empObjects[1])
        self.section.save()


    def test_courseDNE(self):
        self.assertEqual("Course does not exist, or Instructor does not teach course",
                         assignTA("bertkreischer@uwm.edu","Comedy 458","Lab 101","jimgaffigan@uwm.edu"),
                         msg="Entering a course that does not exist fails to return message, "
                             "\"Course does not exist\"")


    def test_sectionDNE(self):
        self.assertEqual("Section does not exist",
                         assignTA("bertkreischer@uwm.edu","Comedy 252","Lab 103","jimgaffigan@uwm.edu"),
                         msg="Entering a section that DNE fails to return message \"Section does not exist\"")


    def test_taDNE(self):
        self.assertEqual("TA does not exist, or employee is not a TA",
                         assignTA("tomsegurra@uwm.edu", "Comedy 252", "Lab 101", "jimgaffigan@uwm.edu"),
                         msg="Entering a ta that DNE fails to return message "
                             "\"TA does not exist, or employee is not TA\"")

    def test_courseIsNotTaughtByInstructor(self):
        self.assertEqual("Course does not exist, or Instructor does not teach course",
                         assignTA("bertkreischer@uwm.edu", "Comedy 351", "Lab 101", "jimgaffigan@uwm.edu"),
                         msg = "Entering a course that the instructor does not teach fails to return message, "
                               "\"Course does not exist, or Instructor does not teach course\"")

    def test_allExistEmpNotTA(self):
        self.assertEqual("TA does not exist, or employee is not a TA",
                         assignTA("jimgaffigan@uwm.edu", "Comedy 252", "Lab 801", "jimgaffigan@uwm.edu"),
                         msg="Entering an employee that is not ta fails to return message"
                             "\"TA does not exist, or employee is not TA\"")


    def test_allExistNoPrev(self):
        self.assertEqual("TA successfully assigned to section",
                         assignTA("bertkreischer@uwm.edu", "Comedy 252", "Lab 101", "jimgaffigan@uwm.edu"),
                         msg="Entering valid inputs with no previous ta assigned to the section fails to return "
                             "\"TA successfully assigned to section\"")

    # If this test, or any other test in test_assign_ta, doesn't work, clear out the data base by going to admin page
    # and clearing out all previous entries. It will not run correctly if there are duplicate entries in the database
    def test_allExistPrev(self):
        self.assertEqual("TA successfully assigned to section",
                         assignTA("bertkreischer@uwm.edu", "Comedy 252", "Lab 101", "jimgaffigan@uwm.edu"),
                         msg="Entering valid inputs with a previous ta assigned to the section returns message "
                             "\"TA successfully assigned to section\"")
