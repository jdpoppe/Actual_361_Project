from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import taForCourse, createEmp


class TestTAForCourse(TestCase):
    def setUp(self):
        self.employeeList = {"toby@uwm.edu": ["Bob", "Dog", "TA", "B", "Bark"],
                             "george@uwm.edu": ["Hannah", "Dog", "TA", "B", "Bark"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.course = Course(title="Class 11")
        self.course.save()
        self.ta1 = self.empObj[0]
        self.ta2 = self.empObj[1]



    def test_noSectionNoTAs(self):
        self.assertEqual(taForCourse(self.course.title), [], "Entering course with no sections fails to return None")

    def test_sectionNoTAs(self):
        section = Section(title="Section 12", course=self.course)
        section.save()
        self.assertEqual(taForCourse(self.course.title), [], "Entering course with sections that have no TA fails to "
                                                               "return None")

    def test_uniqueTAs(self):
        section1 = Section(title="Section 12", course=self.course, emp=self.ta1)
        section1.save()
        section2 = Section(title="Section 13", course=self.course, emp=self.ta2)
        section2.save()
        self.assertEqual(taForCourse(self.course.title), [(self.ta1.EMP_FNAME, self.ta1.EMP_LNAME),
                                                          (self.ta2.EMP_FNAME, self.ta2.EMP_LNAME)],
                         msg="Entering a course with sections that have unique teachers for each class fails to return"
                             " the correct list")


    def test_duplicateTAs(self):
        section1 = Section(title="Section 12", course=self.course, emp=self.ta1)
        section1.save()
        section2 = Section(title="Section 13", course=self.course, emp=self.ta1)
        section2.save()
        self.assertEqual(taForCourse(self.course.title), [(self.ta1.EMP_FNAME, self.ta1.EMP_LNAME)],
                         msg="Entering a course with duplicate ta's fails to return correct list")

    def test_invalidCourse(self):
        with self.assertRaises(TypeError, msg="Entering an invalid course fails to raise type error"):
            taForCourse("poasidfjposaij")