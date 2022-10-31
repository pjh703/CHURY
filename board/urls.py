from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'board'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('<int:pk>/', TemplateView.as_view(template_name='detail.html'), name="detail"),

]