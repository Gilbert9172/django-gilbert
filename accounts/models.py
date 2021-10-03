from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url
# =============== User Model(Profile구현) =============== #
"""
User 쿼리할 때

from django.contrib.auth import get_user_model
User = get_user_model()                     
user = User.objects.first()
user
"""

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"      # _() ; 번역
        FEMALE = "F", "여성"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True,
                                    validators=[RegexValidator(r"^010-[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=1, blank=True,
                            choices=GenderChoices.choices)

    # _form.html에서 <form>multipart/form-data 꼭 확인
    # 장고의 image_kit library                      
    avatar = models.ImageField(blank=True, upload_to="accounts/profile/%Y/%m/%d")
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)
"""
GenderType = models.TextChoices('Male','Female')
gender = models.charfield(blank=True, choices=GenderType.choices, max_length=1)
"""