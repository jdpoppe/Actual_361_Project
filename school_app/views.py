from django.shortcuts import render, redirect
from django.views import View
from .models import Employee, Course, Section


# Create your views here.

class CreateCourse(View):
    def get(self, request):
        return render(request, "CreateCourse.html", {})

    def post(self, request):
        title = request.POST['title']
        credits = request.POST['credits']
        location = request.POST['location']
        instructor = request.POST['instructor']
        id = len(list(Course.objects.all()))
        entries = list(Course.objects.filter(title=title))
        if len(entries) > 0:
            render(request, "CreateCourse.html", {"message": "course already exists"})
        Course.objects.create(title=title, credits=credits, location=location,
                              instructor=Employee.objects.get(name=instructor), ID=id)
        return redirect("/CreateCourse/")


class Assign(View):
    def get(self, request):
        return render(request, "AssignTA.html")

    def post(self, request):
        if request.POST['LabOrCourse'] == 0:
            # Update lab to hold instructor
            return redirect("AssignTA")


class Login(View):
    def get(self, request):
        return render(request, "home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = Employee.objects.get(EMP_EMAIL=request.POST['email'])
            badPassword = (m.EMP_PASSWORD != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser or badPassword:
            return render(request, "home.html", {"message": "Incorrect email/password"})
        else:
            request.session["email"] = m.EMP_EMAIL
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        m = request.session["email"]
        return render(request, "dashboard.html", {"email": m})


class CreateAccount(View):
    def get(self, request):
        m = request.session["email"]
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))  # i.0, i.1, i.2, i.3, i.4
        return render(request, "createAccount.html", {"entries": formattedEntries})

    def post(self, request):
        m = request.session["email"]
        canAdd = False
        message = ""
        try:
            m = Employee.objects.get(EMP_EMAIL=request.POST['email'])
        except:
            canAdd = True
        if canAdd:
            Employee.objects.create(EMP_ROLE=request.POST['role'], EMP_LNAME=request.POST['l_name'],
                                    EMP_FNAME=request.POST['f_name'], EMP_INITIAL=request.POST['initial'],
                                    EMP_EMAIL=request.POST['email'], EMP_PASSWORD=request.POST['password'])
            message = "Account created"
        else:
            message = "Email is already exists"
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))  # i.0, i.1, i.2, i.3, i.4
        return render(request, "createAccount.html", {"entries": formattedEntries, "message": message})
