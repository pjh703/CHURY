from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


# 유저 회원가입 폼
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "email",
        )

