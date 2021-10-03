from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
# from .models import extract_tag_list

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
from .models import Post

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, "instagram/post_detail.html",{
        "post":post
    })


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 user_page 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
def user_page(request,username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author = page_user)
    post_list_count = post_list.count() #실제 데이터베이스에 count query를 보낸다.
    # len(post_list) 이건 메모리에 모든 포스트를 가져와서 count -> 느릴수 있음
    context = {
        'page_user':page_user,
        'post_list':post_list,
        'post_list_count':post_list_count,
        }
    return render(request, "instagram/user_page.html", context)