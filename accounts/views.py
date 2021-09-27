from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm

# =============== signup views 구현  ================ #
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "회원가입 환영합니다.")
            next_url = request.GET.get('next','/')
            return redirect(next_url)
    else:
        form = SignupForm()
    
    context = {'form':form}
    return render(request, 'accounts/signup_form.html', context)
