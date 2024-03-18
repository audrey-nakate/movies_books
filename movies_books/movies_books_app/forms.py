from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

        username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Input your username',
    })) 

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder' : 'Input your email address',
    })) 

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Input your password',
    }))   

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Repeat your password',
    }))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Input your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Input your password',
    }))