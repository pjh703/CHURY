from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import UserForm

# Create your views here.

# 로그인
def login(request):
    return render(request, 'user/login.html')


# 회원가입
class UserCreateView(CreateView):
    model = User

    template_name = 'user/email.html'
    form_class = UserForm

    success_url = reverse_lazy('user:login')

def SignView(request):
    return render(request, 'user/sign.html')

def ModalView(request):
    return render(request, 'user/modal.html')

def AgreementView(request):
    return render(request, 'user/agreement.html')
