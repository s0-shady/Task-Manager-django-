"""
Views - TYLKO obsługa HTTP request/response.
Zasada Single Responsibility: View nie zawiera logiki biznesowej ani query do bazy.
Cała logika jest w services.py, dostęp do bazy w dao.py.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from .models import Task, Priority, Attachment
from .forms import TaskForm, PriorityForm, AttachmentForm
from . import services as srs  # TAS-5: używamy warstwy services


# ==================== TASK VIEWS ====================

@login_required
def task_list(request):
    """Lista zadań."""
    return render(request, 'tasks/task_list.html', srs.get_task_list_data())


@login_required
def task_detail(request, pk):
    """Szczegóły zadania."""
    try:
        context = srs.get_task_detail_data(pk)
    except Task.DoesNotExist:
        raise Http404(_("Task not found"))
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_create(request):
    """Tworzenie zadania."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': _('Add')})


@login_required
def task_update(request, pk):
    """Edycja zadania."""
    try:
        context = srs.get_task_for_form(pk)
    except Task.DoesNotExist:
        raise Http404(_("Task not found"))
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=context['task'])
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=context['task'])
    return render(request, 'tasks/task_form.html', {'form': form, 'action': _('Edit')})


@login_required
def task_delete_confirm(request, pk):
    """Potwierdzenie usunięcia zadania."""
    try:
        context = srs.get_task_for_delete(pk)
    except Task.DoesNotExist:
        raise Http404(_("Task not found"))
    
    if request.method == 'POST':
        srs.delete_task(pk)
        return redirect('task_list')
    return render(request, 'tasks/task_delete_confirm.html', context)


@login_required
def task_complete_confirm(request, pk):
    """Potwierdzenie ukończenia zadania."""
    try:
        context = srs.get_task_for_complete(pk)
    except Task.DoesNotExist:
        raise Http404(_("Task not found or already completed"))
    
    if request.method == 'POST':
        srs.complete_task(pk)
        return redirect('task_list')
    return render(request, 'tasks/task_complete_confirm.html', context)


@login_required
def task_restore_confirm(request, pk):
    """Potwierdzenie przywrócenia zadania (TAS-4)."""
    try:
        context = srs.get_task_for_restore(pk)
    except Task.DoesNotExist:
        raise Http404(_("Task not found or not completed"))
    
    if request.method == 'POST':
        srs.restore_task(pk)
        return redirect('task_list')
    return render(request, 'tasks/task_restore_confirm.html', context)


# ==================== ATTACHMENT VIEWS (TAS-3) ====================

@login_required
def attachment_add(request, task_pk):
    """Dodawanie załącznika."""
    try:
        context = srs.get_attachment_form_data(task_pk)
    except Task.DoesNotExist:
        raise Http404(_("Task not found"))
    
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            srs.create_attachment(task_pk, request.FILES['file'], request.FILES['file'].name)
            return redirect('task_detail', pk=task_pk)
    else:
        form = AttachmentForm()
    
    context['form'] = form
    return render(request, 'tasks/attachment_form.html', context)


@login_required
def attachment_delete(request, pk):
    """Usuwanie załącznika."""
    try:
        context = srs.get_attachment_for_delete(pk)
    except Attachment.DoesNotExist:
        raise Http404(_("Attachment not found"))
    
    if request.method == 'POST':
        task_pk = srs.delete_attachment(pk)
        return redirect('task_detail', pk=task_pk)
    return render(request, 'tasks/attachment_delete_confirm.html', context)


# ==================== PRIORITY VIEWS ====================

@login_required
def priority_list(request):
    """Lista priorytetów."""
    return render(request, 'tasks/priority_list.html', srs.get_priority_list_data())


@login_required
def priority_create(request):
    """Tworzenie priorytetu."""
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm()
    return render(request, 'tasks/priority_form.html', {'form': form, 'action': _('Add')})


@login_required
def priority_update(request, pk):
    """Edycja priorytetu."""
    try:
        context = srs.get_priority_for_form(pk)
    except Priority.DoesNotExist:
        raise Http404(_("Priority not found"))
    
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=context['priority'])
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm(instance=context['priority'])
    return render(request, 'tasks/priority_form.html', {'form': form, 'action': _('Edit')})


@login_required
def priority_delete_confirm(request, pk):
    """Potwierdzenie usunięcia priorytetu."""
    try:
        context = srs.get_priority_for_delete(pk)
    except Priority.DoesNotExist:
        raise Http404(_("Priority not found"))
    
    if request.method == 'POST':
        srs.delete_priority(pk)
        return redirect('priority_list')
    return render(request, 'tasks/priority_delete_confirm.html', context)
