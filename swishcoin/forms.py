from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "w-full p-2 border border-gray-300 rounded-md"})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "w-full p-2 border border-gray-300 rounded-md"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full p-2 border border-gray-300 rounded-md"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full p-2 border border-gray-300 rounded-md"})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "placeholder": "Enter your username"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "placeholder": "Enter your password"
        })
    )
