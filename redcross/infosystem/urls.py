"""redcross URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'infosystem'

urlpatterns = [
    path('', views.index, name='index'),  # 主页
    path('login_user/', views.login_user, name='login_user'),  # 登录
    path('register/', views.register, name='register'),  # 注册
    path('logout_user/', views.logout_user, name='logout_user'),  # 退出登录
    # path('admin_stat/', views.admin_stat, name='admin_stat'), # 管理员界面 (移至redcross/url.py
    path('userindex/',views.userindex, name='userindex'),  # 用户登录后界面

    path('personal_info/', views.personal_info, name='personal_info'),  # 用户个人信息
    path('personal_info/edit_info/', views.edit_info, name='edit_info'),  # 用户修改个人信息

    path('donate_resources/', views.donate_resources_result, name='donate_resources'),  # 用户查询
    path('donate_resources_result/', views.donate_resources_result, name='donate_resources_result'),  #用户查询结果

    path('donate_money/', views.donate_money_result, name='donate_money'),
    path('donate_money_result/', views.donate_money_result, name='donate_money_result'),

    path('receive_resources/', views.receive_resources_result, name='receive_resources'),
    path('receive_resources_result/', views.receive_resources_result, name='receive_resources_result'),

    path('receive_money/', views.receive_money_result, name='receive_money'),
    path('receive_money_result/', views.receive_money_result, name='receive_money_result'),
]
