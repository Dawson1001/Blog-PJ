from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '请输入用户名',
        'max_length': '用户名最大长度为20',
        'min_length': '用户名最小长度为2',
    })
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入一个正确的邮箱！'})
    captcha = forms.CharField(max_length=6, min_length=6)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经被注册！')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码和邮箱不匹配！")
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入一个正确的邮箱！'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)
