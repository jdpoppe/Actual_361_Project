from django.test import TestCase, Client
from school_app.models import Employee

class ViewInfo(TestCase):
    def setUp(self):
        self.client = Client()
        self.emp1 = Employee.objects.create(EMP_ROLE="Supervisor", EMP_LNAME="Diego", EMP_FNAME="DR", EMP_INITIAL="A",
                                            EMP_EMAIL="doming46@uwm.edu", EMP_PASSWORD="1234")
        self.emp2 = Employee.objects.create(EMP_ROLE="TA", EMP_LNAME="Lue", EMP_FNAME="C", EMP_INITIAL="",
                                            EMP_EMAIL="1234@uwm.edu", EMP_PASSWORD="1234")
        self.emp3 = Employee.objects.create(EMP_ROLE="Instructor", EMP_LNAME="Amanda", EMP_FNAME="DR", EMP_INITIAL="",
                                            EMP_EMAIL="1234@gmail.com", EMP_PASSWORD="1234")

    def test_validDisplay(self):
        response = self.client.post('/', {'j_username': self.emp1.EMP_EMAIL, 'j_password': self.emp1.EMP_PASSWORD})
        response = self.client.get("/viewUsers/")
        self.assertEqual(response.context["employees"], [('DR', 'A', 'Diego', 'Supervisor', 'doming46@uwm.edu'), ('C', '', 'Lue', 'TA', '1234@uwm.edu'), ('DR', '', 'Amanda', 'Instructor', '1234@gmail.com')], "failed to display the correct employee database")

