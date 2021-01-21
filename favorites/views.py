from django.shortcuts import render, redirect

from .models import *

from django.contrib import messages

import bcrypt

def login(request):
    return render(request, 'index.html')

def success(request):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            context = {
                "user": user[0]
            }
        return render(request, 'success.html', context)
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
            return redirect('/success')
    return redirect('/')