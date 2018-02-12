from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import models
from WebConcursos import models

class UserRegisterFormCustom(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2', 'first_name','last_name',)
        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            if commit:
                user.save()
            return user
