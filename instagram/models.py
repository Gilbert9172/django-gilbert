from django.db import models
# from accounts.models import User / 이렇게 해도 동작은 한다.
from django.conf import settings    # 그러나 settings 추천
from django.db.models.deletion import CASCADE
from django.urls import reverse
import re
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# user
# → Post.objects.filter(author=name)
# → user.post_set.all() : default
class Post(models.Model):
    author = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                related_name="my_post_set",
                                on_delete=CASCADE
                                )
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user_set = models.ManyToManyField(
                                            settings.AUTH_USER_MODEL,
                                            related_name="like_post_set",
                                            blank=True
                                            )

    def __str__(self):
        return self.caption

    #=====================  get_absolute_url =======================#
    # detailview구현하면 추천
    def get_absolute_url(self):
        # return reverse("model_detail", kwargs={"pk": self.pk})
        return reverse("instagram:post_detail", args=[self.pk])

    #======================== tag extract ==========================#
    def extract_tag_list(self):
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag,_ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    # 인자로 받은 user가 실제로 post를 좋아하는가
    def is_like_user(self,user):
        return self.like_user_set.filter(pk=user.pk).exists()

    # post 순서 지정
    class Meta:
        ordering = ['-id']

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 comment 모델 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 Tag 모델 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
#django-taggit's 라는 라이브러리도 있음
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

# class LikeUser(models.Model):
#     post = models.ForeignKey(Post, on_delete=CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)