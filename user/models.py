from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

# 유저 정보 모델
class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    
class MYINFO(models.Model):
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    profile_image = models.ImageField
    hp = models.IntegerField(null=True, unique=True)
    hp_confirm = models.BooleanField(default=False)
    email_confirm = models.BooleanField(default=False)
    adult_confirm = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)

    class META:
        pass
