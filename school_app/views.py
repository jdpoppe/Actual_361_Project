from django.shortcuts import render, redirect
from django.views import View
from flask import app, Flask

from .models import Employee, EmployeeType, Course, Section
from .Helpers import createSection, createCourse, assignInstructor, assignTA
import smtplib
# Create your views here.

class CreateCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {})

    def post(self, request):
        print("IM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\nIM HERE\n")
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
        c=list(Course.objects.all())
        courses = list()
        for i in c:
            courses.append((i.title, i.instructor))
        return render(request, "assignInstructor.html", {"courses": courses})

    def post(self, request):
        return render(request, "assignInstructor.html",
                      {"message":assignInstructor(request.POST['email'], request.POST['course'])})

class AssignTA(View):
    def get(self, request):
        c=list(Course.objects.all())
        courses = list()
        for i in c:
            courses.append(i.title)

        #Look for sections in other table
        s = list(Section.objects.all())
        sections = list()
        for j in s:
            sections.append((j.title, j.ta, j.course, j.courseTitle))

        return render(request, "assignTA.html",{"courses": courses,"sections":sections})
    def post(self, request):
        return render(request, "assignTA.html",
                      {"message":assignTA(request.POST['email'], request.POST['course'], request.POST['section'])})

class Dashboard(View):
    def get(self, request):
        return render(request, "dashboard.html",{})
    def post(self, request):
        return render(request, "dashboard.html",{})

class Login(View):
    def get(self, request):
        return render(request, "login.html",{})

    def post(self, request):
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
            return redirect("/dashboard/")

class Account(View):
    def get(self, request):
        return render(request, "account.html", {})

    def post(self, request):
        return render(request, "account.html", {})

class AssignCourse(View):
    def get(self, request):
        return render(request, "assignCourse.html",{})
    def post(self, request):
        return render(request, "assignCourse.html",{})

class Notifications(View):
    def get(self, request):
        return render(request, "notifications.html", {})
    def post(self, request):
        from flask_mail import Mail, Message



        def index(mail):
            msg = Message('Hello', sender='smtpTestcs361@gmail.com', recipients=['halver78@uwm.edu'])
            msg.body = "Hello Flask message sent from Flask-Mail"
            mail.send(msg)
            return "Sent"


        def create_app():
            app = Flask(__name__)
            #@app.route("/")
            with app.app_context():
                app.config['MAIL_SERVER'] = 'smtp.gmail.com'
                app.config['MAIL_PORT'] = 465
                app.config['MAIL_USERNAME'] = 'smtpTestcs361@gmail.com'
                app.config['MAIL_PASSWORD'] = 'gyuJ5b!#^T^Pj*Uod0'
                app.config['MAIL_USE_TLS'] = False
                app.config['MAIL_USE_SSL'] = True
                mail = Mail(app)
                index(mail)
            return app

        app = create_app()




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