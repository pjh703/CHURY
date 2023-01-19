from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from .views import UserCreateView

from . import views

# 비밀번호 변경
from django.contrib.auth import views as auth_views
 
app_name = "user"

urlpatterns = [ 
    path('login/', LoginView.as_view(template_name='user/login.html',next_page='/board/home/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    

    # 비밀번호 찾기 창
    path('pwfind/', views.FindView, name='pwfind'),


    path('email/', UserCreateView.as_view(), name='email'),
    path('sign/', views.SignView, name='sign'),
    path('modal/', views.ModalView, name='modal'),
    path('agreement/', views.AgreementView, name='agreement'),

    # 이메일 전송
    path('send_email/', views.send_email, name='send_email'), 
    
    # 비밀번호 변경
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # path('registration/', include('registration.urls')),

]
