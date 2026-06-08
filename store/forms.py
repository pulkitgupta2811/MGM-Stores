from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Mobile", widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['name', 'mobile', 'email', 'password1', 'password2']
