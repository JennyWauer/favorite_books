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
                "user": user[0]
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
            messages.success(request, "User successfully created")
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
        user_liked = User.objects.get(id=request.POST['user_id'])
        Book.objects.create(title=request.POST['title'],desc=request.POST['desc'],uploaded_by_id=User.objects.get(id=request.POST['user_id']))
        return redirect('/books')