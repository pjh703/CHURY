from django.db import models
# Create your models here.


class MYBOOK(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book_id = models.CharField(null=True, max_length=15)

    
class MYSTAR(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book_id = models.CharField(null=True, max_length=15)
    b_like = models.BooleanField(default=False)
    star = models.IntegerField(null=True, default=0)
    
    
class COMMENT(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    reply = models.CharField(null=True, max_length=100)
    c_date = models.DateTimeField(auto_now_add=True)
    u_date = models.DateTimeField(auto_now=True)


class MYSELECT(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book_id = models.CharField(null=True, max_length=15)
    add_date = models.DateTimeField(auto_now_add=True)
 

class MYCHOOSE(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
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
    