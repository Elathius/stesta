from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Card
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, AddCardForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='main/landing.html',
                  context = {"Cards":Card.objects.all})

def getstarted(request):
    if request.user.is_authenticated:
        return redirect('/core')
    return redirect('/login')

@login_required(login_url="/login/")
def core(request):
   cards = Card.objects.filter(task_owner=request.user.id)
   form = AddCardForm()
   if request.method == 'POST':
       print(request.POST)
       form = AddCardForm(request.POST)
       if form.is_valid():
            formtocommit = form.save(commit=False)
            formtocommit.task_owner = request.user
            formtocommit.save()
            print("Saved entry")
            return redirect("/core")
   return render(request, 'main/core.html',{'cards':cards, 'form':form})

def editcardsubmission(request):
    return redirect('/core')


def deletecardsubmission(request):
    return redirect('/core')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:login")

        else:
            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("/login")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:core')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/index.html",
                    context={"form":form})


def error404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    print("sent 404")
    return response

def error500(request, template_name='500.html'):
    response = render(request, template_name)
    response.status_code = 500
    print("sent 500")
    return response

def error400(request, exception, template_name='400.html'):
    response = render(request, template_name)
    response.status_code = 400
    print("sent 400")
    return response

def error403(request, exception, template_name='403.html'):
    response = render(request, template_name)
    response.status_code = 403
    print("sent 403")
    return response

