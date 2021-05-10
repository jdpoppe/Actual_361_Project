"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from school_app.views import Login, Dashboard, CreateCourse, CreateSection, AssignInstructor, AssignTA, Notifications, \
    Account, CreateAccount, ClassView, PublicContactInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('dashboard/', Dashboard.as_view()),
    path('account/', Account.as_view()),
    path('notifications/', Notifications.as_view()),
    path('createCourse/', CreateCourse.as_view()),
    path('createSection/', CreateSection.as_view()),
    path('assignInstructor/', AssignInstructor.as_view()),
    path('assignTA/', AssignTA.as_view()),
    path('createAccount/', CreateAccount.as_view()),
    path('class1/', ClassView.as_view()),
    #new
    path('publicContactInfo/', PublicContactInfo.as_view())
]
