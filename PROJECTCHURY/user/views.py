from django.contrib.auth import models, forms
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.utils import timezone


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
    success_url = reverse_lazy('user:chu')  # POST 요청을 처리할 때 리다이렉트할 URL


class UserChuView(generic.ListView):
    template_name = 'user/chu.html'
    model = models.UserChu
    paginate_by = 10
    pasinate_orphans = 5


class UserDeleteView(generic.DeleteView):
    model = models.CustomUser
    success_url = reverse_lazy('/')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def useredit(request):
    if request.method == "POST":
        form = forms.CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('board:home')
    else:
        form = forms.UserChangeForm(instance=request.user)
    context = {
        'form' : form,
    }

    return render(request, 'user/edit.html', context)
