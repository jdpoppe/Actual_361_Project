from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import createEmp
from django.test import Client

class TestViewCourse(TestCase):
    def setUp(self):
        self.employeeList = {"rachminoff@uwm.edu":["Jim","Rachminoff","Instructor","T","123"],
                             "hugarian@uwm.edu":["Hungarian","Waltz","TA","A","456"],
                             "music@uwm.edu":["Max","Volume","TA","A","456"]}
        self.empObj = list()
        self. empObj = createEmp(self.employeeList, self.empObj)
        self.client = Client()
        self.instructor = self.empObj[0]
        self.ta1 = self.empObj[1]
        self.ta2 = self.empObj[2]



    def test_getNoCourses(self):
        response = self.client.get("/ViewAllCourses/")
        self.assertEqual(response.context["courses"], [], "Rendering View Courses page fails to return an empty list"
                                                          "when there are no course in the DB")
        self.assertEqual(response.context["currentCourse"],"Select a Course",
                         msg="Rendering the View Courses page for the first time fails to have message "
                             "\"Select a Course\"")

    def test_getCourses(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        course2 = Course(title="Course 15")
        course2.save()
        response = self.client.get("/ViewAllCourses/")
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"],
                         msg="Rendering View Courses page fails to return an empty list when there are no course in the "
                             "DB")
        self.assertEqual(response.context["currentCourse"], "Select a Course",
                         msg="Rendering the View Courses page for the first time fails to have message "
                             "\"Select a Course\"")


    def test_invalidCourse(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        course2 = Course(title="Course 15")
        course2.save()
        response = self.client.post("/ViewAllCourses/",{"currentCourse":"a;lsdkfja"})
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"], msg="Entering an invalid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Course Does not Exist", msg="Entering invalid coures fails to "
                                                                                      "post error message through "
                                                                                      "currentCourse")
        self.assertEqual(response.context["allSections"], [], msg="Entering invalid course fails to post empty list"
                                                                  "of sections")
        self.assertEqual(response.context["allTA"], [], msg="Entering invalid course fails to post empty list of TA")
        self.assertEqual(response.context["currentCourse"], "Please Enter Valid Course",
                         msg="Entering an invalid course fails to return currentCourse as correct message")

    def test_noInstructor(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        course2 = Course(title="Course 15")
        course2.save()
        response = self.client.post("/ViewAllCourses/",{"currentCourse":"Course 15"})
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Instructor Not Assigned Yet",
                         msg="Instructor value invalid after entering course with no instructor")
        self.assertEqual(response.context["allSections"], [], msg="Entering course with no sections fails to procure"
                                                                  "the appropriate list")
        self.assertEqual(response.context["allTA"], [], msg="Entering course with no TA fails to procure an empty list")

    def test_noSections(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        course2 = Course(title="Course 15")
        course2.save()
        response = self.client.post("/ViewAllCourses/", {"currentCourse": "Course 14"})
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="Instructor value invalid after entering course with no instructor")
        self.assertEqual(response.context["allSections"], [], msg="Entering course with no sections fails to procure"
                                                                  "the appropriate list")
        self.assertEqual(response.context["allTA"], [], msg="Entering course with no TA fails to procure an empty list")

    def test_noTA(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        section1 = Section(title="Section 14",course=course1)
        section1.save()
        course2 = Course(title="Course 15")
        course2.save()
        response = self.client.post("/ViewAllCourses/", {"currentCourse": "Course 14"})
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="Instructor value invalid after entering course with no instructor")
        self.assertEqual(response.context["allSections"], [("Section 14","No one", "assigned")],
                         msg="Entering a course with sections and no TA fails to procure correct list")
        self.assertEqual(response.context["allTA"], [],
                         msg="Entering a course with no TAs fails to post empty list of TA")

    def test_oneOfEach(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        course2 = Course(title="Course 15")
        course2.save()
        section = Section(title="Section 14", course=course1, emp=self.ta1)
        section.save()
        response = self.client.post("/ViewAllCourses/", {"currentCourse": "Course 14"})
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="instructor value is invalid after entering course with instructor")
        self.assertEqual(response.context["allSections"], [("Section 14", "Hungarian","Waltz")],
                         msg="allSections value is invalid after entering course with one TA and one section")
        self.assertEqual(response.context["allTA"], [("Hungarian","Waltz")],
                         msg="allTA value is invalid after entering course with one TA and one section")

    def test_manyOfEach(self):
        course1 = Course(title="Course 14", instructor=self.instructor)
        course1.save()
        course2 = Course(title="Course 15")
        course2.save()
        section1 = Section(title="Section 14", course=course1, emp=self.ta1)
        section1.save()
        section2 = Section(title="Section 15", course=course1, emp=self.ta2)
        section2.save()
        response = self.client.post("/ViewAllCourses/", {"currentCourse": "Course 14"})
        self.assertEqual(response.context["courses"], ["Course 14", "Course 15"], msg="Entering an invalid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="instructor value is invalid after entering course with instructor")
        self.assertEqual(response.context["allSections"], [("Section 14", "Hungarian", "Waltz"),
                                                           ("Section 15", "Max", "Volume")],
                         msg="Entering a course with multiple sections and TAs fails to return correct list")
        self.assertEqual(response.context["allTA"], [("Hungarian", "Waltz"),("Max","Volume")],
                         msg="Entering a course with multiple TAs fails to post correct list")