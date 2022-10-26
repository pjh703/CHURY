from tabnanny import verbose
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone

class BoardDetail(models.Model):
    """게시글을 나타내는 모델 클래스"""

    title = models.CharField(max_length=50)  # 제목
    author = models.CharField(max_length=20)  # 내용
    date = models.DateTimeField(default=timezone.now)  # 작성일
    isbn13 = models.CharField(max_length=13)
