from msilib.schema import ListView
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'user'
urlpatterns = [
    # path('login/', views.login, name='login'),
    path('sign/', views.UserCreateView.as_view(), name='sign'),

    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html',
        next_page='/board/home/'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        # template_name='user/user_form.html',
        next_page='/'
    ), name='logout'),

    path('chu/', views.UserChuView.as_view(), name='chu'),

    path('edit/', views.useredit, name='edit'),
]
