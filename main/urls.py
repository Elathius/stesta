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
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='main/password/change-password.html',success_url="../../password_change_done"),
        name="password_change"
    ),
    path(
        'password_change_done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='main/password/password_change_done.html'),
        name="password_change_done"
    ),

    path("donation", views.donation, name="donation"),

    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="main/password/password_reset.html", success_url="../../reset_password_sent"), name="reset_password"),

    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="main/password/password_reset_done.html"), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html", success_url="../../../../reset_password_complete"), name="password_reset_confirm"),

    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="main/password/password_reset_complete.html"), name="password_reset_complete"),
    
]
