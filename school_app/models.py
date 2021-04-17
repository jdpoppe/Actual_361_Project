from django.db import models


class EmployeeType(models.TextChoices):
    Supervisor = 0
    Instructor = 1
    TA = 2


class Employee(models.Model):
    ID = models.IntegerField(max_length=6, unique=True)
    fName = models.CharField(max_length=25)
    lName = models.CharField(max_length=25)
    middleInitial = models.CharField(max_length=1)
    email = models.charField(max_length=30)
    department = models.charField(max_length=30)
    type = models.IntegerField(max_length=1, choices=EmployeeType.choices)


class Course(models.Model):
    ID = models.IntegerField(max_length=6, unique=True)
    title = models.CharField(max_length=20)
    credits = models.IntegerField(max_length=1)
    location = models.CharField(max_length=10)
    instructor = models.ForeignKey(Employee, on_delete=models.SET_Null, blank=True, null=True)


class Section(models.Model):
    ID = models.IntegerField(max_length=6, unique=True)
    time = models.CharField()
    location = models.CharField(max_length=10)
    ta = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


