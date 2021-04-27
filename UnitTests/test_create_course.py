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

    def test_noTitle(self):
        self.assertEqual("Course must have title", createCourse("", "jimgaffigan@uwm.edu"),
                         msg="Entering a course without a title fails to return message \"Course must have title\"")

