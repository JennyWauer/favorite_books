from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    path('books', views.books),
    path('register', views.register),
    path('user_login', views.user_login),
    path('log_off', views.log_off),
    path('add_book', views.add_book),
    path('add_favorite', views.add_favorite),
    path('books/<int:book_id>', views.book_details),
    path('update_book',views.update_book),
]
