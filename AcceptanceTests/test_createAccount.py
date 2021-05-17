from django.test import TestCase, Client
from school_app.models import Employee

class TestCreateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Employee.objects.create(EMP_ROLE="Supervisor", EMP_LNAME="Diego", EMP_FNAME="DR", EMP_INITIAL="A",
                                            EMP_EMAIL="doming46@uwm.edu", EMP_PASSWORD="1234")
        self.emp1 = Employee(EMP_ROLE="Instructor", EMP_LNAME="Amanda", EMP_FNAME="DR", EMP_INITIAL="",
                                            EMP_EMAIL="1234@gmail.com", EMP_PASSWORD="1234")
        self.response = self.client.post('/', {'j_username': self.user1.EMP_EMAIL, 'j_password': self.user1.EMP_PASSWORD}, follow=True)
        self.response = self.client.get('/createAccount/')

    def test_validAdd(self):
        self.response = self.client.post('/createAccount/', {"f_name": self.emp1.EMP_FNAME, "initial": self.emp1.EMP_INITIAL, "l_name": self.emp1.EMP_LNAME, "role": self.emp1.EMP_ROLE, "email": self.emp1.EMP_EMAIL, "password": self.emp1.EMP_PASSWORD})
        self.assertEqual(self.response.context['message'], 'Account created',
                         'Failed to create valid account')
        self.assertEqual(self.response.context["entries"], [('DR', 'A', 'Diego', 'Supervisor', 'doming46@uwm.edu'), ('DR', '', 'Amanda', 'Instructor', '1234@gmail.com')], "failed to display employees after successful add")

    def test_invalidAdd(self):
        self.emp1.save()
        self.response = self.client.post('/createAccount/',
                                         {"f_name": self.emp1.EMP_FNAME, "initial": self.emp1.EMP_INITIAL,
                                          "l_name": self.emp1.EMP_LNAME, "role": self.emp1.EMP_ROLE,
                                          "email": self.emp1.EMP_EMAIL, "password": self.emp1.EMP_PASSWORD})
        self.assertEqual(self.response.context['message'], 'Email is already exists',
                         'Error: added an account already in the database')
        self.assertEqual(self.response.context["entries"], [('DR', 'A', 'Diego', 'Supervisor', 'doming46@uwm.edu'),
                                                            ('DR', '', 'Amanda', 'Instructor', '1234@gmail.com')],
                         "failed to display employees after unsuccessful add")