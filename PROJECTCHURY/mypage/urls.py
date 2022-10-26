from django.urls import path

from . import views
from django.views.generic import TemplateView


app_name = 'mypage'
urlpatterns = [
    path('library/', views.LibraryView, name='library'),
    path('env/', views.EnvView, name='env'),

]