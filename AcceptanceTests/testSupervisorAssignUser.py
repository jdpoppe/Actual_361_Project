from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import createEmp
from django.test import Client


class TestSupervisorAssign(TestCase):
    def setUp(self):
        self.client = Client()
        self.employeeList = {"abc1@uwm.edu":["john","doe","Instructor","a","123"],
                             "abc3@uwm.edu":["james","doe","Instructor","a","123"],
                             "def3@uwm.edu":["jane","doe","TA","a","123"],
                             "ghi3@uwm.edu":["jack","doe","Supervisor","a","123"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.courseNoInstructor = Course(title="Class 3")
        self.courseNoInstructor.save()
        self.courseHasInstructor = Course(title="Class 4", instructor=self.empObj[0])
        self.courseHasInstructor.save()
        self.section1 = Section(title="Section 3", course=self.courseNoInstructor)
        self.section1.save()
        self.section2 = Section(title="Section 4", course=self.courseHasInstructor)
        self.section2.save()
        self.courses = ["Class 3", "Class 4"]

    def test_get(self):
        response = self.client.get("/assignTA/")
        self.assertEqual(response.context["courses"], self.courses, "The incorrect course's list gets loaded when "
                                                                    "the assignTA page is rendered")

    def test_invalidCourse(self):
        response = self.client.post("/assignTA/",
                                    {"email": "abc1@uwm.edu", "section": "Section 3", "course": "Class 0"})
        self.assertEqual(response.context["message"], "Course does not exist",
                         msg="Entering a course that DNE fails to post correct message")

        self.assertEqual(response.context["courses"], self.courses, "Entering a course that DNE fails to post correct"
                                                                    "list of all courses")

    def test_invalidSection(self):
        response = self.client.post("/assignTA/",
                                    {"email": "abc1@uwm.edu", "section": "Section 0", "course": "Class 3"})
        self.assertEqual(response.context["message"], "Section does not exist",
                         msg="Entering a section that DNE fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses, msg="Entering a section that DNE fails to post "
                                                                        "correct list of all courses")

    def test_empDNE(self):
        response = self.client.post("/assignTA/", {"email": "oops!", "section": "Section 3", "course": "Class 3"})
        self.assertEqual(response.context["message"], "Employee does not exist",
                         msg="Entering an employee that DNE fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses, msg="Entering an employee that DNE fails to post "
                                                                        "correct list of all courses")

    def test_empIsSupervisor(self):
        response = self.client.post("/assignTA/",
                                    {"email": "ghi3@uwm.edu", "section": "Section 3", "course": "Class 3"})
        self.assertEqual(response.context["message"], "You cannot assign a supervisor to a section",
                         msg="Entering a supervisor fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses, msg="Entering a supervisor fails to post "
                                                                        "correct list of all courses")

    def test_validTA(self):
        response = self.client.post("/assignTA/",
                                    {"email": "def3@uwm.edu", "section": "Section 3", "course": "Class 3"})
        self.assertEqual(response.context["message"], "Employee successfully assigned to section",
                         msg="Successfully assigning a ta to a section fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses, msg="Successfully assigning a ta to a section "
                                                                        "fails correct list of all courses")

    def test_courseNoInstructor(self):
        response = self.client.post("/assignTA/",
                                    {"email": "abc3@uwm.edu", "section": "Section 3", "course": "Class 3"})
        self.assertEqual(response.context["message"], "Employee successfully assigned to section",
                         msg="Successfully assigning an instructor to a section in a course without an instructor"
                             " fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses,
                         msg="Successfully assigning an instructor to a section in a course without an instructor"
                             "fails correct list of all courses")

    def test_courseInstructorIsInstructor(self):
        response = self.client.post("/assignTA/",
                                    {"email": "abc1@uwm.edu", "section": "Section 4", "course": "Class 4"})
        self.assertEqual(response.context["message"], "Employee successfully assigned to section",
                         msg="Successfully assigning an instructor to a section in their own course"
                             " fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses,
                         msg="Successfully assigning an instructor to a section in their own course"
                             "fails correct list of all courses")

    def test_courseInstructorNotInstructor(self):
        response = self.client.post("/assignTA/",
                                    {"email": "abc3@uwm.edu", "section": "Section 4", "course": "Class 4"})
        self.assertEqual(response.context["message"],
                         "Course has different Instructor assigned to it, cannot assign new instructor to section",
                         msg="Trying to assign a instructor to a section in a course they are not assigned to"
                             " fails to post correct message")
        self.assertEqual(response.context["courses"], self.courses,
                         msg="Trying to assign a instructor to a section in a course they are not assigned to"
                             "fails correct list of all courses")
