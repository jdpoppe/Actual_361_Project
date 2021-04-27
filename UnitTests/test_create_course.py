import unittest

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course
from school_app.Helpers import createCourse


# Create your tests here.

class TestCreateCourse(unittest.TestCase):
    def setUp(self):
        self.instructor = Employee.objects.create(Email_Field="jimgaffigan@uwm.edu", EMP_FNAME="Jim",
                                                  EMP_LNAME="Gaffigan", EMP_ROLE="Instructor", EMP_INITIAL="T",
                                                  EMP_PASSWORD="123")
        self.supervisor = Employee.objects.create(Email_Field="bertkreischer@uwm.edu", EMP_FNAME="Bert",
                                                  EMP_LNAME="Kreischer", EMP_ROLE="Supervisor", EMP_INITIAL="A",
                                                  EMP_PASSWORD="456")
        self.course = Course.objects.create(title="Comedy 251", instructor="jimgaffigan@uwm.edu")
    def test_noTitle(self):
        self.assertEqual("Course must have title", createCourse("", "jimgaffigan@uwm.edu"),
                         msg="Entering a course without a title fails to return message \"Course must have title\"")

    def test_courseExists(self):
        self.assertEqual("Course already exists", createCourse("Comedy 251", "jimgaffigan@uwm.edu"),
                         msg="Entering a course that already exists fails to return message "
                             "\"Course already exists\"")

    def test_instructorDNE(self):
        self.assertEqual("Instructor does not exist, or employee is not an Instructor",
                         createCourse("Comedy 361", "tomsegurra@uwm.edu"),
                         msg="Entering an instructor that does not exist fails to return message"
                             "\"Instructor does not exist, or employee is not an Instructor\"")

    def test_employeeNotInstructor(self):
        self.assertEqual("Instructor does not exist, or employee is not an Instructor",
                         createCourse("Comedy 361", "bertkreischer@uwm.edu"),
                         msg = "Entering an employee who is not an instructor does not return message, "
                               "\"Instructor does not exist, or employee is not an Instructor\"")

    def test_validInput(self):
        self.assertEqual("Course successfully created", createCourse("Comedy 351","jimgaffigan@uwm.edu"),
                         msg="Entering an untaken course title and instructor fails to return message "
                             "\"Course successfully created\"")


