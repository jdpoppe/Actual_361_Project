import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from django.test import TestCase
from school_app.models import Employee, Course, Section
from django.test import Client


class TestInstructorAssignTA(TestCase):
    def setUp(self):
        self.client = Client()
        if len(list(Employee.objects.filter(EMP_EMAIL="gaffigan@uwm.edu"))) < 1:
            self.instructor = Employee.objects.create(EMP_EMAIL="gaffigan@uwm.edu", EMP_FNAME="Jim",
                                                      EMP_LNAME="Gaffigan", EMP_ROLE="Instructor", EMP_INITIAL="T",
                                                      EMP_PASSWORD="123")
            self.ta = Employee.objects.create(EMP_EMAIL="kreischer@uwm.edu", EMP_FNAME="Bert",
                                              EMP_LNAME="Kreischer", EMP_ROLE="TA", EMP_INITIAL="A",
                                              EMP_PASSWORD="456")
            self.fakeTA = Employee.objects.create(EMP_EMAIL="", EMP_FNAME="",
                                                  EMP_LNAME="", EMP_ROLE="TA", EMP_INITIAL="",
                                                  EMP_PASSWORD="")
            self.course = Course.objects.create(title="Comedy 152", instructor=self.instructor)
            self.course2 = Course.objects.create(title="Comedy 151")
            self.section = Section.objects.create(title="Lab 201", course=self.course, emp=self.ta)
            self.section2 = Section.objects.create(title="Lab 202", course=self.course, emp=self.fakeTA)

        self.teach = Employee.objects.get(EMP_EMAIL="gaffigan@uwm.edu")

    def test_get(self):
        session = self.client.session
        session['email'] = "gaffigan@uwm.edu"
        session.save()
        response = self.client.get("/instructorAssignTA/")
        c = Course.objects.filter(instructor=self.teach)
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
        self.assertEqual(response.context["message"], "Course does not exist, or Instructor does not teach course",
                         msg="Entering a TA that DNE fails to return correct message")

    def test_CourseNotInstructors(self):
        session = self.client.session
        session["email"] = "gaffigan@uwm.edu"
        session.save()

        request = self.client.post("/instructorAssignTA/",
                                   {"email": "slime", "course": "Comedy 151", "section": "Lab 202"})
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
