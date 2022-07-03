from tkinter import Widget
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password =forms.CharField(max_length=20, widget=forms.PasswordInput)
    captcha=CaptchaField()

    class Meta():
        fields=['username','password','captcha']
