from django.shortcuts import render, redirect
from django.views import View
from .models import Employee


# Create your views here.
class Home(View):
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
        return render(request, "dashboard.html")
