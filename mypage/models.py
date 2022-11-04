from django.db import models
# Create your models here.

class MYINFO(models.Model):
    email = models.ForeignKey("user.User", on_delete=models.CASCADE)
    profile_image = models.ImageField
    hp = models.IntegerField(null=True, unique=True)
    hp_confirm = models.BooleanField(default=False)
    email_confirm = models.BooleanField(default=False)
    adult_confirm = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)

    class META:
        pass


class MYBOOK(models.Model):
    email = models.ForeignKey("user.User", on_delete=models.CASCADE)
    mylike = models.CharField(null=True, max_length=15)
    mydic = models.CharField(null=True, max_length=15)
    myread = models.CharField(null=True, max_length=15)
    
    def __str__(self):
        return self.email
    def __str__(self):
        return self.mylike
    def __str__(self):
        return self.mydic
    def __str__(self):
        return self.myread
