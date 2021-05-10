import unittest

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import taForCourse


class TestTAForCourse(unittest.TestCase):
    def setUp(self):
        if len((Course.objects.filter(title="Class 11"))) < 1:
            self.course = Course.objects.create(title="Class 11")
            self.ta1 = Employee.objects.create(EMP_EMAIL="bob@uwm.edu", EMP_INITIAL="B", EMP_FNAME="Bob",
                                               EMP_LNAME="Dog", EMP_ROLE="TA", EMP_PASSWORD="Bark")
            self.ta2 = Employee.objects.create(EMP_EMAIL="hannah@uwm.edu", EMP_INITIAL="B", EMP_FNAME="Hannah",
                                               EMP_LNAME="Dog", EMP_ROLE="TA", EMP_PASSWORD="Bark")
        self.course = Course.objects.get(title="Class 11")
        self.ta1 = Employee.objects.get(EMP_EMAIL="bob@uwm.edu")
        self.ta2 = Employee.objects.get(EMP_EMAIL="hannah@uwm.edu")



    def test_noSectionNoTAs(self):
        self.assertEqual(taForCourse(self.course.title), [], "Entering course with no sections fails to return None")

    def test_sectionNoTAs(self):
        section = Section.objects.create(title="Section 12", course=self.course)
        self.assertEqual(taForCourse(self.course.title), [], "Entering course with sections that have no TA fails to "
                                                               "return None")

    def test_uniqueTAs(self):
        section1 = Section.objects.get(title="Section 12")
        section1.emp = self.ta1
        section1.save()
        section2 = Section.objects.create(title="Section 13", course=self.course, emp=self.ta2)
        self.assertEqual(taForCourse(self.course.title), [(self.ta1.EMP_FNAME, self.ta1.EMP_LNAME),
                                                          (self.ta2.EMP_FNAME, self.ta2.EMP_LNAME)],
                         msg="Entering a course with sections that have unique teachers for each class fails to return"
                             " the correct list")


    def test_duplicateTAs(self):
        section1 = Section.objects.get(title="Section 12")
        section2 = Section.objects.get(title="Section 13")
        section2.emp = self.ta1
        section2.save()
        self.assertEqual(taForCourse(self.course.title), [(self.ta1.EMP_FNAME, self.ta1.EMP_LNAME)],
                         msg="Entering a course with duplicate ta's fails to return correct list")

    def test_invalidCourse(self):
        with self.assertRaises(TypeError, msg="Entering an invalid course fails to raise type error"):
            taForCourse("poasidfjposaij")