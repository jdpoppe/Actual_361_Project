from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import createEmp
from django.test import Client


class TestInstructorAssignTA(TestCase):
    def setUp(self):
        self.client = Client()
        self.employeeList = {"gaffigan@uwm.edu":["Jim","Gaffigan","Instructor","T","123"],
                             "kreischer@uwm.edu":["Bert","Kreischer","TA","A","456"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.instructor = self.empObj[0]
        self.ta = self.empObj[1]
        self.course = Course.objects.create(title="Comedy 152", instructor=self.instructor)
        self.course2 = Course.objects.create(title="Comedy 151")
        self.section = Section.objects.create(title="Lab 201", course=self.course, emp=self.ta)



    def test_get(self):
        session = self.client.session
        session['email'] = "gaffigan@uwm.edu"
        session.save()
        response = self.client.get("/instructorAssignTA/")
        c = Course.objects.filter(instructor=self.instructor)
        courses = list()
        for i in c:
            courses.append(i.title)
        self.assertEqual(response.context["courses"], courses,
                         msg="Visiting assign TA page as instructor fails to create list of all classes"
                             "that instructor teaches")

    def test_sectionDNE(self):
        session = self.client.session
        session["email"] = "gaffigan@uwm.edu"
        session.save()
        response = self.client.post("/instructorAssignTA/",
                                    {"email": "kreischer@uwm.edu", "course": "Comedy 152", "section": "Lab 102"})
        self.assertEqual(response.context["message"], "Section does not exist",
                         msg="Entering an invalid section fails to return correct message")

    def test_courseDNE(self):
        session = self.client.session
        session["email"] = "gaffigan@uwm.edu"
        session.save()
        request = self.client.post("/instructorAssignTA/",
                                   {"email": "kreischer@uwm.edu", "course": "Comedy 252", "section": "Lab 202"})
        self.assertEqual(request.context["message"], "Course does not exist, or Instructor does not teach course",
                         msg="Entering an invalid course fails to return correct message")

    def test_taDNE(self):
        session = self.client.session
        session["email"] = "gaffigan@uwm.edu"
        session.save()
        response = self.client.post("/instructorAssignTA/",
                                    {"email": "slime", "course": "Comedy 152", "section": "Lab 202"})
        self.assertEqual(response.context["message"], "TA does not exist, or employee is not a TA",
                         msg="Entering a TA that DNE fails to return correct message")

    def test_CourseNotInstructors(self):
        session = self.client.session
        session["email"] = "gaffigan@uwm.edu"
        session.save()

        request = self.client.post("/instructorAssignTA/",
                                   {"email": "kreischer@uwm.edu", "course": "Comedy 151", "section": "Lab 202"})
        self.assertEqual(request.context["message"], "Course does not exist, or Instructor does not teach course",
                         msg="Entering a course that isn't the instructor's fails to return correct message")

    def test_successfulAssignment(self):
        session = self.client.session
        session["email"] = "gaffigan@uwm.edu"
        session.save()
        request = self.client.post("/instructorAssignTA/",
                                   {"email": "kreischer@uwm.edu", "course": "Comedy 152", "section": "Lab 201"})
        self.assertEqual(request.context["message"], "TA successfully assigned to section",
                         msg="Successfully assigning TA fails to return correct message")
