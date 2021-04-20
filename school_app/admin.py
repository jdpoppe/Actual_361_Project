from django.contrib import admin
from .models import MyUser, employee

# Register your models here.
admin.site.register(MyUser)
admin.site.register(employee)