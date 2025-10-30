from django import forms
from .models import Task, Priority


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'date_added', 'priority']
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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }
