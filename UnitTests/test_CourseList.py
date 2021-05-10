import unittest

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()

from school_app.models import Employee, Course, Section
from school_app.Helpers import courseList
# Because of database, test only work when ran individually
class TestCourseList(unittest.TestCase):
    def setUp(self):
        pass

    def test_noCourses(self):
        self.assertEqual(courseList(), [],
                         msg="Making list of courses when the DB is empty fails to return an empty list")

    def test_someCourses(self):
        class5 = Course.objects.create(title="Class 5").title
        class6 = Course.objects.create(title="Class 6").title
        self.assertEqual(courseList(), [class5, class6], msg="Making a list of courses when the DB has some entries "
                                                             "return a list of every element")

    def test_sameName(self):
        class7 = Course.objects.create(title="Class 7").title
        Course.objects.create(title="Class 7")
        Course.objects.create(title="Class 7")
        Course.objects.create(title="Class 7")
        class6 = Course.objects.get(title="Class 6").title
        class5 = Course.objects.get(title="Class 5").title
        self.assertEqual(courseList(), [class5, class6, class7, class7, class7, class7], msg="Making a list courses when some names"
                                                                             "have repeats fails to return correct "
                                                                             "list")
