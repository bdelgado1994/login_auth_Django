from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .form import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Method for create a new User
def create_user(request):
    context = {"form": UserCreationForm}
    if request.method == "GET":
        return render(request, "pages/singup.html", context)
    else:
        password = request.POST.get("password1")
        password_2 = request.POST.get("password2")
        username = request.POST.get("username")
        if password == password_2:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                )
                user.save()
                login(request, user)
                return redirect("task")
            except IntegrityError:
                messages.error(request, "El Usuario se encuentra registrado")
                return redirect("singup")
        else:
            messages.error(request, "Las Contraseñas deben de ser iguales")
            return redirect("singup")


# LogIn Method
def singin(request):
    context = {"form": AuthenticationForm}
    if request.method == "GET":
        return render(request, "pages/login.html", context)
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            messages.error(request, "Username or password is incorrect")
            return redirect("login")
        login(request, user)
        return redirect("task")


# close session method
def close_session(request):
    logout(request)
    return redirect("home")


# Method to call Task Page
def task_page(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True).order_by(
            "-datecompleted"
        )  
        return render(request, "pages/task.html", {"tasks": tasks})
    else:
        return render(request, "pages/task.html")


# This page show you a specific task
def task_detail(request, id_task):
    if request.method == "GET":
        if request.user.is_authenticated:
            task = get_object_or_404(Task, id=id_task, user=request.user)
            form = TaskForm(instance=task)
            return render(
                request, "pages/task_details.html", {"task": task, "form": form}
            )
        else:
            return redirect('task')
    else:
        task = get_object_or_404(Task, id=id_task, user=request.user)
        if request.POST.get("datecompleted",None):
            task.datecompleted = timezone.now()
        else:
            task.datecompleted=None
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('task')
# In this Method or function you can create a new task
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "pages/create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("task")
        except Exception as ex:
            messages.error(request, "Coudn't create a new task please try again")
            return redirect("create_task")
#This Method Delete a Task
@login_required
def delete_task(request,id_task):
    task = get_object_or_404(Task, id=id_task, user=request.user)
    task.delete()
    return redirect('task')
#This metohd show you all tasks completed
def tasks_completed(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by(
            "-datecompleted"
        )  
        return render(request, "pages/tasks_completed.html", {"tasks": tasks})
    else:
        return render(request,"pages/tasks_completed.html")

# This is our HomePage
def home(request):
    return render(request, "pages/home.html")
