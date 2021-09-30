from django.db import models
# from accounts.models import User / 이렇게 해도 동작은 한다.
from django.conf import settings
from django.db.models.deletion import CASCADE
import re

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

    # detailview구현 필요
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    

    #======================== tag extract ==========================#
    def extract_tag_list(self):
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag,_ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list



#django-taggit's 라는 라이브러리도 있음
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name