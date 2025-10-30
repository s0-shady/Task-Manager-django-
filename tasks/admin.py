from django.contrib import admin
from .models import Task, Priority


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'weight', 'deleted']
    list_filter = ['deleted']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'date_added', 'completion_date', 'deleted']
    list_filter = ['deleted', 'priority', 'completion_date']
    search_fields = ['title', 'content']
    date_hierarchy = 'date_added'
