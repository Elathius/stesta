from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Card

class DateInput(forms.DateInput):
    input_type = 'date'

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class AddCardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['task_name', 'task_deadline_date', 'task_deadline_time']
        #widgets = { 'task_deadline_date' : DateInput()}

