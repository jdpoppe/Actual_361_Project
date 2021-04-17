from django.shortcuts import render, redirect
from django.views import View
from .models import Employee, Course, Section
# Create your views here.

class CreateCourse(View):
    def get(self, request):
        return render(request, "CreateCourse.html",{})
    def post(self, request):
        title = request.POST['title']
        credits = request.POST['credits']
        location = request.POST['location']
        instructor = request.POST['instructor']
        id = len(list(Course.objects.all()))
        entries = list(Course.objects.filter(title=title))
        if len(entries)>0:
            render(request,"CreateCourse.html",{"message":"course already exists"})
        Course.objects.create(title=title, credits=credits, location=location,
                              instructor=Employee.objects.get(name=instructor), ID=id)
        return redirect("/CreateCourse/")



class Assign(View):
    def get(self,request):
        return render(request, "AssignTA.html")
    def post(self,request):
        if request.POST['LabOrCourse']==0:
            #Update lab to hold instructor
            return redirect("AssignTA")
        else

