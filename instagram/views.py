from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
# from .models import extract_tag_list
from django.db.models import Q
from .models import Post
from datetime import timedelta
from django.utils import timezone
#〓〓〓〓〓〓〓〓〓〓〓〓〓〓 index 구현 〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
@login_required
def index(request):
    timesince =timezone.now() - timedelta(days=3)

    # Q는 OR를 의미 : 작성자가 자기 자신이거나, 팔로워 목록에 있다면
    post_list = Post.objects.all()\
        .filter(
            Q(author=request.user) |
            Q(author__in=request.user.following_set.all())
        )\
        .filter(
            created_at__gte=timesince  #gte : grater then, lte : less then
        )

    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all())
    
    return render(request,"instagram/index.html",{
        "post_list":post_list,
        "suggested_user_list":suggested_user_list
    })

# exclude(pk=request.user.pk) : 나 자신을 제외
# exclude(pk__in=request.user.following_set.all()) : following_set에
# 있는 모든 user를 제외


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓 post new 구현 〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # tag_set은 ManyToMany 이기 때문에 add() 명령어를 사용해야 한다.
            # DB가 먼저 저장되어야 한다. PK가 필요하다.
            post.tag_set.add(*post.extract_tag_list())

            messages.success(request, "포스팅 되었씁니다.")
            return redirect(post) # model에서 absolute를 구현해야함.
    else:
        form = PostForm()

    context = {'form':form}
    return render(request, "instagram/post_form.html", context)


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 post_detail 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
# detail view를 구현하먄 models.py에서 get_absolute_url 구현 추천

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, "instagram/post_detail.html",{
        "post":post
    })

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 post_like 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
@login_required
def post_like(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request,f"{post.pk}번 게시물을 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER","root")
    return redirect(redirect_url)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 post_like 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
@login_required
def post_unlike(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request,f"{post.pk}번 게시물 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER","root")
    return redirect(redirect_url)

#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 user_page 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
def user_page(request,username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author = page_user)
    post_list_count = post_list.count() #실제 데이터베이스에 count query를 보낸다.
    # len(post_list) 이건 메모리에 모든 포스트를 가져와서 count -> 느릴수 있음

    if request.user.is_authenticated: # 로그인 O : User객체, 로그인 X :AnonymousUser
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False
    
    
    context = {
        'page_user':page_user,
        'post_list':post_list,
        'post_list_count':post_list_count,
        'is_follow':is_follow
        }
    return render(request, "instagram/user_page.html", context)

