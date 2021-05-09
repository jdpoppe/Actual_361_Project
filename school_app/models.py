from django.db import models


class EmployeeType(models.TextChoices):
    SUPE = "Supervisor"
    INS = "Instructor"
    TA = "TA"


class Employee(models.Model):
    EMP_ROLE = models.CharField(max_length=12, choices=EmployeeType.choices, default=EmployeeType.TA)
    EMP_LNAME = models.CharField(max_length=25, blank=False)
    EMP_FNAME = models.CharField(max_length=25, blank=False)
    EMP_INITIAL = models.CharField(max_length=1)
    EMP_EMAIL = models.EmailField(max_length=254, blank=False)
    EMP_PASSWORD = models.CharField(max_length=20, blank=False)


class Course(models.Model):
    title = models.CharField(max_length=20)
    instructor = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)

class Section(models.Model):
    title = models.CharField(max_length=20)
    emp = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)







