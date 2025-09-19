from django.urls import path
from . import views

app_name = 'App_blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/detail/<int:blog_id>', views.blog_details, name='blog_details'),
    path('blog/pub', views.pub_blog, name='pub_blog'),
    path('blog/comment/pub', views.pub_comment, name='pub_comment'),
    path('blog/search', views.search, name='search'),
    path('myblog', views.myblog, name='myblog'),
]
