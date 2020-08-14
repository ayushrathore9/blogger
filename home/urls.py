from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('signup', views.signUp, name='signUp'),
    path('login', views.userlogin, name='userlogin'),
    path('logout', views.userlogout, name='userlogout'),
]