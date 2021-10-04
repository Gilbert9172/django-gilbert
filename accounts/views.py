from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PasswordChangeForm, SignupForm
from django.contrib.auth import login as auth_login

#================= signup views 구현 ===================#
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user) #django.contrib.auth의 login으로 구현
            messages.success(request, "회원가입 환영합니다.")
            next_url = request.GET.get('next','/')
            return redirect(next_url)
    else:
        form = SignupForm()
    
    context = {'form':form}
    return render(request, 'accounts/signup_form.html', context)


#============================ login 구현 ===========================#
from django.contrib.auth.views import LoginView

login = LoginView.as_view(template_name="accounts/login_form.html")


#============================ logout 구현 ===========================#
from django.contrib.auth.views import logout_then_login

def logout(request, login_url=None):
    messages.success(request, "로그아웃이 되었습니다.")
    return logout_then_login(request,login_url)


#============================ profile Edit ===========================#
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def profile_edit(request):
    if request.method=='POST':
        # request.FILES 없으면 이미지 받을 수 없다.
        form = ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'프로필을 수정/저장했습니다.')
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=request.user)
        
    return render(request,'accounts/profile_edit_form.html',{
        'form':form
    })



#============================ password edit ===========================#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.urls import reverse_lazy

# PasswordChangeView (FormView를 상속 받음 → def form_valid(self,form):)
class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):

    success_url = reverse_lazy('password_change')
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self,form):
        messages.success(self.request,"암호를 변경했습니다.")
        return super().form_valid(form)

password_change = PasswordChangeView.as_view()


#〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓 user_follow/unfollow 〓〓〓〓〓〓〓〓〓〓〓〓〓〓〓#
from . models import User

@login_required
def user_follow(request, username):
    # accounts app안에 있으니깐 User사용 / get_user_model이랑 같음
    follow_user = get_object_or_404(User,username=username)

    # 내가 "A"를 팔로우하면, following_set에 "A"를 추가
    request.user.following_set.add(follow_user)

    # "A"입장에서는 자신을 팔로우 하는 사람들 follower_set에 나를 추가
    follow_user.follower_set.add(request.user)

    messages.success(request, f'{follow_user}님을 팔로우 했습니다.')

    # HTTP_REFERER : 헤더가 없는경우
    redirect_url = request.META.get('HTTP_REFERER','root')
    return redirect(redirect_url)

@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User,username=username)

    request.user.following_set.remove(unfollow_user)

    unfollow_user.follower_set.remove(request.user)

    messages.success(request, f'{unfollow_user}님을 팔로우 취소했습니다.')
    redirect_url = request.META.get('HTTP_REFERER','root')
    return redirect(redirect_url)