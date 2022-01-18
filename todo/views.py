from typing import Tuple
from django.forms.forms import Form
from django.http.request import HttpRequest
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.db import  IntegrityError
from django.contrib.auth import login,logout, authenticate
from .forms import Todo, TodoForm
from .models import Todo
from django.utils import timezone

def home(request):
    return render(request,'todo/home.html')

def loginuser(request):
    if request.method=='GET':
        return render(request,'todo/loginuser.html',{'form': AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form': AuthenticationForm(), 'error':'Userid does not exist'})
        else:
            login(request,user)
            return redirect('todos')

def signupuser(request):

    if request.method=='GET':
        return render(request,'todo/signupuser.html',{'form': UserCreationForm()})
    else:
        # Create new user
        if request.POST['password1'] ==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('todos')

            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form': UserCreationForm(), 'error':'Userid already exist'})
        else:
            # Password is not same
            return render(request,'todo/signupuser.html',{'form': UserCreationForm(), 'error':'Password are not same'})

# LOGOUT 

def logoutuser(request):
    if(request.method== 'POST'):
        logout(request)
        return redirect('home')


def todos(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'todo/todos.html', {'todos':todos })

def completedtodos(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo/completedtodos.html', {'todos':todos })

def viewtodo(request, todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user= request.user )
    if request.method=='GET':
      form=TodoForm(instance=todo)
      return render(request,'todo/viewtodo.html', {'todo':todo , 'form':form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('todos')
        except ValueError:
            return render(request,'todo/viewtodo.html', {'todo':todo , 'form':form , 'error': 'Bad info '})


def createtodo(request):
    if request.method=='GET':
        return render(request,'todo/createtodo.html',{'form': TodoForm()})
    
    else:
        form= TodoForm(request.POST)
        newtodo=form.save(commit=False)
        newtodo.user=request.user
        newtodo.save()
        return redirect('todos')

def completetodo(request, todo_pk):
     todo=get_object_or_404(Todo,pk=todo_pk,user= request.user )
     if(request.method== 'POST'):
         todo.datecompleted=timezone.now()
         todo.save()
         return redirect('todos')

def deletetodo(request, todo_pk):
     todo=get_object_or_404(Todo,pk=todo_pk,user= request.user )
     if(request.method== 'POST'):
         todo.delete()
         return redirect('todos')