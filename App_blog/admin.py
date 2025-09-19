from django.contrib import admin
from .models import BlogCategory, Blog, BlogComments


# Register your models here.

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time', 'category', 'author']


class BlogCommentsAdmin(admin.ModelAdmin):
    list_display = ['content', 'pub_time', 'blog', 'author']


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComments, BlogCommentsAdmin)
