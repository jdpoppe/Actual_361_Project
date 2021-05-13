from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import sectionsForCourse, createEmp


class TestSectionsForCourse(TestCase):
    def setUp(self):
        self.employeeList = {"toby@uwm.edu": ["Toby", "Dog", "TA", "B", "Bark"],
                             "george@uwm.edu": ["George", "Dog", "TA", "B", "Bark"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.ta1 = self.empObj[0]
        self.ta2 = self.empObj[1]
        self.course = Course(title="Class 10")
        self.course.save()

    def test_noSections(self):
       self.assertEqual(sectionsForCourse("Class 10"), [], msg="A course with no sections fails to return empty list")

    def test_someSectionsWOTA(self):
        section1 = Section(title="Section 10", course=self.course)
        section1.save()
        section2 = Section(title="Section 11", course=self.course)
        section2.save()
        self.assertEqual(sectionsForCourse("Class 10"), [(section1.title, "No one", "assigned"),
                                                         (section2.title, "No one", "assigned")],
                         msg="Entering a course with sections that have no teachers fails to return correct list")

    def test_someSectionWTA(self):
        section1 = Section(title="Section 10", course=self.course)
        section1.emp = self.ta1
        section1.save()
        section2 = Section(title="Section 11", course=self.course)
        section2.emp = self.ta2
        section2.save()
        self.assertEqual(sectionsForCourse("Class 10"), [(section1.title, "Toby", "Dog"),
                                                         (section2.title, "George", "Dog")],
                         msg="Entering a course with sections that has teachers fails to return correct list")

    def test_duplicateTA(self):
        section1 = Section(title="Section 10", course= self.course, emp=self.ta1)
        section1.save()
        section2 = Section(title="Section 11", course= self.course, emp=self.ta1)
        section2.save()
        self.assertEqual(sectionsForCourse("Class 10"), [(section1.title, self.ta1.EMP_FNAME, self.ta2.EMP_LNAME),
                                                         (section2.title, self.ta1.EMP_FNAME, self.ta2.EMP_LNAME)])

    def test_invalidCourse(self):
        with self.assertRaises(TypeError, msg="Entering an invalid course fails to raise type error"):
            sectionsForCourse("poasidfjposaij")

