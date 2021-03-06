from django.shortcuts import render, redirect

from .models import *

from django.contrib import messages

import bcrypt

def login(request):
    return render(request, 'index.html')

def books(request):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            context = {
                "user": user[0],
                "books": Book.objects.all(),
                "books_user_likes": User.objects.get(id=request.session['userid']).liked_books.all(),
            }
        return render(request, 'books.html', context)
    return redirect('/login')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if User.objects.filter(email=request.POST['email']):
            messages.error(request, 'Email is already registered. Please login!')
            return redirect('/')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()    
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['userid'] = new_user.id
            return redirect('/books')
    return redirect('/')

def user_login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['login_email'])
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['login_pass'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/books')
        else:
            messages.error(request, 'Email/password combination not recognized. Please try again!')
        return redirect("/")

def log_off(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')

def add_book(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            new_book = Book.objects.create(title=request.POST['title'],desc=request.POST['desc'],uploaded_by=User.objects.get(id=request.POST['user_id']))
            user_who_like = User.objects.get(id=request.POST['user_id'])
            new_book.users_who_like.add(user_who_like)
            return redirect('/books')

def add_favorite(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        book_to_add = Book.objects.get(id=request.POST['book_id'])
        user_who_added = User.objects.get(id=request.POST['user_id'])
        book_to_add.users_who_like.add(user_who_added)
        return redirect('/books')

def book_details(request, book_id):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            context = {
                "user": user[0],
                "book": Book.objects.get(id=book_id),
            }
        return render(request, 'book_details.html', context)
    return redirect('/login')

def update_book(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        book_errors = Book.objects.book_validator(request.POST)
        if len(book_errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            book_to_update = Book.objects.get(id=request.POST['book_id'])
            book_to_update.title = request.POST['title']
            book_to_update.desc = request.POST['desc']
            book_to_update.save()
            return redirect('/books')

def delete(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        book_to_delete = Book.objects.get(id=request.POST['book_id'])
        book_to_delete.delete()
        return redirect('/books')

def remove_favorite(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        book_to_remove = Book.objects.get(id=request.POST['book_id'])
        user_to_remove = User.objects.get(id=request.POST['user_id'])
        book_to_remove.users_who_like.remove(user_to_remove)
        return redirect('/books')