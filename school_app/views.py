from django.shortcuts import render, redirect
from django.views import View
from .models import Employee
from .Helpers import createCourse, createSection, assignTA, assignInstructor
# Create your views here.

class CreateCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {})

    def post(self, request):
        message = createCourse(request.POST['courseTitle'], request.POST['instructorEmail'])
        print(message)
        return render(request, "createCourse.html", {"message": message})


class CreateSection(View):
    def get(self,request):
        return render(request, "createSection.html", {})

    def post(self, request):
        message = createSection(request.POST['secTitle'], request.POST['taEmail'], request.POST['course'])
        return render(request, "createSection.html", {"message": message})


class AssignInstructor(View):
    def get(self, request):
        return render(request, "assignInstructor.html", {})

    def post(self, request):
        return render(request, "assignInstructor.html",
                      {"message":assignInstructor(request.POST['email'], request.POST['course'])})

class AssignTA(View):
    def get(self, request):
        return render(request, "assignTA.html",{})
    def post(self, request):
        return render(request, "assignTA.html",
                      {"message":assignTA(request.POST['email'], request.POST['course'], request.POST['section'])})


class Login(View):
    def get(self, request):
        return render(request, "home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = Employee.objects.get(Email_Field =request.POST['email'])
            badPassword = (m.EMP_PASSWORD != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser or badPassword:
            return render(request, "home.html", {"message": "Incorrect email/password"})
        else:
            request.session["email"] = m.Email_Field
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        m = request.session["email"]
        return render(request, "dashboard.html", {"email": m})

