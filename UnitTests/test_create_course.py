import unittest

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import createCourse, createSection, assignTA, assignInstructor


# Create your tests here.

class TestCreateCourse(unittest.TestCase):
    def setUp(self):
        self.instructor = Employee.objects.create(Email_Field="jimgaffigan@uwm.edu", EMP_FNAME="Jim",
                                                  EMP_LNAME="Gaffigan", EMP_ROLE=1, EMP_INITIAL="T", EMP_PASSWORD="123")
        self.course = Course.objects.create(title="Comedy 251", instructor="jimgaffigan@uwm.edu")
    def test_noTitle(self):
        self.assertEqual("Course must have title", createCourse("", "jimgaffigan@uwm.edu"),
                         msg="Entering a course without a title fails to return message \"Course must have title\"")

    def test_courseExists(self):
        self.assertEqual("Course already exists", createCourse("Comedy 251", "jimgaffigan@uwm.edu"))

    def test_instructorDNE(self):
        self.assertEqual("Instructor does not exist", createCourse("Comedy 361", "tomsegurra@uwm.edu"))

    def test_instruc
