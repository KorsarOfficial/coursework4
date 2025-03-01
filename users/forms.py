from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User


class UsersRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class BlockingUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ["is_active"]
