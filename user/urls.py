from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from .views import UserCreateView

from . import views

app_name = "user"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html',next_page='/board/home/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    path('email/', UserCreateView.as_view(), name='email'),
    path('sign/', views.SignView, name='sign'),
    # path('modal/', views.ModalView, name='modal'),
    path('agreement/', views.AgreementView, name='agreement'),
]
