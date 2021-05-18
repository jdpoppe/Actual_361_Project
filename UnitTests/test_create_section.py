from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import createSection,createEmp


class TestCreateSection(TestCase):
    def setUp(self):
        self.employeeList = {"jimgaffigan@uwm.edu":["Jim","Gaffigan","Instructor","T","123"],
                             "bertkreischer@uwm.edu":["Bert","Kreischer","TA","A","456"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.course = Course(title="Comedy 251", instructor=self.empObj[0])
        self.course.save()
        self.section = Section(title="Lab 801", course=self.course, emp=self.empObj[1])
        self.section.save()

    def test_noTitle(self):
        self.assertEqual("Section needs to have title",
                         createSection("", "jimgaffigan@uwm.edu", "Comedy 251"),
                         msg="Entering a section with no title fails to return message \"Section needs title\"")

    def test_noCourse(self):
        self.assertEqual("Section needs to have a course", createSection("Lab 802", "bertkreischer@uwm.edu", ""),
                         msg="Entering a section with no parent course fails to return message, \"Must enter course\"")

    def test_courseDNE(self):
        self.assertEqual("Course does not exist", createSection("Lab 802", "bertkreischer@uwm.edu", "Comedy 361"),
                         msg="Entering a section with a course that does not exist fails to return message, "
                             "\"Course does not exists\"")

    def test_taDNE(self):
        self.assertEqual("Employee does not exist, or employee is a supervisor",
                         createSection("Lab 802", "tomsegurra@uwm.edu", "Comedy 251"),
                         msg="Entering a TA that does not exist fails to return message "
                             "\"Employee does not exist, or employee is supervisor\"")

    def test_employeeNotTA(self):
        self.assertEqual("Employee does not exist, or employee is a supervisor",
                         createSection("Lab 802", "gaffigan@uwm.edu", "Comedy 251"),
                         msg="Entering an employee that is not a TA for a section fails to return message "
                             "\"Employee does not exist, or employee is supervisor\"")

    def test_validInputNoTaInput(self):
        self.assertEqual("Section successfully added",
                         createSection("Lab 800", "", "Comedy 251"),
                         msg="Entering a valid course and title with no Ta fails to return correct message")

    def test_validInput(self):
        self.assertEqual("Section successfully added",
                         createSection("Lab 807", "bertkreischer@uwm.edu", "Comedy 251"),
                         msg="Entering a valid ta, course, and title for a section fails to return message"
                             "\"Section successfully created\"")
