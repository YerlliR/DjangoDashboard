from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('wallet/', views.wallet_list_view, name='wallet'),
    path('wallet/create-new/', views.wallet_create_view, name='wallet'),
    path('wallet/<int:wallet_id>/', views.wallet_detail_view, name='wallet'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forzar-404/', views.probar_404),

]