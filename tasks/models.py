from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Priority(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=False)
    weight = models.IntegerField(_('Weight'), null=False)
    deleted = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'priorities'
        verbose_name = _('Priority')
        verbose_name_plural = _('Priorities')
        ordering = ['-weight']

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(_('Title'), max_length=200, null=False)
    content = models.TextField(_('Content'), null=True, blank=True)
    date_added = models.DateField(_('Date Added'), default=timezone.now, null=False)
    deleted = models.BooleanField(default=False, null=False)
    completion_date = models.DateField(_('Completion Date'), null=True, blank=True)
    priority = models.ForeignKey(
        Priority,
        on_delete=models.PROTECT,
        null=False,
        related_name='tasks',
        verbose_name=_('Priority')
    )

    class Meta:
        db_table = 'tasks'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-priority__weight', 'date_added']

    def __str__(self):
        return self.title

    @property
    def is_completed(self):
        return self.completion_date is not None


# TAS-3: Attachment model
class Attachment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('Task')
    )
    file = models.FileField(_('File'), upload_to='attachments/%Y/%m/%d/')
    filename = models.CharField(_('Filename'), max_length=255)
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)

    class Meta:
        db_table = 'attachments'
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename
