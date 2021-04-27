from django.contrib import admin
from .models import Employee, Course, Section

# Register your models here.
admin.site.register(Employee)
admin.site.register(Course)
admin.site.register(Section)