from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task, Priority, Attachment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'date_added', 'priority']
        labels = {
            'title': _('Title'),
            'content': _('Content'),
            'date_added': _('Date Added'),
            'priority': _('Priority'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'date_added': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['priority'].queryset = Priority.objects.filter(deleted=False)


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name', 'weight']
        labels = {
            'name': _('Name'),
            'weight': _('Weight'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# TAS-3: Attachment form
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        labels = {
            'file': _('File'),
        }
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
