from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('generate_music', views.generate_music, name = 'generate_music'),
    path('generate_random', views.generate_random, name = 'generate_random'),
    path('forgotpassword', views.forgot_password, name= 'forgot_password'),
    path('register', views.register, name= 'register'),
    path('login', views.login, name= 'login')
]