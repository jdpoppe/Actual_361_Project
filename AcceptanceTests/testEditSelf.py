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
        self.employeeList = {"grandma@old.com":["Dolores", "Grundhold", "Supervisor", "D", "Ih8Kids"],
                             "idiot@baby.fart":["Bartholomew", "Grundhold", "Supervisor", "B", "GwammaSux"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.soupervisor = self.empObj[0]
        self.suprvisr = self.empObj[1]

    def test_emailAlreadyExists(self):
        session = self.client.session
        session['email'] = "grandma@old.com"
        session.save()
        response = self.client.post("/editSelf/",
                                    {"f_name": "olores", "initial": "F",
                                     "l_name": "rundhold", "email": "idiot@baby.fart",
                                     "password": "h8Kids"})
        self.assertEqual(response.context["message"], "email already exists",
                         msg="the new email cannot currently exist in the db")

    def test_editSelf(self):
        session = self.client.session
        session['email'] = "grandma@old.com"
        session.save()
        response = self.client.post("/editSelf/",
                                    {"f_name": "olores", "initial": "F",
                                     "l_name": "rundhold", "email": "randma@old.com",
                                     "password": "h8Kids"})
        self.assertEqual(response.context["message"], "account successfully updated",
                         msg="name has not been changed correctly")