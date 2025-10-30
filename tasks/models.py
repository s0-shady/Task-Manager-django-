from django.db import models
from django.utils import timezone

class Priority(models.Model):
    name = models.CharField(max_length=100, null=False)
    weight = models.IntegerField(null=False)
    deleted = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'priorities'
        verbose_name_plural = 'Priorities'
        ordering = ['-weight']

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=True, blank=True)
    date_added = models.DateField(default=timezone.now, null=False)
    deleted = models.BooleanField(default=False, null=False)
    completion_date = models.DateField(null=True, blank=True)
    priority = models.ForeignKey(
        Priority,
        on_delete=models.PROTECT,
        null=False,
        related_name='tasks'
    )

    class Meta:
        db_table = 'tasks'
        ordering = ['-priority__weight', 'date_added']

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        return self.completion_date is not None
