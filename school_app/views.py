from django.shortcuts import render, redirect
from django.views import View
from .models import Employee, EmployeeType, Course, Section
from .Helpers import createSection, createCourse, assignInstructor, assignTA, assignEmployeeToSection, courseList, \
    makeInstructor, sectionsForCourse, taForCourse, courseAndSection


# Create your views here.

class CreateCourse(View):
    def get(self, request):

        return render(request, "createCourse.html", {"courses":courseList()})

    def post(self, request):
        message = createCourse(request.POST['courseTitle'], request.POST['instructorEmail'])
        print(message)
        return render(request, "createCourse.html", {"message": message,"courses":courseList()})


class CreateSection(View):
    def get(self, request):
        return render(request, "createSection.html", {"courseAndSection":courseAndSection(courseList())})

    def post(self, request):
        message = createSection(request.POST['secTitle'], request.POST['taEmail'], request.POST['course'])
        return render(request, "createSection.html",
                      {"message": createSection(request.POST['secTitle'], request.POST['taEmail'],
                                                request.POST['course']),
                       "courseAndSection":courseAndSection(courseList())})


class AssignInstructor(View):
    def get(self, request):
        c = list(Course.objects.all())
        courses = list()
        for i in c:
            courses.append((i.title, i.instructor))
        return render(request, "assignInstructor.html", {"courses": courses})

    def post(self, request):
        return render(request, "assignInstructor.html",
                      {"message": assignInstructor(request.POST['email'], request.POST['course'])})


class InstructorAssignTA(View):
    def get(self, request):
        instructor = Employee.objects.get(EMP_EMAIL=request.session["email"])
        c = list(Course.objects.filter(instructor=instructor))
        courses = list()
        for i in c:
            courses.append((i.title))
        return render(request, "instructorAssignTA.html", {"courses": courses})

    def post(self, request):
        instructor = Employee.objects.get(EMP_EMAIL=request.session["email"])
        c = list(Course.objects.filter(instructor=instructor))
        courses = list()
        for i in c:
            courses.append((i.title))
        return render(request, "instructorAssignTA.html",
                      {"message": assignTA(request.POST['email'], request.POST['course'], request.POST['section'],
                                           request.session["email"]), "courses": courses})


class AssignEmployee(View):
    def get(self, request):
        return render(request, "assignTA.html", {"courses": courseList()})

    def post(self, request):
        return render(request, "assignTA.html", {"message": assignEmployeeToSection(request.POST["email"],
                                                                             request.POST["section"],
                                                                             request.POST["course"]),
                                                 "courses": courseList()})


class ViewAllCourses(View):
    def get(self, request):
        return render(request, "ViewAllCourses.html", {"courses":courseList(),"currentCourse":"Select a Course"})

    def post(self, request):
        course = request.POST["currentCourse"]
        instructor = ""
        allTA = []
        allSections = []
        try:
            instructor = makeInstructor(course)
            allTA = taForCourse(course)
            allSections = sectionsForCourse(course)
        except:
            course = "Please Enter Valid Course"

        return render(request, "ViewAllCourses.html", {"courses": courseList(),
                                                       "currentCourse": course,
                                                       "instructor": instructor,"allTA": allTA,
                                                       "allSections": allSections})


class Dashboard(View):
    def get(self, request):
        return render(request, "dashboard.html", {"user": request.session["type"]})

    def post(self, request):
        return render(request, "dashboard.html", {"user": request.session["type"]})


class Login(View):
    def get(self, request):
        request.session["type"] = "Hacker"
        request.session.save()
        return render(request, "login.html", {})

    def post(self, request):
        request.session["type"] = "Hacker"
        noSuchUser = False
        badPassword = False
        try:
            m = Employee.objects.get(EMP_EMAIL=request.POST['j_username'])
            badPassword = (m.EMP_PASSWORD != request.POST['j_password'])
        except:
            noSuchUser = True
        if noSuchUser or badPassword:
            return render(request, "login.html", {"message": "Incorrect email/password"})
        else:
            request.session["email"] = m.EMP_EMAIL
            request.session["type"] = m.EMP_ROLE
            return redirect("/dashboard/")


class Account(View):
    def get(self, request):
        return render(request, "account.html", {})

    def post(self, request):
        return render(request, "account.html", {})


class AssignCourse(View):
    def get(self, request):
        return render(request, "assignCourse.html", {})

    def post(self, request):
        return render(request, "assignCourse.html", {})


class Notifications(View):
    def get(self, request):
        return render(request, "notifications.html", {})

    def post(self, request):
        return render(request, "notifications.html", {})


class ClassView(View):
    def get(self, request):
        return render(request, "classTemplate.html", {})

    def post(self, request):
        return render(request, "classTemplate.html", {})


class CreateAccount(View):
    def get(self, request):
        m = request.session["email"]
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))  # i.0, i.1, i.2, i.3, i.4
        return render(request, "createAccount.html", {"entries": formattedEntries, "roles": EmployeeType.choices})

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
        return render(request, "createAccount.html", {"entries": formattedEntries, "message": message,
                                                      "roles": EmployeeType.choices})
