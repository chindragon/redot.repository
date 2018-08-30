"""redot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('index', views.index),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('register', views.user_register),
    path('confirm_user_register', views.confirm_user_register),
    path('confirm_user_login', views.confirm_user_login),
    path('query_from_board_tree_node', views.query_from_board_tree_node, name='query_from_board_tree_node')
]
