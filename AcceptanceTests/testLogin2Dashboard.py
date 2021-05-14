from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Course, Section
from school_app.Helpers import createEmp
from django.test import Client


class ProperDashboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.employeeList = {"bertkreischer@uwm.edu":["Bert","Kreischer","TA","D","123"],
                             "tomsegurra@uwm.edu":["Tom","Segurra","Instructor","D","123"],
                             "jimgaffigan@uwm.edu":["Jim","Gaffigan","Supervisor","L","123"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.ta = self.empObj[0]
        self.instructor = self.empObj[1]
        self.supervisor = self.empObj[2]

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
