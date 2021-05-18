from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
     return render(request, 'todo/home.html')


def signupuser(request):
     if request.method=='GET':
          return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
          
     else:
          if request.POST['password1']==request.POST['password2']:
               try:
                    user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('currenttodo')

               except IntegrityError:
                    return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Username Already Taken!'})
     
          else:
               return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords Did Not Match!'})


def loginuser(request):
     if request.method=='GET':
          return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
          
     else:
          user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
          if user is None:
               return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and Password did not match'})
          else:
               login(request, user)
               return redirect('currenttodo')


def logoutuser(request):
     if request.method == 'POST':
          logout(request)
          return redirect('home')


def createtodo(request):
     if request.method == 'GET':
          return render(request, 'todo/createtodo.html', {'form': TodoForm()})
     else:
          try:
               form = TodoForm(request.POST)
               finaltodo = form.save(commit=False)
               finaltodo.user = request.user
               finaltodo.save()
               return redirect('currenttodo')
          except ValueError:
               return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Wrong data inputted! Try Again.'})


def currenttodo(request):
     todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
     return render(request, 'todo/currenttodo.html', {'todos': todos})
