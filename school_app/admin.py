from django.contrib import admin
from .models import Employee, Course, Section

admin.site.register(Employee)
admin.site.register(Course)
admin.site.register(Section)