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
    mydic = models.BigIntegerField(null=True)
    myread = models.CharField(null=True, max_length=15)
    
    # def __str__(self):
    #     return self.email
    # def __str__(self):
    #     return self.mylike
    # def __str__(self):
    #     return self.mydic
    # def __str__(self):
    #     return self.myread


class MYCHOOSE(models.Model):
    email = models.ForeignKey("user.User", on_delete=models.CASCADE)
    Action = models.IntegerField(null=True, default=0)
    Adventure = models.IntegerField(null=True, default=0)
    Animation = models.IntegerField(null=True, default=0)
    Comedy = models.IntegerField(null=True, default=0)
    Crime = models.IntegerField(null=True, default=0)
    Documentary = models.IntegerField(null=True, default=0)
    Drama = models.IntegerField(null=True, default=0)
    Family = models.IntegerField(null=True, default=0)
    Fantasy = models.IntegerField(null=True, default=0)
    History = models.IntegerField(null=True, default=0)
    Horror = models.IntegerField(null=True, default=0)
    Music = models.IntegerField(null=True, default=0)
    Mystery = models.IntegerField(null=True, default=0)
    Romance = models.IntegerField(null=True, default=0)
    ScienceFiction = models.IntegerField(null=True, default=0)
    TVMovie = models.IntegerField(null=True, default=0)
    Thriller = models.IntegerField(null=True, default=0)
    War = models.IntegerField(null=True, default=0)
    Western = models.IntegerField(null=True, default=0)
    