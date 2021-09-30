from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm
# from .models import extract_tag_list
# Create your views here.
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
            return redirect('/') # model에서 absolute를 구현해야함.
    else:
        form = PostForm()

    context = {'form':form}
    return render(request, "instagram/post_form.html", context)