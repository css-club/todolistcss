from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task
def login_view(request):
    if request.user.is_authenticated:
        return redirect('task')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    return render(request, 'base/login.html')
def register(request):
    if request.user.is_authenticated:
        return redirect('task')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        else:
            try:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                return redirect('task')
            except:
                messages.error(request, 'Username already exists')
    
    return render(request, 'base/register.html')
    
            
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    search_input = request.GET.get('search-area') or ''
    if search_input:
        tasks = tasks.filter(title__icontains=search_input)
    
    context = {
        'tasks': tasks,
        'count': tasks.filter(complete=False).count(),
        'search_input': search_input
    }
    return render(request, 'base/task_list.html', context)
    

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    return render(request, 'base/task.html', {'task': task})
@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        complete = request.POST.get('complete') == 'on'
        
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            complete=complete
        )
        return redirect('task')
    return render(request, 'base/task_form.html')    

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.complete = request.POST.get('complete') == 'on'
        task.save()
        return redirect('task')
    return render(request, 'base/task_form.html', {'task': task})
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')
    return render(request, 'base/delete.html', {'task': task})
