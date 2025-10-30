from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task, Priority
from .forms import TaskForm, PriorityForm


@login_required
def task_list(request):
    # Get uncompleted tasks (sorted by priority weight DESC, then date_added ASC)
    uncompleted_tasks = Task.objects.filter(
        deleted=False,
        completion_date__isnull=True
    ).select_related('priority').order_by('-priority__weight', 'date_added')
    
    # Get completed tasks (sorted by completion_date DESC)
    completed_tasks = Task.objects.filter(
        deleted=False,
        completion_date__isnull=False
    ).select_related('priority').order_by('-completion_date')
    
    context = {
        'uncompleted_tasks': uncompleted_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, deleted=False)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Add'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, deleted=False)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit'})


@login_required
def task_delete_confirm(request, pk):
    task = get_object_or_404(Task, pk=pk, deleted=False)
    if request.method == 'POST':
        task.deleted = True
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_delete_confirm.html', {'task': task})


@login_required
def task_complete_confirm(request, pk):
    task = get_object_or_404(Task, pk=pk, deleted=False, completion_date__isnull=True)
    if request.method == 'POST':
        task.completion_date = timezone.now().date()
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_complete_confirm.html', {'task': task})


@login_required
def priority_list(request):
    priorities = Priority.objects.filter(deleted=False).order_by('-weight')
    return render(request, 'tasks/priority_list.html', {'priorities': priorities})


@login_required
def priority_create(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm()
    return render(request, 'tasks/priority_form.html', {'form': form, 'action': 'Add'})


@login_required
def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk, deleted=False)
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=priority)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm(instance=priority)
    return render(request, 'tasks/priority_form.html', {'form': form, 'action': 'Edit'})


@login_required
def priority_delete_confirm(request, pk):
    priority = get_object_or_404(Priority, pk=pk, deleted=False)
    if request.method == 'POST':
        priority.deleted = True
        priority.save()
        return redirect('priority_list')
    return render(request, 'tasks/priority_delete_confirm.html', {'priority': priority})
