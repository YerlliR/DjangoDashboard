from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]