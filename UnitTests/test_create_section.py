import unittest

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django

django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import createSection


class TestCreateSection(unittest.TestCase):
    def setUp(self):
        self.instructor = Employee.objects.create(EMP_EMAIL="jimgaffigan@uwm.edu", EMP_FNAME="Jim",
                                                  EMP_LNAME="Gaffigan", EMP_ROLE="Instructor", EMP_INITIAL="T",
                                                  EMP_PASSWORD="123")
        self.ta = Employee.objects.create(EMP_EMAIL="bertkreischer@uwm.edu", EMP_FNAME="Bert",
                                          EMP_LNAME="Kreischer", EMP_ROLE="TA", EMP_INITIAL="A",
                                          EMP_PASSWORD="456")
        self.course = Course.objects.create(title="Comedy 251", instructor=self.instructor)
        self.section = Section.objects.create(title="Lab 801", course=self.course, ta=self.ta, courseTitle="Comedy 251")

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
        self.assertEqual("TA does not exist, or employee is not TA",
                         createSection("Lab 802", "tomsegurra@uwm.edu", "Comedy 251"),
                         msg="Entering a TA that does not exist fails to return message "
                             "\"TA does not exist, or employee is not TA\"")

    def test_employeeNotTA(self):
        self.assertEqual("TA does not exist, or employee is not TA",
                         createSection("Lab 802", "jimgaffigan@uwm.edu", "Comedy 251"),
                         msg="Entering an employee that is not a TA for a section fails to return message "
                             "\"TA does not exist, or employee is not TA\"")

    def test_sectionExists(self):
        self.assertEqual("Section already exists", createSection("Lab 801", "bertkreischer@uwm.edu", "Comedy 251"),
                         msg="Entering a section that already exists fails to return message, "
                             "\"Section already exists\"")

    def test_validInput(self):
        self.assertEqual("Section successfully added",
                         createSection("Lab 807", "bertkreischer@uwm.edu", "Comedy 251"),
                         msg="Entering a valid ta, course, and title for a section fails to return message"
                             "\"Section successfully created\"")
