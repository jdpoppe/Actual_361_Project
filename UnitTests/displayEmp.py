import unittest
from django.test import TestCase, Client
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee
from school_app.Helpers import displayEmp

# database needs to be empty
class TestDisplayEmp(unittest.TestCase):
    def setUp(self):
        self.emp1 = Employee.objects.create(EMP_ROLE="Supervisor", EMP_LNAME="Diego", EMP_FNAME="DR", EMP_INITIAL="A", EMP_EMAIL="doming46@uwm.edu", EMP_PASSWORD="1234")
        self.emp2 = Employee.objects.create(EMP_ROLE="TA", EMP_LNAME="Lue", EMP_FNAME="C", EMP_INITIAL="", EMP_EMAIL="1234@uwm.edu", EMP_PASSWORD="1234")
        self.emp3 = Employee.objects.create(EMP_ROLE="Instructor", EMP_LNAME="Amanda", EMP_FNAME="DR", EMP_INITIAL="", EMP_EMAIL="1234@gmail.com", EMP_PASSWORD="1234")

    def test_display(self):
        print(displayEmp())
        self.assertEqual(displayEmp(), [('DR', 'A', 'Diego', 'Supervisor', 'doming46@uwm.edu'), ('C', '', 'Lue', 'TA', '1234@uwm.edu'), ('DR', '', 'Amanda', 'Instructor', '1234@gmail.com')], 'Failed to display the correct Employees in the database')

    def tearDown(self):
        self.emp1.delete()
        self.emp2.delete()
        self.emp3.delete()
