from django.contrib.auth import models, forms
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .forms import CustomUserCreationForm

from . import models


# Create your views here.
def login(request):
    return render(request, 'user/login.html')

class UserCreateView(generic.CreateView):
    """
    내장 뷰 클래스인 CreateView를 상속하여 구현한 사용자 정의 CreateView
    GET 요청 시 회원가입 페이지로 이동하고, 
    POST 요청 시 내장 모델 클래스인 User를 사용하여 회원가입 처리를 한다 
    """
    form_class = CustomUserCreationForm
    
    template_name = 'user/sign.html'  # GET 요청을 처리할 때 응답할 템플릿 파일
    success_url = reverse_lazy('home')  # POST 요청을 처리할 때 리다이렉트할 URL
