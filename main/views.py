from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Card, SubCard
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, AddCardForm, EditSubCardForm
from django.contrib.auth.decorators import login_required
import datetime


# ############### Helper functions ############# #

def create_subtask(subtaskname,subtaskstate, id):
    #fetch the card instance
    card = Card.objects.filter(taskid=id)
    card = card[0]
    #create subtask using card
    newsubtask = SubCard(subtask_name=subtaskname, subtask_state=subtaskstate, task_name=card)
    #commit changes
    newsubtask.save()
    return True

def delete_subtask(id, nameofsubtask):
    #fetch card instance
    card = Card.objects.filter(taskid=id)
    card = card[0]
    #Delete subcard
    subtask = SubCard.objects.filter(task_name=card,subtask_name=nameofsubtask)
    print("Deleting subcard with name: ",nameofsubtask)
    subtask.delete()
    return True

def update_subtask(id, nameofsubtask, subtaskstate):
    
    subtask = SubCard.objects.filter(task_name=id,subtask_name=nameofsubtask)
    subtask = subtask[0]
    print("Updating subtask: ",subtask.subtask_name," with new state of: ",subtaskstate)
    subtask.subtask_state = subtaskstate
    subtask.save()

    return True


def updateprogress(uuid):

    completed = 0
    subtasklist = SubCard.objects.values_list('subtask_state', flat=True).filter(task_name=uuid)
    total = len(subtasklist)
    card = Card.objects.get(taskid = uuid)
    print(card.task_progress)
    if(total != 0):
        for i in subtasklist:
            if(i == True):
                completed=completed+1
        progress = (completed/total)*100
        print(progress,"%")
        card.task_progress = progress
        card.save()
    else:
        card.task_progress = 0
        card.save()

# ################ VIEWS ############### #

# Create your views here.
def password_change_done(request):
    return render(request, "main/password_change_done.html")
    
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
   cardids = Card.objects.values_list('taskid',flat=True).filter(task_owner=request.user.id)
   subtasklist = SubCard.objects.all()
   subtasks = []
   for subs in subtasklist:
       if subs.task_name.taskid in cardids:
           subtasks.append(subs)
      
   form = AddCardForm()
   if request.method == 'POST':
    #    print(request.POST)
       form = AddCardForm(request.POST)
       if form.is_valid():
            formtocommit = form.save(commit=False)
            formtocommit.task_owner = request.user
            #Fills deadline as using date and time | Used to display remaining time 
            formtocommit.task_deadline = datetime.datetime.combine(formtocommit.task_deadline_date,formtocommit.task_deadline_time)
            formtocommit.save()
            print("Saved entry")
            return redirect("/core")
   return render(request, 'main/core.html',{'cards':cards, 'form':form, 'subtasks':subtasks})

def editcardsubmission(request):
    if 'editcardsubmission' in request.POST:
        ## 1.) Delete subtasks marked for deletion before updation:
        subtaskdeletelist = request.POST.getlist('subtaskdeletes')
        print(len(subtaskdeletelist))
        print("Subtasks marked for deletion: ", subtaskdeletelist)
        if(len(subtaskdeletelist)>0):
            for i in subtaskdeletelist:
                delete_subtask(request.POST.get('carduuid'),i)

        ## 2.) Update subtasks state:
        # Get list of all subtasks of the card
        subtasklist = SubCard.objects.values_list('subtask_name', flat=True).filter(task_name=request.POST.get('carduuid'))
        #Check Add Subtask fields
        Add_subtask = request.POST.get('newsubtaskname')
        newsubtask_state = request.POST.get('newsubtask_state',False)
        print("New subtask: [",Add_subtask,"] was returned with value ",newsubtask_state)
        # Get updated list of all subtasks marked completed
        subtasktruelist = request.POST.getlist('subtaskvalue')
        print("Updated list of subtasks state: ", subtasktruelist)

        ## Commits
        # Subtasks update
        for i in subtasklist:
            if(i in subtasktruelist):
                print(i," Completed")
                update_subtask(request.POST.get('carduuid'),i,True)
            else:
                print(i, " Pending")
                update_subtask(request.POST.get('carduuid'),i,False)
        #Add new subtask
        if(Add_subtask != ""):
            create_subtask(Add_subtask,newsubtask_state,request.POST.get('carduuid'))

        #Update progress and return
        updateprogress(request.POST.get('carduuid'))
        return redirect('/core')
    
    return redirect('/core')


def deletecardsubmission(request):
    if 'deletecardsubmission' in request.POST:
        carduuid=request.POST.get('carduuid')
        print("found and deleting:"+carduuid)
        Card.objects.filter(taskid=carduuid).delete()
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


def donation(request):
    return render(request = request,
                  template_name='main/donation.html')

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

