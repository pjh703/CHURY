from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

# 유저 정보 모델
class User(AbstractUser):
    email = models.EmailField(unique=True)  # 유니크 추가로 migrate 필요?
    

    
