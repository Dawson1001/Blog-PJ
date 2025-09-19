from django.urls import path
from . import views

app_name = 'App_auth'

urlpatterns = [
    path('login', views.auth_login, name='login'),
    path('logout', views.auth_logout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='send_email_captcha'),
]
