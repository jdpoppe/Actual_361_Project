import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from django.test import TestCase
from school_app.models import Employee, Course, Section
from django.test import Client

class TestViewCourse(TestCase):
    def setUp(self):
        self.instructor = Employee.objects.create(EMP_EMAIL="rachminoff@uwm.edu", EMP_FNAME="Jim",
                                                  EMP_LNAME="Rachminoff", EMP_ROLE="Instructor", EMP_INITIAL="T",
                                                  EMP_PASSWORD="123")
        self.ta = Employee.objects.create(EMP_EMAIL="hugarian@uwm.edu", EMP_FNAME="Hungarian",
                                          EMP_LNAME="Waltz", EMP_ROLE="TA", EMP_INITIAL="A",
                                          EMP_PASSWORD="456")
        self.ta2 = Employee.objects.create(EMP_EMAIL="music@uwm.edu", EMP_FNAME="Max",
                                          EMP_LNAME="Volume", EMP_ROLE="TA", EMP_INITIAL="A",
                                          EMP_PASSWORD="456")
        self.client = Client()



    def test_getNoCourses(self):
        response = self.client.get("/ViewAllCourses/")
        self.assertEqual(response.context["courses"], [], "Rendering View Courses page fails to return an empty list"
                                                          "when there are no course in the DB")
        self.assertEqual(response.context["currentCourse"],"Select a Course",
                         msg="Rendering the View Courses page for the first time fails to have message "
                             "\"Select a Course\"")

    def test_getCourses(self):
        Course.objects.create(title="Course 14", instructor=self.instructor)
        Course.objects.create(title="Course 15")
        response = self.client.get("/ViewAllCourses/")
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"],
                         msg="Rendering View Courses page fails to return an empty list when there are no course in the "
                             "DB")
        self.assertEqual(response.context["currentCourse"], "Select a Course",
                         msg="Rendering the View Courses page for the first time fails to have message "
                             "\"Select a Course\"")


    def test_invalidCourse(self):
        response = self.client.post("/ViewAllCourses/",{"currentCourse":"a;lsdkfja"})
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"], msg="Entering an invalid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Course Does Not Exist", msg="Entering invalid coures fails to "
                                                                                      "post error message through "
                                                                                      "currentCourse")
        self.assertEqual(response.context["allSections"], [], msg="Entering invalid course fails to post empty list"
                                                                  "of sections")
        self.assertEqual(response.context["allTa"], [], msg="Entering invalid course fails to post empty list of TA")
        self.assertEqual(response.context["currentCourse"], "Please Enter Valid Course",
                         msg="Entering an invalid course fails to return currentCourse as correct message")

    def test_noInstructor(self):
        response = self.client.post("/ViewAllCourses/",{"currentCourse":"Course15"})
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Instructor Not Assigned Yet",
                         msg="Instructor value invalid after entering course with no instructor")
        self.assertEqual(response.context["allSections"], [], msg="Entering course with no sections fails to procure"
                                                                  "the appropriate list")
        self.assertEqual(response.context["allTa"], [], msg="Entering course with no TA fails to procure an empty list")

    def test_noSections(self):
        response = self.client.post("/ViewAllCourses", {"currentCourse": "Course14"})
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="Instructor value invalid after entering course with no instructor")
        self.assertEqual(response.context["allSections"], [], msg="Entering course with no sections fails to procure"
                                                                  "the appropriate list")
        self.assertEqual(response.context["allTa"], [], msg="Entering course with no TA fails to procure an empty list")

    def test_noTA(self):
        course = Course.objects.get(title="Course 14")
        Section.objects.create(title="Section 14", course=course)
        response = self.client.post("/ViewAllCourses", {"currentCourse": "Course14"})
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="Instructor value invalid after entering course with no instructor")
        self.assertEqual(response.context["allSections"], [("Section14","No one", "Assigned")],
                         msg="Entering a course with sections and no TA fails to procure correct list")
        self.assertEqual(response.context["allTa"], [],
                         msg="Entering a course with no TAs fails to post empty list of TA")

    def test_oneOfEach(self):
        section = Section.objects.get(title="Section 14")
        section.ta = self.ta
        section.save()
        response = self.client.post("/ViewAllCourses", {"currentCourse": "Course14"})
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"], msg="Entering a valid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="instructor value is invalid after entering course with instructor")
        self.assertEqual(response.context["allSections"], [("Section14", "Hungarian","Waltz")],
                         msg="allSections value is invalid after entering course with one TA and one section")
        self.assertEqual(response.context["allTa"], [("Hungarian","Waltz")],
                         msg="allTA value is invalid after entering course with one TA and one section")

    def test_manyOfEach(self):
        course = Course.objects.get(title="Course 14")
        section = Section.objects.create(title="Section 15",course=course,emp=self.ta2)
        response = self.client.post("/ViewAllCourses", {"currentCourse": "Course14"})
        self.assertEqual(response.context["courses"], ["Course14", "Course 15"], msg="Entering an invalid course fails"
                                                                                     "to post all courses")
        self.assertEqual(response.context["instructor"], "Jim Rachminoff",
                         msg="instructor value is invalid after entering course with instructor")
        self.assertEqual(response.context["allSections"], [("Section14", "Hungarian", "Waltz"),
                                                           ("Section15", "Max", "Volume")],
                         msg="Entering a course with multiple sections and TAs fails to return correct list")
        self.assertEqual(response.context["allTa"], [("Hungarian", "Waltz"),("Max","Volume")],
                         msg="Entering a course with multiple TAs fails to post correct list")