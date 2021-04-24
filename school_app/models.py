from django.db import models


class EmployeeType(models.TextChoices):
    SUPE = "Supervisor"
    INS = "Instructor"
    TA = "TA"


class Employee(models.Model):
    EMP_ROLE = models.CharField(max_length=12, choices=EmployeeType.choices, default=EmployeeType.TA)
    EMP_LNAME = models.CharField(max_length=25)
    EMP_FNAME = models.CharField(max_length=25)
    EMP_INITIAL = models.CharField(max_length=1)
    EMP_EMAIL = models.EmailField(max_length=254)
    EMP_PASSWORD = models.CharField(max_length=20)

