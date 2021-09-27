from django.contrib.auth.models import AbstractUser
from django.db import models

# =============== User Model(Profile구현) =============== #
"""
User 쿼리할 때

from django.contrib.auth import get_user_model
User = get_user_model()                     
user = User.objects.first()
user
"""

class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    pass
