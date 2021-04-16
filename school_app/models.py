from django.db import models


# Create your models here.
class MyUser(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email