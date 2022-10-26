from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'board'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:pk>/', views.BoardDetailView, name="detail"),

]