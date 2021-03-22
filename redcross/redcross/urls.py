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
from django.contrib import admin
from django.urls import path, include
from infosystem import views

app_name = 'infosystem'

urlpatterns = [
    #path('infosystem/', include('infosystem.urls', namespace='infosystem')),
    #path('', views.index, name='views.index'),
    path('', include('infosystem.urls', namespace='infosystem')),
    path('admin/', admin.site.urls),  # 管理员后台界面
    path('infosystem/admin_stat/', views.admin_stat, name='admin_stat'), # 管理员界面
]
