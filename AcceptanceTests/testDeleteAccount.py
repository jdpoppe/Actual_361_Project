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
                             "idiot@baby.com":["Bartholomew", "Grundhold", "Supervisor", "B", "GwammaSux"],
                             "holy@god.com":["Dichophrates", "Smith", "Supervisor", "Z", "Dance4Lyfe"]}
        self.empObj = list()
        self.empObj = createEmp(self.employeeList, self.empObj)
        self.soupervisor = self.empObj[0]
        self.suprvisr = self.empObj[1]
        self.supervisor = self.empObj[2]

    def test_emailDNE(self):
        session = self.client.session
        session['email'] = "grandma@old.com"
        session.save()
        response = self.client.post("/deleteAccount/",
                                    {"accToDelete": "randma@old.com"})
        self.assertEqual(response.context["message"], "cannot delete your own or nonexistent accounts",
                         msg="accounts that don't exist in the db should not be erasable")

    def test_deleteSelf(self):
        session = self.client.session
        session['email'] = "grandma@old.com"
        session.save()
        response = self.client.post("/deleteAccount/",
                                    {"accToDelete": "grandma@old.com"})
        self.assertEqual(response.context["message"], "cannot delete your own or nonexistent accounts",
                         msg="You shouldn't be able to delete yourself")

    def test_deleteOther(self):
        session = self.client.session
        session['email'] = "holy@god.com"
        session.save()
        response = self.client.post("/deleteAccount/",
                                    {"accToDelete": "idiot@baby.com"})
        self.assertEqual(response.context["message"], "account has been deleted",
                         msg="You should be able to delete accounts in the db")