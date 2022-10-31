from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView, DetailView

from .forms import UserUpdateForm

from user.models import User
from django.urls import reverse_lazy

# Create your views here.


def LibraryView(request):
    return render(request, "mypage/library.html")


def EnvView(request):
    return render(request, "mypage/env.html")


def ProfileView(request):
    return render(request, "mypage/profile.html")


# 회원탈퇴
class UserDeleteView(DeleteView):
    model = User
    template_name = 'mypage/delete.html'
    success_url = reverse_lazy('user:login')
    context_object_name = 'user'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
        

# 회원정보
class UserDetailView(DetailView):
    template_name = 'member/detail.html'
    model = User


# 회원정보 수정
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name',]
    success_url = reverse_lazy('mypage:profile')
    template_name = 'mypage/update.html'


# 비밀번호 변경
class PwUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('user:login')
    template_name = 'mypage/pwupdate.html'

