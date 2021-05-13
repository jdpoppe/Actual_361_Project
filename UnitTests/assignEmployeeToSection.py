from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import assignEmployeeToSection, createEmp



class TestAssignEmployeeToSection(TestCase):
    def setUp(self):
        self.employeeList = {"abc1@uwm.edu":["john","doe","Instructor","a","123"],
                             "abc2@uwm.edu":["james","doe","Instructor","a","123"],
                             "def1@uwm.edu":["jane","doe","TA","a","123"],
                             "ghi1@uwm.edu":["jack","doe","Supervisor","a","123"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.courseNoInstructor = Course(title="Class 1", instructor=None)
        self.courseNoInstructor.save()
        self.courseHasInstructor = Course.objects.create(title="Class 2", instructor=self.empObj[0])
        self.section1 = Section.objects.create(title="Section 1", course=self.courseNoInstructor)
        self.section2 = Section.objects.create(title="Section 2", course=self.courseHasInstructor)

    def test_courseDNE(self):
        self.assertEqual("Course does not exist", assignEmployeeToSection("def1@uwm.edu", "Section 1", "Class 0"),
                         msg="Entering a course that DNE fails to return correct message")

    def test_sectionDNE(self):
        self.assertEqual("Section does not exist", assignEmployeeToSection("def1@uwm.edu", "Section 0", "Class 1"),
                         msg="Entering a section that DNE fails to return message")

    def test_employeeDNE(self):
        self.assertEqual("Employee does not exist",
                         assignEmployeeToSection("jkl@uwm.edu", "Section 1", "Class 1"),
                         msg="Entering an employee that DNE fails to return correct message")

    def test_employeeSupervisor(self):
        self.assertEqual("You cannot assign a supervisor to a section",
                         assignEmployeeToSection("ghi1@uwm.edu", "Section 1", "Class 1"),
                         msg="Entering a supervisor fails to return correct message")

    def test_assignInsNotCourseIns(self):
        self.assertEqual("Course has different Instructor assigned to it, cannot assign new instructor to section",
                         assignEmployeeToSection("abc2@uwm.edu","Section 2", "Class 2"),
                         msg="Entering an instruction different from the instructor already assigned to the course "
                             "fails to return the correct message")

    def test_validTA(self):
        self.assertEqual("Employee successfully assigned to section",
                         assignEmployeeToSection("def1@uwm.edu", "Section 1", "Class 1"),
                         msg="Successfully assigning a valid TA to a course fails to return correct message")

    def test_validInsCourseHasIns(self):
        self.assertEqual("Employee successfully assigned to section",
                         assignEmployeeToSection("abc1@uwm.edu", "Section 1", "Class 1"),
                         msg="Entering a valid Instructor for a course they are already assigned to fails to return the"
                             " correct message")

    def test_validInsCourseDNHIns(self):
        self.assertEqual("Employee successfully assigned to section",
                         assignEmployeeToSection("abc1@uwm.edu", "Section 1", "Class 1"),
                         msg="Entering a valid instructor for a course that does not have an instructor assigned to "
                             "it fails to return the correct message")



