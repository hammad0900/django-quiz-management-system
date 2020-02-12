from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.contrib.auth import (login,logout,authenticate,get_user_model)
from rest_framework.authtoken.models import Token
from django.contrib.messages import constants as messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session
from Quizapp.models import *


# Create your views here.
# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('/home')
#     next = request.GET.get('next')
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(username=username,password=password)
#         login(request,user)
        
#         if next:
#             return redirect(next)
#         return redirect('/home')

#     return render(request,'login.html',{'form':form})



# def logoutsession(request):
#     auth.logout(request)
#     return render(request,'/home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method=='POST':
        form = AuthenticationForm(request.user,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                # request.session.set_expiry(300) 
                login(request,user)
                return redirect('/home') 
        else:
            print("user not found")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form}) 

@login_required
def home(request):
    # print(dir(request.META),"ye username")
    user=request.user
    ip = request.META.get('REMOTE_ADDR')
    
    topic_count=Topic.objects.all().count()
    subject_count=Subject.objects.all().count()
    class_count=Class.objects.all().count()
    question_count=Questions.objects.all().count()
        
    return render(request,"index.html",{'headers':request.headers,'topic_count':topic_count,'subject_count':subject_count,'class_count':class_count,'question_count':question_count})

def user_logout(request):
    if request.method=='POST':
        logout(request)
        return redirect('/accounts/login')
    else:
        return redirect('/home')

    