from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import UserForm
from . import models
from user.models import User

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



# 비밀번호 찾기 창
def FindView(request):
    return render(request, 'user/pwfind.html')


from django.core.mail.message import EmailMessage
 
def send_email(request):

    
    if request.method == "POST":
        username = request.POST['username']  # html에서 input칸 id=username
        email = request.POST['email']  # html에서 input칸 id=email
        
        User.objects.filter(username = username)[0]  # User 모델과 input username 비교해서 같으면 출력
        email_check = User.objects.filter(username = username)[0].email  # User 모델과 input username 비교해서 같으면 해당 유저에서 이메일 출력
        email_model = User.objects.filter(email = email)[0].email

        # print(email_check, email_model)

        if email_check == email_model:
            
            subject = "CHURY 비밀번호 안내 이메일 입니다."
            to = ["hongsb5837@naver.com"]
            from_email = "project.chury@gmail.com"
            message = f"비밀번호 변경 테스트:{User.objects.filter(username = username)[0].password}"
            EmailMessage(subject=subject, body=message, to=to,
            from_email=from_email).send()
        else:
            print("????????????????????????????????")
        # email_id = User.objects.get(email = username)
        # mydic = MYBOOK.objects.filter(email_id = email_id).values('mydic').filter(mydic = pk)


    else:
        print('-'*30)
        print("?")
        pass


    return render(request, 'user/login.html')


