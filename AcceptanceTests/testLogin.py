from django.test import TestCase, Client
from school_app.models import Employee

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Employee.objects.create(EMP_ROLE="Supervisor", EMP_LNAME="Diego", EMP_FNAME="DR", EMP_INITIAL="A",
                                            EMP_EMAIL="doming46@uwm.edu", EMP_PASSWORD="1234")

    def test_validLogin(self):
        response = self.client.post('/', {'j_username': self.user1.EMP_EMAIL, 'j_password': self.user1.EMP_PASSWORD})
        self.assertEqual(response.url, '/dashboard/', 'Incorrect redirect after the existing user logged in')
        response = self.client.get('/dashboard/')

    def test_invalidLogin(self):
        response = self.client.post('/', {'j_username': self.user1.EMP_EMAIL, 'j_password': "777"}, follow=True)
        self.assertEqual(response.context['message'], 'Incorrect email/password', 'Failed to display the error for incorrect password')

    def test_invalidEmail(self):
        response = self.client.post('/', {'j_username': "123@uwm.edu", 'j_password': "777"}, follow=True)
        self.assertEqual(response.context['message'], 'Incorrect email/password', 'Failed to display the error for incorrect password')