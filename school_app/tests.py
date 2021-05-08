import os

from django.test import TestCase

# Create your tests here.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

# system testing TA sceduling App (tests.py) - Hamza

from django.test import TestCase
from .models import Employee, Course, Section


class LoginPass(TestCase):

    def setUp(self):
        self.user = Employee.object.create(ID=123, user_name="Bob123", password="admin")

    def test_correctUser(self):
        resp = self.user.POST('/', {"user_name": self.user.user_name, "password": self.user.password})
        self.assertEqual(resp.context["message"], "Valid login", msg="Direct to dashboard")


class LoginFail(TestCase):

    def setUp(self):
        self.user = Employee.object.create(ID=123, user_name="Bob123", password="admin")

    def test_wrongUsername(self):
        resp = self.user.post("/", {"user_name": "Bob12", "password": "admin"})
        self.assertEqual(resp.context["message"], "bad username", "user does not exist, failed login")

    def test_noPassword(self):
        resp = self.user.post("/", {"user_name": "Bob123", "password": ""})
        self.assertEqual(resp.context["message"], "bad password", "no password entered, failed login")

    def test_OtherUserPassword(self):
        resp = self.user.post("/", {"user_name": "Bob123", "password": "12345"})
        self.assertEqual(resp.context["message"], "bad password", "failed login, wrong password entered for user")


# on create account page
class CreateAccount(TestCase):

    def setUp(self):
        self.user = Employee.object.create(ID=123, user_name="Bob123", password="admin")

    def test_createAccount(self):
        result = self.user.POST('/', {"user_name": "Hm123", "password": "admin123"})
        self.assertEqual(result.context["message"], "Account Created", msg="New account created")

    def test_AccountAlreadyExists(self):
        result = self.user.POST('/', {"user_name": "Bob123", "password": "admin"})
        self.assertEqual(result.context["message"], "User already Exists",
                         msg="username already exists in the database. Direct to login page")


class CreateCourse(TestCase):

    def setUp(self):
        self.user = Employee.object.create(ID=123, user_name="Supervisor123", password="admin", title="supervisor")
        self.courseList = {"CS317", "CS351", "CS361"}

    # someone besides a supervisor tries to create a course
    def create_course_error(self):
        resp = self.user.post("/", {"title": "TA", "course": "CS535"})
        self.assertEqual(resp.context["message"], "bad entry", "only a supervisor can create a course")


# assign course/user to course
class AssignCourse(TestCase):

    def setUp(self):
        self.user = Employee.object.create(ID=2637, user_name="Bob123", password="admin", course="CS361")

    def assign_course_repeatedly(self):
        resp = self.user.post("/", {"user_name": "Bob123", "course": "CS361"})
        self.assertEqual(resp.context["message"], "bad entry", "course already assigned to select user")

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django

django.setup()
from django.test import TestCase
from school_app.models import Employee
from django.test import Client



class ProperDashboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.ta = Employee.objects.create(EMP_ROLE="TA", EMP_LNAME="Kreischer", EMP_FNAME="Bert",
                                          EMP_INITIAL="D", EMP_PASSWORD="123", EMP_EMAIL="bertkreischer@uwm.edu")
        self.instructor = Employee.objects.create(EMP_ROLE="Instructor", EMP_LNAME="Segurra", EMP_FNAME="Tom",
                                                  EMP_INITIAL="R", EMP_PASSWORD="123", EMP_EMAIL="tomsegurra@uwm.edu")
        self.supervisor = Employee.objects.create(EMP_ROLE="Supervisor", EMP_LNAME="Gaffigan", EMP_FNAME="Jim",
                                                  EMP_INITIAL="L", EMP_PASSWORD="123", EMP_EMAIL="jimgaffigan@uwm.edu")

    def test_skipLogIn(self):
        response = self.client.get('/')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context["user"], "Hacker", msg="Successfully logging in as hacker fails to display hacker"
                                                             " dashboard")
    def test_taLogin(self):
        response = self.client.post("/", {"j_username": self.ta.EMP_EMAIL,
                                          "j_password": self.ta.EMP_PASSWORD})
        self.assertEqual(response.url, "/dashboard/", msg="Successfully logging in as TA fails to redirect to "
                                                          "dashboard")
        response = self.client.get("/dashboard/")
        self.assertEqual(response.context["user"], "TA", msg="Successfully logging in as TA fails to display TA "
                                                             "dashboard")

    def test_instructorLogin(self):
        response = self.client.post("/", {"j_username": self.instructor.EMP_EMAIL,
                                          "j_password": self.instructor.EMP_PASSWORD})

        self.assertEqual(response.url, "/dashboard/", msg="Successfully logging in as instructor fails to redirect to "
                                                          "dashboard")
        response = self.client.get("/dashboard/")
        self.assertEqual(response.context["user"], "Instructor",
                         msg="Successfully logging in as Instructor fails to display Instructor dashboard")

    def test_supervisorLogin(self):
        response = self.client.post("/", {"j_username": self.supervisor.EMP_EMAIL,
                                          "j_password": self.supervisor.EMP_PASSWORD})

        self.assertEqual(response.url, "/dashboard/", msg="Successfully logging in as Supervisor fails to redirect to "
                                                          "dashboard")
        response = self.client.get("/dashboard/")
        self.assertEqual(response.context["user"], "Supervisor", msg="Successfully logging in as Supervisor fails to "
                                                                     "display Supervisor dashboard")