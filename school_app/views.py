from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser
from .database_lookup import DbLookup



# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, "home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = MyUser.objects.get(email=request.POST['email'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "home.html", {"message": "Incorrect email/password"})
        else:
            request.session["email"] = m.email
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        #m = request.session["email"]
        return render(request, "dashboard.html")
