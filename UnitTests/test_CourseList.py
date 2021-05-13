from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
import django
django.setup()
from school_app.models import Employee, Course, Section
from school_app.Helpers import courseList


class TestCourseList(TestCase):
    def test_noCourses(self):
        self.assertEqual(courseList(), [],
                         msg="Making list of courses when the DB is empty fails to return an empty list")

    def test_someCourses(self):
        class5 = Course(title="Class 5")
        class5.save()
        class6 = Course(title="Class 6")
        class6.save()
        self.assertEqual(courseList(), [class5.title, class6.title], msg="Making a list of courses when the DB has some entries "
                                                             "return a list of every element")

    def test_sameName(self):
        class5 = Course(title="Class 5")
        class5.save()
        class6 = Course(title="Class 6")
        class6.save()
        class7_1 = Course(title="Class 7")
        class7_1.save()
        class7_2 = Course(title="Class 7")
        class7_2.save()
        class7_3 = Course(title="Class 7")
        class7_3.save()
        class7_4 = Course(title="Class 7")
        class7_4.save()
        self.assertEqual(courseList(),
                         [class5.title, class6.title, class7_1.title, class7_1.title, class7_1.title, class7_1.title],
                         msg="Making a list courses when some names have repeats fails to return correct list")
