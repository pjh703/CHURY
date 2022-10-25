from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'user'
urlpatterns = [
    # path('login/', views.login, name='login'),
    path('sign/', views.UserCreateView.as_view(), name='sign'),

    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html',
        next_page='/'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        # template_name='user/user_form.html',
        next_page='/'
    ), name='logout'),

]
