from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.core.mail import send_mail
from .models import CaptchaModel
import string, random
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

# Create your views here.

User = get_user_model()


@require_http_methods(['POST', 'GET'])
def auth_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)  # 登录
                # 判断是否需要“记住我”
                if not remember:
                    # 如果没有点击“记住我”，设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
            return redirect('/')  # 如果点击了“记住我”，那么什么都不用执行，使用默认的两周过期时间
        else:
            print('邮箱或密码错误!')
            # form.add_error('email', '邮箱或密码错误!')
            # return render(request, 'login.html', {'form': form})
            return redirect(reverse('App_auth:login'))


def auth_logout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('App_auth:login'))
        else:
            print(form.errors)
            return redirect(reverse('App_auth:login'))


def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': '请输入有效邮箱!'})
    captcha = "".join(random.sample(string.digits, 6))
    # 存储到数据库中
    CaptchaModel.objects.update_or_create(
        email=email,
        defaults={
            'captcha': captcha,
            'create_time': timezone.now()
        }
    )
    send_mail("blog博客注册验证码", message=f"您的注册验证码为: {captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'message': "邮箱验证码发送成功!"})
