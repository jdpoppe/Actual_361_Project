from django.db import models


class MyUser(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class Role(models.TextChoices):
    TA = "TA"
    INS = "Instructor"


class employee(models.Model):
    EMP_ROLE = models.CharField(max_length=12, choices=Role.choices, default=Role.TA)
    EMP_LNAME = models.CharField(max_length=25)
    EMP_FNAME = models.CharField(max_length=25)
    EMP_INITIAL = models.CharField(max_length=1)
    EMP_EMAIL = models.EmailField(max_length=254)
    EMP_DEPARTMENT = models.CharField(max_length=30)


