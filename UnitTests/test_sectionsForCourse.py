import unittest

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import sectionsForCourse


class TestSectionsForCourse(unittest.TestCase):
    def setUp(self):
        if(len(Course.objects.filter(title="Class 10"))) < 1:
            self.course = Course.objects.create(title="Class 10")
            self.ta1 = Employee.objects.create(EMP_EMAIL="toby@uwm.edu", EMP_INITIAL="B", EMP_FNAME="Toby",
                                               EMP_LNAME="Dog", EMP_ROLE="TA", EMP_PASSWORD="Bark")
            self.ta2 = Employee.objects.create(EMP_EMAIL="george@uwm.edu", EMP_INITIAL="B", EMP_FNAME="George",
                                               EMP_LNAME="Dog", EMP_ROLE="TA", EMP_PASSWORD="Bark")

        self.course = Course.objects.get(title="Class 10")
        self.ta1 = Employee.objects.get(EMP_EMAIL="toby@uwm.edu")
        self.ta2 = Employee.objects.get(EMP_EMAIL="george@uwm.edu")
    def test_noSections(self):
       self.assertEqual(sectionsForCourse("Class 10"), [], msg="A course with no sections fails to return empty list")

    def test_someSectionsWOTA(self):
        section1 = Section.objects.create(title="Section 10", course=self.course)
        section2 = Section.objects.create(title="Section 11", course=self.course)
        self.assertEqual(sectionsForCourse("Class 10"), [(section1.title, "No one", "assigned"),
                                                         (section2.title, "No one", "assigned")],
                         msg="Entering a course with sections that have no teachers fails to return correct list")

    def test_someSectionWTA(self):
        section1 = Section.objects.get(title="Section 10")
        section1.emp = self.ta1
        section1.save()
        section2 = Section.objects.get(title="Section 11")
        section2.emp = self.ta2
        section2.save()
        self.assertEqual(sectionsForCourse("Class 10"), [(section1.title, "Toby", "Dog"),
                                                         (section2.title, "George", "Dog")],
                         msg="Entering a course with sections that has teachers fails to return correct list")

    def test_duplicateTA(self):
        section1 = Section.objects.get(title="Section 10")
        section2 = Section.objects.get(title="Section 11")
        section2.ta = section1.ta
        section2.save()
        self.assertEqual(sectionsForCourse("Class 10"))

    def test_invalidCourse(self):
        with self.assertRaises(TypeError, msg="Entering an invalid course fails to raise type error"):
            sectionsForCourse("poasidfjposaij")

