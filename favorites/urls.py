from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    path('books', views.success),
    path('register', views.register),
    path('user_login', views.user_login),
    path('log_off', views.log_off),
]
