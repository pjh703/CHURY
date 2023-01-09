from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'account'

urlpatterns = [

    path('password_reset/', views.password_reset_request, name="password_reset"),
]