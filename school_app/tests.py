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