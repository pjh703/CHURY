from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import UserDeleteView, UserUpdateView, UserDetailView, PwUpdateView


app_name = 'mypage'

urlpatterns = [
    path('library/', views.LibraryView, name='library'),
    path('env/', views.EnvView, name='env'),
    path('profile/', views.ProfileView , name='profile'),

    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('pwupdate/<int:pk>/', PwUpdateView.as_view(), name='pwupdate'),
    # path('update/<int:pk>/', UserDetailView.as_view(), name='update'),

    # 데이터 처리
    path('mydic/', views.mydic, name='mydic')
]
