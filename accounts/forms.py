from django import forms 
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import User

# ========================= 로그인 구현 form ========================== #
"""
물론 커스텀으로 구현해도 된다. 하지만 django에서 구현을 이미 잘 해놨다

class SignupForm(forms.ModelFrom):
    class Meta:
        model = User
        fields = ['username','password']
여기에 password를 넣으면 user의 password가 admin에 그대로 저장된다.
user.set_password('1234') → password 암호화
"""
class SignupForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    #Meta만 쓸 경우, 기존 UserCreationForm에 있는 Meta 속성은 오버라이드 한다.
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email

# ========================= profile form ========================== #


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar','first_name', 'last_name', 'website_url',
                    'bio', 'phone_number', 'gender']

# ========================= password edit form ========================== #
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError("새로운 암호는 기존 암호와 다르게 입력해주세요.")
        return new_password2