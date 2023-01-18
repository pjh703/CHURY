from django.urls import path
from django.views.generic import DetailView

from . import views


app_name = 'board'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('detail/<pk>/', views.BoardDetailView, name="detail"),
    path('search/', views.search, name='search'),
    path('loading/', views.loading, name='loading'),
]