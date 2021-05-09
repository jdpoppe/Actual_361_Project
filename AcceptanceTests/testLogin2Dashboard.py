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
