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