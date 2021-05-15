from django.shortcuts import render, redirect
from django.views import View
from .models import Employee, EmployeeType
from .Helpers import createSection, createCourse, assignInstructor, assignTA
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
        return render(request, "notifications.html", {})

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
class EditAccount(View):
    def get(self, request):
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))
        return render(request, "editAccount.html", {"entries": formattedEntries, "roles": EmployeeType.choices})
    def post(self, request):
        valid = True
        valid2 = False
        message = ""
        try:
            m = Employee.objects.get(EMP_EMAIL=request.POST['accToEdit'])
        except:
            valid = False
        if valid:
            m.EMP_FNAME = request.POST['f_name']
            m.EMP_INITIAL = request.POST['initial']
            m.EMP_LNAME = request.POST['l_name']
            m.EMP_ROLE = request.POST['role']
            try:
                Employee.objects.get(EMP_EMAIL=request.POST['email'])
            except:
                valid2 = True
            if valid2:
                m.EMP_EMAIL = request.POST['email']
            else:
                return render(request, "editAccount.html", {"message": "Email Already Exists"})
            m.EMP_PASSWORD = request.POST['password']
            m.save()
            message = "account has been edited"
        else:
            message = "account does not exist"
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))
        return render(request, "editAccount.html", {"entries": formattedEntries, "message": message,
                                                    "roles": EmployeeType.choices})

class EditSelf(View):
    def get(self, request):
        return render(request, "editSelf.html")
    def post(self, request):
        valid = False
        message = ""
        m = Employee.objects.get(EMP_EMAIL=request.session['email'])
        m.EMP_FNAME = request.POST['f_name']
        m.EMP_INITIAL = request.POST['initial']
        m.EMP_LNAME = request.POST['l_name']
        try:
            Employee.objects.get(EMP_EMAIL=request.POST['email'])
        except:
            valid = True
        if valid:
            m.EMP_EMAIL = request.POST['email']
        else:
            return render(request, "editSelf.html", {"message": "Email Already Exists"})
        m.EMP_PASSWORD = request.POST['password']
        m.save()
        request.session['email'] = m.EMP_EMAIL
        return render(request, "editSelf.html", {'message': "account successfully updated"})

class DeleteAccount(View):
    def get(self, request):
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))
        return render(request, "deleteAccount.html", {"entries": formattedEntries})
    def post(self, request):
        valid = True
        message = ""
        try:
            m = Employee.objects.get(EMP_EMAIL=request.POST['accToDel'])
        except:
            valid = False
        if valid and request.POST['accToDel'] != request.session['email']:
            m.delete()
            message = "account has been deleted"
        else:
            message = "cannot delete your own or nonexistent accounts"
        allEmployee = list(Employee.objects.all())
        formattedEntries = []
        for i in allEmployee:
            formattedEntries.append(
                (i.EMP_FNAME, i.EMP_INITIAL, i.EMP_LNAME, i.EMP_ROLE, i.EMP_EMAIL))
        return render(request, "deleteAccount.html", {"entries": formattedEntries, "message": message})