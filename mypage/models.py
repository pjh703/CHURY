from django.db import models
from user.models import User
# Create your models here.

class MYINFO(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE, db_column='email')
    profile_image = models.ImageField
    hp = models.IntegerField(null=True)
    hp_confirm = models.BooleanField(default=False)
    email_confirm = models.BooleanField(default=False)
    adult_confirm = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)


class MYBOOK(models.Model):
    like = models.TextField
    mydic = models.TextField
    read = models.TextField

