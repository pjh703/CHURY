from email.policy import default
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone

# Create your models here.
class CustomUser(auth_models.User):
    """내장 모델 클래스인 User 클래스를 상속받아 구현한 사용자 정의 모델 클래스"""

    # 기존 User 클래스에서 제공하는 필드 외 추가하고 싶은 필드가 있으면,
    # User 클래스를 상속받는 클래스를 만들어서 직접 작성
    password2 = models.CharField(max_length=150, verbose_name='비밀번호 확인')  # 비밀번호 확인 필드
    address = models.TextField(verbose_name='주소')  # 주소 필드


class UserChu(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
