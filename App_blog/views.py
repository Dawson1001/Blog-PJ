from django.shortcuts import render, reverse, redirect
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComments
from .forms import PubBlogForm
from django.db.models import Q


# Create your views here.


def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={'blogs': blogs})


def blog_details(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None  # 这里获取不到blog_id应该跳转到404页面，这里简化，直接将blog_id指定为None
    return render(request, 'blog_details.html', context={'blog': blog} )


# @login_required(login_url=reverse_lazy('App_auth:login'))  # 直接用reverse("App_auth:login")需要浏览器有login页面的缓存
# @login_required(login_url='auth/login')  # 直接指定login页面的路由
@require_http_methods(['GET', 'POST'])
@login_required()  # 一劳永逸 但是需要在项目setting.py中配置"LOGIN_URL"
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={"categories": categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "博客发布成功！", "data": {"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, "message": "参数错误！"})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComments.objects.create(content=content, blog_id=blog_id, author=request.user)
    # 重新加载博客详情页
    return redirect(reverse("App_blog:blog_details", kwargs={'blog_id': blog_id}))


@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    # 从博客的标题和内容进行查找包含'q'的关键字
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request, 'index.html', context={'blogs': blogs})


@require_GET
def myblog(request):
    # 从博客的标题和内容进行查找包含'q'的关键字
    blogs = Blog.objects.filter(author_id=request.user).all()
    return render(request, 'myblog.html', context={'blogs': blogs})
