from django.urls import path
from django.views.generic import DetailView

from . import views


app_name = 'board'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:pk>/', DetailView.as_view(), name="detail"),

]