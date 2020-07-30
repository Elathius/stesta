"""lightscale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("core", views.core, name="core"),
    path("getstarted", views.getstarted, name="getstarted"),
    path("editcardsubmission", views.editcardsubmission, name="editcardsubmission"),
    path("deletecardsubmission", views.deletecardsubmission, name="cdeletecardsubmission"),
<<<<<<< HEAD
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='main/change-password.html',success_url="../password_change_done"),
        name="password_change"
    ),
    path(
        'password_change_done/',
        auth_views.PasswordChangeView.as_view(template_name='main/password_change_done.html'),
        name="password_change_done"
    ),

=======
    path("donation", views.donation, name="donation"),
    
>>>>>>> ad56d64f900e7f086fb31ed68783ce3646f9d3fe
]
