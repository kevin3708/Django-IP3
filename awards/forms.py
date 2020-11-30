from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    job_title = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('job_title','username', 'first_name', 'last_name', 'email', 'password1', 'password2') 
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'profile', 'like', 'screenshots']

class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = Screenshot
        fields = '__all__'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['project','profile']
        
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['project','profile','like']
